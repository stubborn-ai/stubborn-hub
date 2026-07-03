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
| [`stubborn-watch`](https://pypi.org/project/stubborn-watch/) | **0.1.0b1** | Dev orchestration — file watch → SCIP indexer → merge |

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
| **stubborn** | public | Headless core — ingest, store, prune, weave, CLI, API | **Beta** (`0.9.0b4` on PyPI) |
| **stubborn-mcp** | public | MCP stdio server | **Beta** (`0.1.0b1` on PyPI) |
| **stubborn-watch** | public | Dev orchestration: watch → SCIP indexer → merge | **Beta** (`0.1.0b1` on PyPI) |
| **stubborn-demo** | public | Runnable demos + black-box validation projects | ✅ Active |
| **vscode-stubborn** | public | VS Code bridge for MCP setup + sidecar stubs | 📋 Planned |
| **lab-notes** | **private** | Journals, ADR drafts, lab ideas | ✅ Active |
| **.github** | public | Org profile README | ✅ Active |

Product ADRs live in **`stubborn/docs/adr/`** until a cross-cutting decision needs a hub-level ADR.

## Local workspace (author machine)

```
C:\github\stubborn-ai\
├── stubborn-hub/
├── stubborn/
├── stubborn-mcp/
├── stubborn-watch/
├── stubborn-demo/
├── vscode-stubborn/
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

Dev loop: `stubborn-watch` → indexer → `stubborn index --merge` → same `symbols.db`.

Full diagrams: [ARCHITECTURE.md](ARCHITECTURE.md).

## Validation entrypoints

Use the repo that owns the contract you want to prove:

| Scope | Canonical entrypoint | Owner |
|-------|----------------------|-------|
| ADR-009 merge contract | `stubborn-demo/demo-spring/scripts/run-merge-e2e.ps1` | `stubborn-demo` |
| Watch / orchestration smoke | `stubborn-watch/tests/test_watch.py` | `stubborn-watch` |
| MCP surface smoke over prepared `symbols.db` | `stubborn-demo/demo-spring/scripts/mcp-smoke.ps1` | `stubborn-mcp` + `stubborn-demo` assets |

## What is verified today

| Capability | Status |
|------------|--------|
| SCIP ingest → SQLite (`stubborn index`) | ✅ |
| Prune + weave + token budget | ✅ |
| MCP tools via **stubborn-mcp** on PyPI | ✅ |
| Java E2E (demo-spring, petclinic, dukesbank) | ✅ via `stubborn-demo` |
| `stubborn diff` / PR symbol-diff workflow | ✅ |
| Incremental `--merge` (ADR-009) | ✅ |
| demo-spring save → merge → `list_symbols` host runbook | ✅ |
| `stubborn-watch` | ✅ PyPI beta + CLI smoke |

## Conventions (do not forget)

| Topic | Rule |
|-------|------|
| Chat with AI | Chinese is fine |
| Code comments, docs, commits | **English** |
| Machine index | SCIP (canonical); optional future ingest adapters are opt-in |
| Public vs draft | Stabilized docs → `stubborn-hub` or `stubborn`; raw thinking → `lab-notes` |
| Commits | Only when the user explicitly asks |

## Next work (priority)

1. Validate `stubborn-demo` host E2E on a machine with JDK/Maven/scip-java
2. Add Docker / CI path for demo-spring merge E2E in `stubborn-demo`
3. PyPI release `stubborn-stub` `0.9.0b5`

See **[AGENTS.md](../AGENTS.md)** for AI session bootstrap.

When the user says “continue Stubborn AI”, read in order:

1. This file
2. `AGENTS.md`
3. Latest `lab-notes/journal/*.md` (if available)
4. [stubborn CHANGELOG](https://github.com/stubborn-ai/stubborn/blob/main/CHANGELOG.md) for product releases

Do **not** assume chat history from prior sessions exists.
