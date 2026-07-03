# Ecosystem

Repository catalog for the Stubborn AI program. Status legend: ✅ Active · 📋 Planned · 💡 Idea (lab-notes only).

## Core (ship first)

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| [**stubborn**](https://github.com/stubborn-ai/stubborn) | [`stubborn-stub`](https://pypi.org/project/stubborn-stub/), CLI `stubborn` | SCIP ingest, SQLite store, prune, weave, `stubborn.api`, CLI | ✅ **Beta** `0.9.0b4` |
| [**stubborn-hub**](https://github.com/stubborn-ai/stubborn-hub) | — | Program docs, architecture, roadmap | ✅ Active |

## Surfaces (agent & dev UX)

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| **stubborn-mcp** | [`stubborn-mcp`](https://pypi.org/project/stubborn-mcp/) | FastMCP stdio — `get_context`, `list_symbols`, `metrics` | ✅ **Beta** `0.1.0b1` |
| **stubborn-watch** | `stubborn-watch` | File watch → external SCIP indexer → `stubborn index --merge` | ✅ **Beta** `0.1.0b1` (repo scaffold) |

## Private / meta

| Repository | Role | Status |
|------------|------|--------|
| **lab-notes** | Journals, ADR drafts, ecosystem ideas | ✅ Private remote |
| **.github** | Org profile README | ✅ Active |

## Ideas (lab-notes — not public roadmap commitments)

Tracked in [`lab-notes/ideas/`](../lab-notes/ideas/) until promoted:

| Idea | Summary |
|------|---------|
| Pluggable ingest | SCIP canonical + opt-in OpenAPI / LSP / DB adapters |
| IDE extensions | `vscode-stubborn` — status bar, symbol browse, trigger watch |
| `stubborn-indexer` | Unified CLI to invoke scip-java / scip-typescript / … |
| Gradle/Maven hook | Post-compile full snapshot in CI |
| Hybrid graph | Code + API + schema edges in one `symbols.db` |

## External ecosystem (not our repos)

| Tool | Role |
|------|------|
| [scip-java](https://github.com/sourcegraph/scip-java) | Java SCIP indexer (beta primary path) |
| [scip-typescript](https://github.com/sourcegraph/scip-typescript) | TypeScript indexer (1.0 candidate) |
| [scip-python](https://github.com/sourcegraph/scip-python) | Python indexer |
| [scip-clang](https://github.com/sourcegraph/scip-clang) | C/C++ indexer |
| [anchor-migration](https://github.com/anchor-migration) | Optional consumer — migration SSOT program |

## Dependency graph

```
scip-* (external)
       ↓
   stubborn-stub  ←── stubborn-mcp
       ↑
   stubborn-watch
```

## Naming conventions

| Pattern | Example | Use |
|---------|---------|-----|
| `stubborn` | core repo | Compiler — short name for the main product |
| `stubborn-*` | `stubborn-mcp`, `stubborn-watch` | Program repos in the same org |
| `stubborn-stub` | PyPI package | Historical PyPI name for the core library |
| `stubborn-ingest-*` | `stubborn-ingest-openapi` | Optional future adapter packages |

## Promotion workflow

```
lab-notes/ideas  →  stubborn ADR or hub doc  →  new repo + ROADMAP item
```

Do not create public repos for 💡 ideas until an ADR or hub decision record exists.
