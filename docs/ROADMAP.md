# Roadmap

Near-term program phases. Status legend: ✅ Done · 🚧 In progress · 📋 Planned · 💡 Idea (see lab-notes).

Large exploratory items stay in [`lab-notes/ideas/`](../lab-notes/ideas/) — not listed here unless promoted.

## Phase 0 — Foundation

| Item | Repo | Status |
|------|------|--------|
| Core compiler (ingest → weave) | stubborn | ✅ Beta `0.9.0b4` on PyPI |
| Java E2E + Docker CI | stubborn-demo | ✅ |
| Product ADRs 001–009 | stubborn | ✅ |
| Program hub (`stubborn-hub`) | stubborn-hub | ✅ |
| Org profile (`.github`) | stubborn-ai | ✅ |
| MCP server package | stubborn-mcp | ✅ `0.1.0b1` on PyPI |

## Phase 1 — Beta hardening

| Item | Repo | Status |
|------|------|--------|
| ADR-009 incremental merge (`--merge`, schema v2) | stubborn | ✅ |
| Real-project validation runbook | stubborn-demo | ✅ initial repo |

## Phase 2 — Dev loop

| Item | Repo | Status |
|------|------|--------|
| `stubborn-watch` (Java, debounced) | stubborn-watch | ✅ `0.1.0b1` on PyPI |
| demo-spring: save → merge → `list_symbols` E2E | stubborn-demo | ✅ host runbook |
| VS Code thin bridge scaffold | vscode-stubborn | 📋 Planned |

## Phase 3 — Stable 1.0 (direction)

| Item | Repo | Status |
|------|------|--------|
| Multi-language weave E2E (TS first) | stubborn | 💡 |
| Stable public API semver | stubborn | 💡 |
| OpenAPI contract graph adapter | stubborn-ingest-openapi | 📋 Planned after ADR-011 |
| IDE extension MVP | vscode-stubborn | 📋 MCP setup + sidecar stubs |

## Not on this roadmap

See lab-notes for: pluggable non-SCIP ingest beyond OpenAPI, hybrid code+API+schema graphs beyond REST, IntelliJ plugin, `stubborn-indexer` wrapper.

## Related

- [stubborn CHANGELOG](https://github.com/stubborn-ai/stubborn/blob/main/CHANGELOG.md) — `stubborn-stub` releases
- [stubborn-mcp CHANGELOG](https://github.com/stubborn-ai/stubborn-mcp/blob/main/CHANGELOG.md) — MCP releases
- [stubborn BETA](https://github.com/stubborn-ai/stubborn/blob/main/docs/BETA.md) — beta checklist & KPIs
