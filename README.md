# YouTube Playables Integration

Reusable Codex skill for adapting browser-based HTML5 games to the YouTube
Playables SDK.

## Included

- SDK loading order and Playables lifecycle
- `playablesBridge` adapter pattern
- Cloud save/load, versioned schema and migration
- Canonical score submission
- Host pause/resume and audio synchronization
- Rewarded ads with safe reward claiming
- Release bundle, CSP and size validation
- Local bridge tests and Playables Test Suite checklist

## Install as a Codex skill

Copy this folder to the local Codex skills directory:

```text
Windows: %USERPROFILE%\.codex\skills\youtube-playables-integration
macOS/Linux: ~/.codex/skills/youtube-playables-integration
```

Then invoke it explicitly with:

```text
$youtube-playables-integration
```

The skill is also eligible for automatic invocation when a task is clearly
about integrating an HTML5 game with YouTube Playables.

## Contents

```text
youtube-playables-integration/
├── SKILL.md
├── agents/openai.yaml
└── references/implementation-guide.md
```

This is an evolving integration guide. Portal onboarding, certification, full
device QA, remote leaderboards and future monetization work remain separate
follow-up areas.

## Official documentation

- [Getting started](https://developers.google.com/youtube/gaming/playables/reference/getting_started)
- [SDK reference](https://developers.google.com/youtube/gaming/playables/reference/sdk)
- [Integration requirements](https://developers.google.com/youtube/gaming/playables/certification/requirements_integration)
- [Monetization](https://developers.google.com/youtube/gaming/playables/reference/monetization)
- [Stability and performance](https://developers.google.com/youtube/gaming/playables/certification/requirements_stability)
