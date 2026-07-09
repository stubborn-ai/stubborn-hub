# Ecosystem

Repository catalog for the Stubborn AI program. Status legend: ✅ Active · 📋 Planned · 💡 Idea (lab-notes only).

## Core (ship first)

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| [**stubborn**](https://github.com/stubborn-ai/stubborn) | [`stubborn-stub`](https://pypi.org/project/stubborn-stub/), CLI `stubborn` | Headless core: SCIP code ingest, OpenAPI/manifest contract ingest, SQLite store, prune, weave, `stubborn.api`, CLI, `doctor` | ✅ **Beta** `0.9.0b5` |
| [**stubborn-hub**](https://github.com/stubborn-ai/stubborn-hub) | — | Program docs, architecture, roadmap | ✅ Active |

## Demos & validation

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| [**stubborn-demo**](https://github.com/stubborn-ai/stubborn-demo) | — | Runnable demos and black-box validation projects (`demo-spring`, PetClinic, Duke's Bank) | ✅ Active |

## Surfaces (agent & dev UX)

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| **stubborn-mcp** | [`stubborn-mcp`](https://pypi.org/project/stubborn-mcp/) | FastMCP stdio — `workspace_info`, `list_symbols`, `list_contracts`, `get_context`, `metrics`; `doctor` | ✅ **Beta** `0.1.0b2` |
| **stubborn-watch** | [`stubborn-watch`](https://pypi.org/project/stubborn-watch/) | File watch → external SCIP indexer → `stubborn index --merge`; `doctor` | ✅ **Beta** `0.1.0b2` |
| [**vscode-stubborn**](https://github.com/stubborn-ai/vscode-stubborn) | VS Code extension | Thin IDE bridge for Stubborn MCP setup and sidecar stub UX | 📋 Planned |
| **stubborn-status** | CLI `stubborn-status` | Aggregate federated `doctor --json` for terminal, CI, and IDE consumers ([ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md)) | ✅ **Beta** `0.1.0b1` (repo; PyPI pending) |

## Contract ingest

| Repository | PyPI / entry | Role | Status |
|------------|--------------|------|--------|
| [**stubborn**](https://github.com/stubborn-ai/stubborn) | CLI `index-openapi`, `index-contract` | OpenAPI/manifest → contract graph facts for REST endpoints, schema constraints, and service-boundary evidence ([ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md), [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md)) | ✅ Active |

## Private / meta

| Repository | Role | Status |
|------------|------|--------|
| **lab-notes** | Journals, ADR drafts, ecosystem ideas | ✅ Private remote |
| **.github** | Org profile README | ✅ Active |

## Ideas (lab-notes — not public roadmap commitments)

Tracked in [`lab-notes/ideas/`](../lab-notes/ideas/) until promoted:

| Idea | Summary |
|------|---------|
| Pluggable ingest beyond OpenAPI | SCIP canonical for code + opt-in LSP / DB adapters |
| IntelliJ extension | Separate future repo; platform-specific thin IDE bridge |
| `stubborn-indexer` | Unified CLI to invoke scip-java / scip-typescript / … |
| Gradle/Maven hook | Post-compile full snapshot in CI |
| Hybrid graph beyond REST | Code + API + schema edges in one `symbols.db` |

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
scip-* (external)        OpenAPI specs / contract manifests
       ↓                      ↓
                stubborn-stub
                ↑          ↑
   stubborn-watch          stubborn-mcp  ←── vscode-stubborn
                ↑          ↑                    ↑
             stubborn-demo ┘              stubborn-status (doctor aggregate)
```

## Naming conventions

| Pattern | Example | Use |
|---------|---------|-----|
| `stubborn` | core repo | Headless compiler / engine — short name for the main product |
| `stubborn-*` | `stubborn-mcp`, `stubborn-watch`, `stubborn-demo` | Program repos in the same org |
| `stubborn-status` | CLI `stubborn-status` | Federated doctor aggregation (not an IDE bridge) |
| `stubborn-stub` | PyPI package | Historical PyPI name for the core library |
| `stubborn-ingest-*` | `stubborn-ingest-db` | Optional future adapter packages beyond core OpenAPI ingest |

## Promotion workflow

```
lab-notes/ideas  →  stubborn ADR or hub doc  →  new repo + ROADMAP item
```

Do not create public repos for 💡 ideas until an ADR or hub decision record exists.
