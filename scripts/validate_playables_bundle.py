#!/usr/bin/env python3
"""Static preflight checks for a YouTube Playables directory or ZIP bundle.

This intentionally does not claim to certify runtime behavior, rights, Portal
metadata, initial network transfer size, cloud-save size, or device performance.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Iterable
from urllib.parse import urlparse
from zipfile import BadZipFile, ZipFile


SDK_URL = "https://www.youtube.com/game_api/v1"
MAX_FILES = 8_000
MAX_TOTAL_BYTES = 250 * 1024 * 1024
MAX_FILE_BYTES = 30 * 1024 * 1024
RECOMMENDED_FILE_BYTES = 512 * 1024
SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9_.-]+$")
ABSOLUTE_URL = re.compile(r"(?:https?:)?//[^\s\"'<>`)]+", re.IGNORECASE)
TEXT_SUFFIXES = {
    ".html", ".htm", ".js", ".mjs", ".cjs", ".css", ".json", ".txt",
    ".xml", ".svg", ".map", ".wasm.map",
}
DEBUG_NAMES = {"devtools.js", "debug.js", "stats.js", ".env", ".env.local"}


@dataclass
class Finding:
    level: str
    code: str
    message: str


class ScriptOrderParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.scripts: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.lower() == "script":
            # Inline code is still game code and therefore affects SDK order.
            self.scripts.append(values.get("src") or "__INLINE_SCRIPT__")
        if tag.lower() in {"link", "img", "audio", "video", "source", "iframe"}:
            value = values.get("href") or values.get("src")
            if value:
                self.links.append(value)


class Bundle:
    def __init__(self, source: Path) -> None:
        self.source = source
        self._zip: ZipFile | None = None

    def __enter__(self) -> "Bundle":
        if self.source.is_file():
            self._zip = ZipFile(self.source)
        return self

    def __exit__(self, *_: object) -> None:
        if self._zip:
            self._zip.close()

    def files(self) -> list[tuple[str, int]]:
        if self._zip:
            return [(item.filename, item.file_size) for item in self._zip.infolist() if not item.is_dir()]
        return [
            (path.relative_to(self.source).as_posix(), path.stat().st_size)
            for path in self.source.rglob("*") if path.is_file()
        ]

    def read(self, name: str, limit: int = 4 * 1024 * 1024) -> bytes:
        if self._zip:
            info = self._zip.getinfo(name)
            if info.file_size > limit:
                return b""
            return self._zip.read(info)
        path = self.source.joinpath(*PurePosixPath(name).parts)
        if path.stat().st_size > limit:
            return b""
        return path.read_bytes()


def is_external(value: str) -> bool:
    value = value.strip()
    if value.startswith(("data:", "blob:", "#")):
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc or value.startswith("//"))


def path_findings(name: str) -> Iterable[Finding]:
    if "\\" in name:
        yield Finding("error", "PATH_SEPARATOR", f"Backslash path separator: {name}")
        return
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        yield Finding("error", "UNSAFE_PATH", f"Path must be relative and traversal-free: {name}")
    for segment in path.parts:
        if not SAFE_SEGMENT.fullmatch(segment):
            yield Finding("error", "INVALID_FILENAME", f"Unsupported filename characters: {name}")
            break


def inspect_html(bundle: Bundle, findings: list[Finding]) -> None:
    try:
        html = bundle.read("index.html").decode("utf-8-sig", errors="replace")
    except (KeyError, OSError):
        findings.append(Finding("error", "INDEX_READ", "Could not read root index.html."))
        return

    parser = ScriptOrderParser()
    parser.feed(html)
    sdk_positions = [i for i, src in enumerate(parser.scripts) if src.split("?", 1)[0] == SDK_URL]
    if not sdk_positions:
        findings.append(Finding("error", "SDK_MISSING", f"Missing required SDK script: {SDK_URL}"))
    elif sdk_positions[0] != 0:
        findings.append(Finding("error", "SDK_ORDER", "YouTube SDK must precede every other external game script."))
    if len(sdk_positions) > 1:
        findings.append(Finding("warning", "SDK_DUPLICATE", "YouTube SDK is loaded more than once."))

    for value in parser.scripts + parser.links:
        if is_external(value) and value.split("?", 1)[0] != SDK_URL:
            findings.append(Finding("error", "EXTERNAL_RESOURCE", f"External resource in index.html: {value}"))
        elif value.startswith("/") and not value.startswith("//"):
            findings.append(Finding("error", "ROOT_RELATIVE", f"Use a relative bundle path, not root-relative: {value}"))


def inspect_text(bundle: Bundle, files: list[tuple[str, int]], findings: list[Finding]) -> None:
    for name, _ in files:
        path = PurePosixPath(name)
        if path.name.lower() in DEBUG_NAMES:
            findings.append(Finding("warning", "DEBUG_ARTIFACT", f"Possible debug artifact: {name}"))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = bundle.read(name)
        if not raw:
            continue
        text = raw.decode("utf-8", errors="ignore")
        for match in sorted(set(ABSOLUTE_URL.findall(text))):
            clean = match.rstrip(".,;}")
            if clean.split("?", 1)[0] != SDK_URL:
                findings.append(Finding(
                    "warning", "URL_REVIEW",
                    f"Review absolute URL in {name}: {clean}",
                ))


def validate(source: Path) -> tuple[dict[str, int | str], list[Finding]]:
    findings: list[Finding] = []
    with Bundle(source) as bundle:
        files = bundle.files()
        names = [name for name, _ in files]
        total = sum(size for _, size in files)
        summary: dict[str, int | str] = {
            "source": str(source.resolve()),
            "file_count": len(files),
            "total_bytes": total,
            "largest_file_bytes": max((size for _, size in files), default=0),
        }

        if "index.html" not in names:
            findings.append(Finding("error", "INDEX_ROOT", "Bundle root must contain index.html."))
        if len(files) > MAX_FILES:
            findings.append(Finding("error", "FILE_COUNT", f"{len(files)} files exceeds {MAX_FILES}."))
        if total >= MAX_TOTAL_BYTES:
            findings.append(Finding("error", "TOTAL_SIZE", "Uncompressed bundle must be smaller than 250 MiB."))

        for name, size in files:
            findings.extend(path_findings(name))
            if size >= MAX_FILE_BYTES:
                findings.append(Finding("error", "FILE_SIZE", f"File must be smaller than 30 MiB: {name}"))
            elif size > RECOMMENDED_FILE_BYTES:
                findings.append(Finding("warning", "FILE_SIZE_TARGET", f"File exceeds recommended 512 KiB: {name}"))

        if "index.html" in names:
            inspect_html(bundle, findings)
        inspect_text(bundle, files, findings)

    findings.append(Finding(
        "manual", "RUNTIME_REQUIRED",
        "Still verify lifecycle, pause/audio, save/score, CSP, initial transfer, 512 MB heap, devices, rights, metadata and Portal fields.",
    ))
    return summary, findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Release directory or .zip file")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    source: Path = args.bundle
    if not source.exists() or (source.is_file() and source.suffix.lower() != ".zip"):
        parser.error("bundle must be an existing directory or .zip file")

    try:
        summary, findings = validate(source)
    except BadZipFile:
        print("ERROR ZIP_INVALID: Input is not a valid ZIP file.", file=sys.stderr)
        return 2

    errors = sum(item.level == "error" for item in findings)
    warnings = sum(item.level == "warning" for item in findings)
    result = "FAIL" if errors else "PASS"
    if args.json:
        print(json.dumps({
            "result": result,
            "summary": summary,
            "errors": errors,
            "warnings": warnings,
            "findings": [asdict(item) for item in findings],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"{result}: {summary['file_count']} files, {summary['total_bytes']} bytes")
        for item in findings:
            print(f"{item.level.upper():7} {item.code}: {item.message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
