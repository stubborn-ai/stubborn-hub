# AGENTS.md — Stubborn AI

Instructions for AI coding assistants (Cursor, etc.) in a **new session** with no prior chat history.

## Bootstrap (read first)

1. [docs/START-HERE.md](docs/START-HERE.md) — program map, repos, conventions
2. If user mentions recent work: private repo `lab-notes` → latest `journal/*.md` and `ideas/*.md`
3. Task-specific:
   - Core compiler / ingest / weave → [stubborn](https://github.com/stubborn-ai/stubborn) + its [ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md)
   - MCP / Cursor → [stubborn-mcp](https://github.com/stubborn-ai/stubborn-mcp)
   - Dev watch loop → [stubborn-watch](https://github.com/stubborn-ai/stubborn-watch)
   - Product positioning → [stubborn POSITIONING](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md)
   - How we build → [stubborn DEVELOPMENT-MODEL](https://github.com/stubborn-ai/stubborn/blob/main/docs/DEVELOPMENT-MODEL.md)

**Do not assume** you remember previous conversations. Use files in the workspace.

## Program summary

- **Goal:** Deterministic LLM context compiler for SCIP-indexed codebases (Java-first beta).
- **Public org:** https://github.com/stubborn-ai
- **PyPI:** `stubborn-stub` **0.9.0b4**, `stubborn-mcp` **0.1.0b1**
- **Deterministic deliverables:** Python — same SCIP + target + options → same stub.
- **AI role:** implement under architecture and boundary protocols; Stubborn does **not** call LLMs at runtime.

## Repository layout

| Path | Repo | Notes |
|------|------|-------|
| `stubborn-hub/` | public | Program docs — START-HERE, ARCHITECTURE, ROADMAP |
| `stubborn/` | public | Headless core — PyPI `stubborn-stub`, CLI `stubborn` |
| `stubborn-mcp/` | public | MCP server — PyPI `stubborn-mcp`, entry `stubborn-mcp` |
| `stubborn-watch/` | public | Dev orchestration — PyPI `stubborn-watch`, watch → merge |
| `stubborn-demo/` | public | Runnable demos and black-box validation projects |
| `lab-notes/` | **private** | Journals, ideas, ADR drafts — may contain WIP |

## Hard conventions

- User may chat in **Chinese**; **code comments, documentation, commit messages** → **English**.
- Do not commit secrets (`.env`, credentials).
- Only commit when the user explicitly asks.
- Public docs must not link to or expose private lab-notes content.
- Material pipeline changes → ADR in `stubborn/docs/adr/` before bulk implementation.

## Key technical decisions (already made)

| Topic | Decision |
|-------|----------|
| Machine index | SCIP via external indexers — [ADR-001](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-001-scip-as-machine-index.md) |
| Store | SQLite `symbols.db` — [ADR-002](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-002-sqlite-symbol-graph-ssot.md) |
| Beta scope | Java-first E2E — [ADR-007](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-007-java-first-beta-scope.md) |
| Agent surface | MCP in **stubborn-mcp** over `stubborn.api` — [ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md) |
| Incremental dev | `--merge` on path-scoped SCIP ingest — [ADR-009](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-009-incremental-index-merge.md) |
| Ecosystem | Weak coupling to anchor-migration — [INTEGRATION.md](docs/INTEGRATION.md) |
| Repos | Multi-repo under org; not a monorepo |

## Current status (2026-07-03)

- **Done:** ADR-009 `--merge` + schema v2; `stubborn-watch` scaffold; `stubborn-demo` created for runnable validation; `stubborn-stub` **0.9.0b4**; `stubborn-mcp` **0.1.0b1** on PyPI; ADR-001–009; Java E2E; program hub published
- **Next:** validate `stubborn-demo` E2E with JDK/Maven/scip-java; PyPI `0.9.0b5` / `stubborn-watch` release

## Typical tasks

| User ask | Where to work |
|----------|----------------|
| Ingest / store / merge | `stubborn/src/stubborn/store/`, `ingest/` |
| Prune / weave / formats | `stubborn/src/stubborn/graph/`, `weave/` |
| CLI / API | `stubborn/src/stubborn/cli.py`, `api.py` |
| MCP server | `stubborn-mcp/src/stubborn_mcp/` |
| File watch / merge orchestration | `stubborn-watch/src/stubborn_watch/` |
| Runnable demos / validation | `stubborn-demo/` |
| Program docs | `stubborn-hub/docs/` |
| Exploratory ideas | `lab-notes/ideas/` — promote to ADR when stable |

## Workspace

Open `stubborn-ai.code-workspace` — includes `stubborn-hub`, `stubborn`, `stubborn-mcp`, `stubborn-watch`, `stubborn-demo`, `lab-notes`.
