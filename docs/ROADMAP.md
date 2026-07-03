# Roadmap

Near-term program phases. Status legend: ✅ Done · 🚧 In progress · 📋 Planned · 💡 Idea (see lab-notes).

Large exploratory items stay in [`lab-notes/ideas/`](../lab-notes/ideas/) — not listed here unless promoted.

## Phase 0 — Foundation

| Item | Repo | Status |
|------|------|--------|
| Core compiler (ingest → weave) | stubborn | ✅ Beta `0.9.0b3` |
| Java E2E + Docker CI | stubborn | ✅ |
| Product ADRs 001–008 | stubborn | ✅ |
| Program hub (`stubborn-hub`) | stubborn-hub | 🚧 This repo |
| Org profile (`.github`) | stubborn-ai | 📋 |

## Phase 1 — Beta hardening

| Item | Repo | Status |
|------|------|--------|
| ADR-009 incremental merge (`--merge`, schema v2) | stubborn | 📋 ADR accepted |
| Release `0.9.0b4` (unreleased changelog items) | stubborn | 📋 |
| Real-project validation runbook | stubborn-hub or stubborn | 📋 |

## Phase 2 — Agent & dev loop

| Item | Repo | Status |
|------|------|--------|
| Extract MCP server | stubborn-mcp | ✅ `0.1.0b1` |
| `stubborn-watch` (Java, debounced) | stubborn-watch | 📋 |
| demo-spring: save → merge → `list_symbols` E2E | stubborn | 📋 |

## Phase 3 — Stable 1.0 (direction)

| Item | Repo | Status |
|------|------|--------|
| Multi-language weave E2E (TS first) | stubborn | 💡 |
| Stable public API semver | stubborn | 💡 |
| IDE extension MVP | vscode-stubborn | 💡 |

## Not on this roadmap

See lab-notes for: pluggable non-SCIP ingest, hybrid code+API graphs, IntelliJ plugin, `stubborn-indexer` wrapper.

## Related

- [stubborn CHANGELOG](https://github.com/stubborn-ai/stubborn/blob/main/CHANGELOG.md) — shipped product changes
- [stubborn BETA](https://github.com/stubborn-ai/stubborn/blob/main/docs/BETA.md) — beta checklist & KPIs
