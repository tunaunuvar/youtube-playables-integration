# YouTube Playables Integration

A reusable Codex skill for adapting, auditing, packaging, and testing web games
for YouTube Playables.

The skill covers the full path from an existing HTML5/Canvas/WebGL or engine web
export to a certification-readiness report:

- Playables SDK lifecycle and environment detection
- Cloud save/load, migration, canonical scores, host pause and audio
- Rewarded and interstitial ads through YouTube APIs
- Privacy, external-call and personal-data restrictions
- Responsive game design, touch/mouse input and accessibility
- Bundle limits, relative paths, filenames, CSP and release ZIP validation
- Unity WebGL, Godot Web, Flutter Web and standard HTML5 notes
- Test Suite, real-device QA, Developer Portal and certification workflow
- Trust & Safety, audience, metadata and rights checks

## Install as a Codex skill

After publishing the repository, replace `<owner>` with the GitHub account or
organization name and clone the complete repository:

```powershell
git clone https://github.com/<owner>/youtube-playables-integration.git "$env:USERPROFILE\.codex\skills\youtube-playables-integration"
```

On macOS/Linux:

```bash
git clone https://github.com/<owner>/youtube-playables-integration.git "${CODEX_HOME:-$HOME/.codex}/skills/youtube-playables-integration"
```

Invoke it explicitly with:

```text
$youtube-playables-integration
```

It can also be selected automatically for YouTube Playables integration,
compliance, packaging, and certification-readiness tasks.

The skill itself and the YouTube Playables SDK do **not** require an NPM
installation. NPM, pnpm, or Yarn is used only when the target game's existing
build system requires it. See
[setup-and-testing.md](references/setup-and-testing.md) for lockfile-aware
dependency commands, local serving, and the full test sequence.

## Repository structure

```text
youtube-playables-integration/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   └── validate_playables_bundle.py
├── tests/
│   └── test_validator.py
└── references/
    ├── official-requirements.md
    ├── setup-and-testing.md
    ├── implementation-guide.md
    ├── game-design-and-accessibility.md
    ├── engine-notes.md
    ├── release-and-certification.md
    └── preflight-checklist.md
```

## Bundle validator

Run the dependency-free validator against a release directory or ZIP:

```bash
python scripts/validate_playables_bundle.py path/to/release
python scripts/validate_playables_bundle.py path/to/release.zip
```

It checks the root entry point, SDK order, file count, total and individual file
sizes, filename characters, relative references, external URLs, and common debug
artifacts. Runtime behavior, initial network transfer size, save size, rights,
Portal metadata, and certification still require manual or hosted testing.

Run the validator tests with:

```bash
python -m unittest discover -s tests -v
```

## Test the game in YouTube's environment

Start the release build on a local HTTP server, then open the official
[YouTube Playables SDK Test Suite](https://developers.google.com/youtube/gaming/playables/test_suite).
The SDK is a no-op during ordinary local serving, so a local smoke test alone
cannot validate the Playables integration.

After uploading a release through the invitation-only Developer Portal, open
**Verify and test** and use its **Test Suite Link** and **YouTube Dev Link**.
Test the latter on desktop web, mobile web, YouTube for Android, and YouTube for
iOS before submitting for certification.

## Authority and freshness

Official English Google/YouTube documentation is authoritative. The bundled
research snapshot was reviewed on **2026-08-28** and deliberately links every
requirement group back to its source. Always check the official
[revision history](https://developers.google.com/youtube/gaming/playables/certification/revisionhistory)
before submission.

## Core official sources

- [Playables overview](https://developers.google.com/youtube/gaming/playables)
- [Getting started](https://developers.google.com/youtube/gaming/playables/reference/getting_started)
- [SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk)
- [Certification requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements)
- [Test Suite guide](https://developers.google.com/youtube/gaming/playables/reference/test_suite_guide)
- [Open Playables Test Suite](https://developers.google.com/youtube/gaming/playables/test_suite)
- [Developer Portal](https://developers.google.com/youtube/gaming/playables/developer_portal)
- [Official web-game samples](https://github.com/google/web-game-samples)

This repository provides implementation guidance and automated preflight checks;
it does not guarantee acceptance by YouTube.
