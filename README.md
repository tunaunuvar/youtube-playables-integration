# YouTube Playables Guide

An open Agent Skills repository for adapting, auditing, packaging, and testing
web games for YouTube Playables. It combines actionable agent instructions,
human-readable guidance, official-source references, a release checklist, and a
dependency-free bundle validator.

## What this repository is

This is an **Agent Skill** following the open `SKILL.md` format used by Codex,
Claude Code, Cursor, OpenCode, and other compatible coding agents. Install the
complete repository and invoke `$youtube-playables-guide` in a game project. The
agent is instructed to inspect the actual project, preserve its engine and
package manager, implement the integration, run available checks, and return an
evidence-based readiness report—not merely explain the API.

`agents/openai.yaml` adds optional Codex/ChatGPT presentation metadata; the core
`SKILL.md`, references, and scripts remain portable. The Markdown references are
also useful as standalone human documentation.

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

## Install with NPX

After publishing the repository, replace `<owner>` with the GitHub account or
organization name. The open Agent Skills CLI can install the GitHub repository
without this project publishing a separate NPM package:

```bash
npx skills add <owner>/youtube-playables-guide
```

The interactive installer detects supported agents and lets the user choose
installation targets. Install globally for all projects with:

```bash
npx skills add <owner>/youtube-playables-guide -g
```

Install explicitly for Codex with:

```bash
npx skills add <owner>/youtube-playables-guide -g -a codex
```

Use `--list` first to inspect the skills found in the repository:

```bash
npx skills add <owner>/youtube-playables-guide --list
```

If a persistent system-wide CLI is preferred instead of NPX:

```bash
npm install --global skills
skills add <owner>/youtube-playables-guide -g
```

Here the first `--global` installs the CLI; the later `-g` installs the skill for
all projects supported by the selected AI agent.

## Manual Codex installation

Git remains available as a fallback:

```powershell
git clone https://github.com/<owner>/youtube-playables-guide.git "$env:USERPROFILE\.codex\skills\youtube-playables-guide"
```

On macOS/Linux:

```bash
git clone https://github.com/<owner>/youtube-playables-guide.git "${CODEX_HOME:-$HOME/.codex}/skills/youtube-playables-guide"
```

Invoke it explicitly with:

```text
$youtube-playables-guide
```

It can also be selected automatically for YouTube Playables integration,
compliance, packaging, and certification-readiness tasks.

The skill can be distributed with `npx skills`, but the YouTube Playables SDK
itself is **not** an NPM dependency. NPM, pnpm, or Yarn is used in a game project
only when that project's existing build system requires it. See
[setup-and-testing.md](references/setup-and-testing.md) for lockfile-aware
dependency commands, local serving, and the full test sequence.

## Repository structure

```text
youtube-playables-guide/
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

## Skill ecosystem

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Open Agent Skills CLI](https://github.com/vercel-labs/skills)
