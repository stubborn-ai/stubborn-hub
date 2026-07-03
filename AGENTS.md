# AGENTS.md — Stubborn AI

Instructions for AI coding assistants (Cursor, etc.) in a **new session** with no prior chat history.

## Bootstrap (read first)

1. [docs/START-HERE.md](docs/START-HERE.md) — program map, repos, conventions
2. If user mentions recent work: private repo `stubborn-ai-lab-notes` → latest `journal/*.md` and `ideas/*.md`
3. Task-specific:
   - Core compiler / ingest / weave → [stubborn](https://github.com/stubborn-ai/stubborn) + its [ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md)
   - Product positioning → [stubborn POSITIONING](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md)
   - How we build → [stubborn DEVELOPMENT-MODEL](https://github.com/stubborn-ai/stubborn/blob/main/docs/DEVELOPMENT-MODEL.md)

**Do not assume** you remember previous conversations. Use files in the workspace.

## Program summary

- **Goal:** Deterministic LLM context compiler for SCIP-indexed codebases (Java-first beta).
- **Public org:** https://github.com/stubborn-ai
- **Deterministic deliverables:** Python (`stubborn-stub`) — same SCIP + target + options → same stub.
- **AI role:** implement under architecture and boundary protocols; Stubborn does **not** call LLMs at runtime.

## Repository layout

| Path | Repo | Notes |
|------|------|-------|
| `stubborn-hub/` | public | Program docs — START-HERE, ARCHITECTURE, ROADMAP |
| `stubborn/` | public | Core compiler — PyPI `stubborn-stub`, CLI `stubborn` |
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
| Agent surface | MCP over `stubborn.api` — [ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md); split to `stubborn-mcp` planned |
| Incremental dev | `--merge` on path-scoped SCIP ingest — [ADR-009](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-009-incremental-index-merge.md) |
| Ecosystem | Weak coupling to anchor-migration — [INTEGRATION.md](docs/INTEGRATION.md) |
| Repos | Multi-repo under org; not a monorepo |

## Current status (update via journal if stale)

- **Done:** `stubborn` Beta `0.9.0b3`; ADR-001–009; Java E2E; MCP in-core
- **Next:** ADR-009 implementation; `stubborn-mcp` split; `stubborn-watch`; publish `stubborn-hub`

## Typical tasks

| User ask | Where to work |
|----------|----------------|
| Ingest / store / merge | `stubborn/src/stubborn/store/`, `ingest/` |
| Prune / weave / formats | `stubborn/src/stubborn/graph/`, `weave/` |
| CLI / API | `stubborn/src/stubborn/cli.py`, `api.py` |
| MCP server | `stubborn/src/stubborn/mcp_server/` → future `stubborn-mcp` |
| Program docs | `stubborn-hub/docs/` |
| Exploratory ideas | `lab-notes/ideas/` — promote to ADR when stable |

## Workspace

Open `stubborn-ai.code-workspace` at the parent of `stubborn-hub` and `stubborn`.
