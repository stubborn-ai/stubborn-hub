# AGENTS.md — Stubborn AI

Instructions for AI coding assistants (Cursor, etc.) in a **new session** with no prior chat history.

## Bootstrap (read first)

1. [docs/START-HERE.md](docs/START-HERE.md) — program map, repos, conventions
2. If user mentions recent work: private repo `lab-notes` → latest `journal/*.md` and `ideas/*.md`
3. Task-specific:
   - Core compiler / ingest / weave → [stubborn](https://github.com/stubborn-ai/stubborn) + its [ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md)
   - MCP / Cursor → [stubborn-mcp](https://github.com/stubborn-ai/stubborn-mcp)
   - Dev watch loop → [stubborn-watch](https://github.com/stubborn-ai/stubborn-watch)
   - Doctor aggregation → [stubborn-status](https://github.com/stubborn-ai/stubborn-status)
   - Product positioning → [stubborn POSITIONING](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md)
   - How we build → [stubborn DEVELOPMENT-MODEL](https://github.com/stubborn-ai/stubborn/blob/main/docs/DEVELOPMENT-MODEL.md)

**Do not assume** you remember previous conversations. Use files in the workspace.

## Program summary

- **Goal:** Deterministic LLM context compiler for code symbols and service contracts (Java-first beta for code weave quality).
- **Public org:** https://github.com/stubborn-ai
- **PyPI:** `stubborn-stub` **0.10.0b1**, `stubborn-mcp` **0.10.0b1**, `stubborn-watch` **0.10.0b1**, `stubborn-status` **0.10.0b1**
- **Deterministic deliverables:** Python — same source graph + target + options → same context.
- **AI role:** implement under architecture and boundary protocols; Stubborn does **not** call LLMs at runtime.

## Repository layout

| Path | Repo | Notes |
|------|------|-------|
| `stubborn-hub/` | public | Program docs — START-HERE, ARCHITECTURE, ROADMAP |
| `stubborn/` | public | Headless core — PyPI `stubborn-stub`, CLI `stubborn` |
| `stubborn-mcp/` | public | MCP server — PyPI `stubborn-mcp`, entry `stubborn-mcp` |
| `stubborn-watch/` | public | Dev orchestration — PyPI `stubborn-watch`, watch → merge |
| `stubborn-status/` | public | Doctor aggregation — CLI `stubborn-status`, subprocess `doctor --json` |
| `stubborn-demo/` | public | Runnable demos and black-box validation projects |
| `lab-notes/` | **private** | Journals, ideas, ADR drafts — may contain WIP |

## Hard conventions

- User may chat in **Chinese**; **code comments, documentation, commit messages** → **English**.
- Do not commit secrets (`.env`, credentials).
- Only commit when the user explicitly asks.
- Public docs must not link to or expose private lab-notes content.
- Material pipeline changes → ADR in `stubborn/docs/adr/` before bulk implementation.
- Major or release-worthy changes should bump at least the next minor version step
  rather than a patch-only bump, e.g. `0.1.0 -> 0.2.0`.

## Key technical decisions (already made)

| Topic | Decision |
|-------|----------|
| Code-symbol index | SCIP via external indexers — [ADR-001](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-001-scip-as-machine-index.md) |
| Contract index | OpenAPI/explicit manifests as contract graph facts — [ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md), [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) |
| Store | SQLite `symbols.db` with code + contract facts — [ADR-002](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-002-sqlite-symbol-graph-ssot.md), [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) |
| Query model | Source-neutral code/contract targets — [ADR-013](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-013-source-neutral-contract-queries.md) |
| Packaging | SCIP protobuf runtime is optional via `stubborn-stub[scip]` — [ADR-014](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-014-optional-scip-protobuf-runtime.md) |
| Beta scope | Java-first E2E — [ADR-007](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-007-java-first-beta-scope.md) |
| Agent surface | MCP in **stubborn-mcp** over `stubborn.api` — [ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md) |
| Incremental dev | `--merge` on path-scoped SCIP ingest — [ADR-009](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-009-incremental-index-merge.md) |
| Ecosystem | Weak coupling to anchor-migration — [INTEGRATION.md](docs/INTEGRATION.md) |
| Repos | Multi-repo under org; not a monorepo |
| Release docs | Hub `README.md` release matrix is canonical; verify with `python3 scripts/check_release_matrix.py --pypi` from `stubborn-hub/`; runbook: [RELEASE-CHECKLIST.md](docs/RELEASE-CHECKLIST.md) |

## Current status (2026-07-09)

- **Done:** schema v4 contract evidence; `index-contract`; `index-openapi`; source-neutral endpoint queries; optional SCIP protobuf runtime; `stubborn-watch` **0.10.0b1**; `stubborn-stub` **0.10.0b1**; `stubborn-mcp` **0.10.0b1** with contract tools; Java E2E; program hub published; demo launcher contracts; PetClinic validation model; federated `doctor` per [ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md) (`stubborn`, `stubborn-mcp`, `stubborn-watch`); [stubborn-status](https://github.com/stubborn-ai/stubborn-status) **0.10.0b1** on PyPI per [ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md)
- **Next:** coordinated beta release; `vscode-stubborn` doctor panel

## Typical tasks

| User ask | Where to work |
|----------|----------------|
| Ingest / store / merge | `stubborn/src/stubborn/store/`, `ingest/` |
| Contract graph / OpenAPI | `stubborn/src/stubborn/ingest/openapi.py`, `ingest/contracts.py`, `store/`, `graph/prune.py` |
| Prune / weave / formats | `stubborn/src/stubborn/graph/`, `weave/` |
| CLI / API | `stubborn/src/stubborn/cli.py`, `api.py` |
| MCP server | `stubborn-mcp/src/stubborn_mcp/` |
| File watch / merge orchestration | `stubborn-watch/src/stubborn_watch/` |
| Doctor aggregation | `stubborn-status/src/stubborn_status/` |
| Runnable demos / validation | `stubborn-demo/` + [DEMO-LAUNCHERS.md](docs/DEMO-LAUNCHERS.md), [PETCLINIC-VALIDATION.md](docs/PETCLINIC-VALIDATION.md) |
| Program docs | `stubborn-hub/docs/` |
| Exploratory ideas | `lab-notes/ideas/` — promote to ADR when stable |

## Workspace

Open `stubborn-ai.code-workspace` — includes `stubborn-hub`, `stubborn`, `stubborn-mcp`, `stubborn-watch`, `stubborn-status`, `stubborn-demo`, `lab-notes`.
