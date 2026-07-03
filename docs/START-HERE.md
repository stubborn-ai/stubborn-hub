# Start here — Stubborn AI

Program map for humans and for onboarding AI in a new session. Read this file first, then follow links for depth.

## What this program is

**Stubborn AI** is a multi-repo program around **deterministic LLM context compilation** for SCIP-indexed codebases — **Java/Spring first** in beta.

Built with **architecture-led, AI-assisted development**:

- The **developer** defines architecture and boundary protocols (ADRs, schema, CLI/MCP contracts).
- **AI** implements most code under those contracts.
- **Shipped artifacts** are deterministic Python (same SCIP + target + options → same stub).

Public showcase: https://github.com/stubborn-ai

## PyPI packages (current)

| Package | Version | Role |
|---------|---------|------|
| [`stubborn-stub`](https://pypi.org/project/stubborn-stub/) | **0.9.0b4** | Core compiler — CLI `stubborn`, `stubborn.api` |
| [`stubborn-mcp`](https://pypi.org/project/stubborn-mcp/) | **0.1.0b1** | MCP server — `get_context`, `list_symbols`, `metrics` |

## Reading order (recommended)

| Step | Document | Why |
|------|----------|-----|
| 1 | [stubborn DEVELOPMENT-MODEL](https://github.com/stubborn-ai/stubborn/blob/main/docs/DEVELOPMENT-MODEL.md) | Roles, deterministic core, boundary protocols |
| 2 | [ARCHITECTURE.md](ARCHITECTURE.md) | Layers, repo map, diagrams |
| 3 | [stubborn POSITIONING](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md) | Audience, honest scope, competitors |
| 4 | [stubborn ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md) | Design rationale (ADR-001–009 in `stubborn`) |
| 5 | [ECOSYSTEM.md](ECOSYSTEM.md) | Current and planned repositories |
| 6 | [ROADMAP.md](ROADMAP.md) | Near-term phases (lean) |
| 7 | [stubborn BETA](https://github.com/stubborn-ai/stubborn/blob/main/docs/BETA.md) | Beta checklist, KPI baselines |
| 8 | [stubborn-mcp README](https://github.com/stubborn-ai/stubborn-mcp) | Cursor / agent setup |
| 9 | [INTEGRATION.md](INTEGRATION.md) | Optional anchor-migration consumer pattern |

**Private (if you have access):** `lab-notes/journal/` — latest session log and ecosystem ideas.

## Repository map

| Repo | Visibility | Role | Status |
|------|------------|------|--------|
| **stubborn-hub** | public | Program docs (this repo) | ✅ Active |
| **stubborn** | public | Core compiler — ingest, store, prune, weave, CLI, API | **Beta** (`0.9.0b4` on PyPI) |
| **stubborn-mcp** | public | MCP stdio server | **Beta** (`0.1.0b1` on PyPI) |
| **stubborn-watch** | public | Dev orchestration: watch → SCIP indexer → merge | 📋 Planned |
| **lab-notes** | **private** | Journals, ADR drafts, lab ideas | ✅ Active |
| **.github** | public | Org profile README | ✅ Active |

Product ADRs live in **`stubborn/docs/adr/`** until a cross-cutting decision needs a hub-level ADR.

## Local workspace (author machine)

```
C:\github\stubborn-ai\
├── stubborn-hub/
├── stubborn/
├── stubborn-mcp/
├── lab-notes/              private
└── stubborn-ai.code-workspace
```

## Pipeline (one picture)

```
scip-java / scip-*  →  stubborn index  →  symbols.db
                              ↓
                    prune + weave (java-stub | stubborn-dsl)
                              ↓
              CLI / stubborn.api / stubborn-mcp → LLM / Agent
```

Dev loop (planned): `stubborn-watch` → indexer → `stubborn index --merge` → same `symbols.db`.

Full diagrams: [ARCHITECTURE.md](ARCHITECTURE.md).

## What is verified today

| Capability | Status |
|------------|--------|
| SCIP ingest → SQLite (`stubborn index`) | ✅ |
| Prune + weave + token budget | ✅ |
| MCP tools via **stubborn-mcp** on PyPI | ✅ |
| Java E2E (demo-spring, petclinic, dukesbank) | ✅ |
| `stubborn diff` / PR symbol-diff workflow | ✅ |
| Incremental `--merge` (ADR-009) | 📋 ADR accepted; not implemented |
| `stubborn-watch` | 📋 Planned |

## Conventions (do not forget)

| Topic | Rule |
|-------|------|
| Chat with AI | Chinese is fine |
| Code comments, docs, commits | **English** |
| Machine index | SCIP (canonical); optional future ingest adapters are opt-in |
| Public vs draft | Stabilized docs → `stubborn-hub` or `stubborn`; raw thinking → `lab-notes` |
| Commits | Only when the user explicitly asks |

## Next work (priority)

1. **stubborn** — implement ADR-009 (`--merge`, schema v2, `relative_path`)
2. **stubborn-watch** — Java save → scip-java → merge
3. Real-project validation runbook

See **[AGENTS.md](../AGENTS.md)** for AI session bootstrap.

When the user says “continue Stubborn AI”, read in order:

1. This file
2. `AGENTS.md`
3. Latest `lab-notes/journal/*.md` (if available)
4. [stubborn CHANGELOG](https://github.com/stubborn-ai/stubborn/blob/main/CHANGELOG.md) for product releases

Do **not** assume chat history from prior sessions exists.
