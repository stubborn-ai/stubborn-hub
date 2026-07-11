# Start here — Stubborn AI

Program map for humans and for onboarding AI in a new session. Read this file first, then follow links for depth.

## What this program is

**Stubborn AI** is a multi-repo program around **deterministic LLM context compilation** for code symbols and service contracts — **Java/Spring first** for code weave quality in beta.

Built with **architecture-led, AI-assisted development**:

- The **developer** defines architecture and boundary protocols (ADRs, schema, CLI/MCP contracts).
- **AI** implements most code under those contracts.
- **Shipped artifacts** are deterministic Python (same source graph + target + options → same context).

Public showcase: https://github.com/stubborn-ai

## PyPI packages (current)

| Package | Version | Role |
|---------|---------|------|
| [`stubborn-stub`](https://pypi.org/project/stubborn-stub/) | **0.9.0b6** | Core compiler — CLI `stubborn`, `stubborn.api`, code + contract graph |
| [`stubborn-mcp`](https://pypi.org/project/stubborn-mcp/) | **0.1.0b3** | MCP server — `workspace_info`, `list_symbols`, `list_contracts`, `get_context`, `metrics` |
| [`stubborn-watch`](https://pypi.org/project/stubborn-watch/) | **0.1.0b3** | Dev orchestration — file watch → SCIP indexer → merge |
| [`stubborn-status`](https://pypi.org/project/stubborn-status/) | **0.1.0b1** | Aggregate federated `doctor --json` for terminal, CI, and IDE bridges |

## Release matrix

| Package | Published version | Depends on |
|---------|-------------------|------------|
| `stubborn-stub` | `0.9.0b6` | Core compiler line |
| `stubborn-mcp` | `0.1.0b3` | `stubborn-stub>=0.9.0b6,<1.0` |
| `stubborn-watch` | `0.1.0b3` | `stubborn-stub>=0.9.0b6,<1.0` |
| `stubborn-status` | `0.1.0b1` | — (subprocess `doctor --json`; no `stubborn-stub` runtime dep) |

## Reading order (recommended)

| Step | Document | Why |
|------|----------|-----|
| 0 | [USER-JOURNEY.md](USER-JOURNEY.md) | **External users:** pick a path by goal (try / MCP / Java / contracts) |
| 1 | [stubborn DEVELOPMENT-MODEL](https://github.com/stubborn-ai/stubborn/blob/main/docs/DEVELOPMENT-MODEL.md) | Roles, deterministic core, boundary protocols |
| 2 | [ARCHITECTURE.md](ARCHITECTURE.md) | Layers, repo map, diagrams |
| 3 | [stubborn POSITIONING](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md) | Audience, honest scope, competitors |
| 4 | [stubborn ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md) | Design rationale (SCIP, workspace graph, contract graph, source-neutral queries) |
| 5 | [ECOSYSTEM.md](ECOSYSTEM.md) | Current and planned repositories |
| 6 | [ROADMAP.md](ROADMAP.md) | Near-term phases (lean) |
| 7 | [stubborn BETA](https://github.com/stubborn-ai/stubborn/blob/main/docs/BETA.md) | Beta checklist, KPI baselines |
| 8 | [stubborn ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md) | Federated `doctor` per package (onboarding without auto-orchestration) |
| 9 | [stubborn ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md) | `stubborn-status` — aggregate doctor JSON for terminal, CI, IDEs |
| 10 | [stubborn-mcp README](https://github.com/stubborn-ai/stubborn-mcp) | Cursor / agent setup |
| 11 | [INTEGRATION.md](INTEGRATION.md) | Optional anchor-migration consumer pattern |
| 12 | [DEMO-LAUNCHERS.md](DEMO-LAUNCHERS.md) | Explicit env/CLI contracts for all demo scripts |
| 13 | [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md) | Monolith vs microservices PetClinic proof model |
| 14 | [CONTRACT-GRAPH-PLAYBOOK.md](CONTRACT-GRAPH-PLAYBOOK.md) | OpenAPI + manifest ingest and mixed-workspace queries |
| 15 | [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) | Coordinated PyPI release runbook |
| 16 | [stubborn TROUBLESHOOTING](https://github.com/stubborn-ai/stubborn/blob/main/docs/TROUBLESHOOTING.md) | Common setup failures and copy-paste fixes |

**Private (if you have access):** `lab-notes/journal/` — latest session log and ecosystem ideas.

## Repository map

| Repo | Visibility | Role | Status |
|------|------------|------|--------|
| **stubborn-hub** | public | Program docs (this repo) | ✅ Active |
| **stubborn** | public | Headless core — code/contract ingest, store, prune, weave, CLI, API | **Beta** (`0.9.0b6` on PyPI) |
| **stubborn-mcp** | public | Source-neutral MCP stdio server | **Beta** (`0.1.0b3` on PyPI) |
| **stubborn-watch** | public | Dev orchestration: watch → SCIP indexer → merge | **Beta** (`0.1.0b3` on PyPI) |
| **stubborn-status** | public | Federated `doctor` aggregation CLI | **Beta** (`0.1.0b1` on PyPI) |
| **stubborn-demo** | public | Runnable demos + black-box validation projects | ✅ Active |
| **vscode-stubborn** | public | VS Code bridge for MCP setup + sidecar stubs | 📋 Planned |
| **lab-notes** | **private** | Journals, ADR drafts, lab ideas | ✅ Active |
| **.github** | public | Org profile README | ✅ Active |

Product ADRs live in **`stubborn/docs/adr/`** until a cross-cutting decision needs a hub-level ADR.

## Execution tiers

The public strategy is intentionally simple:

| Tier | Default for | What it runs | Notes |
|------|-------------|--------------|-------|
| Docker | Most users, CI, cross-platform reproducibility | `docker compose build`, `docker compose run --rm ...` | Canonical environment on Windows, Linux, and macOS |
| WSL/bash | Contributors doing fast local checks on Unix-like shells | Bash host scripts under `stubborn-demo/**/scripts/*.sh` | Preferred local quick-test path on WSL2, Linux, and macOS |
| PowerShell fallback | Windows host users who cannot or do not want to use WSL | Thin `pwsh` wrappers, or the historical `*.ps1` scripts recoverable from git history | Keep this path as a fallback only; do not duplicate core logic here |

Where a repo ships bash wrappers today, those wrappers are the source of truth. Any PowerShell entrypoint should stay thin and call the same underlying targets.

Host/bash launchers now expect the required Python packages in the active
environment and explicit roots like `BANK_ROOT` or per-demo `upstream/`
directories; they no longer chase sibling source trees or private `PYTHONPATH`
conventions.

### Validation matrix

| Tier | Canonical command shape | Expected result |
|------|-------------------------|-----------------|
| Docker | `docker compose build` → `docker compose run --rm e2e` | Same artifact shape across Windows, Linux, and macOS |
| WSL/bash | `./scripts/run-e2e.sh` or `./scripts/run-merge-e2e.sh` | Fast local validation with the same assertions as Docker |
| PowerShell fallback | Historical `*.ps1` launcher or thin wrapper to the same target | Windows host fallback only; do not fork behavior or assertions |

## Local workspace (author machine)

```
C:\github\stubborn-ai\
├── stubborn-hub/
├── stubborn/
├── stubborn-mcp/
├── stubborn-watch/
├── stubborn-status/
├── stubborn-demo/
├── vscode-stubborn/
├── lab-notes/              private
└── stubborn-ai.code-workspace
```

## Pipeline (one picture)

```
scip-java / scip-*  →  stubborn index        ┐
OpenAPI specs       →  stubborn index-openapi ├→ symbols.db
explicit contracts  →  stubborn index-contract┘
                                      ↓
                    source-neutral prune + weave
                    (java-stub | stubborn-dsl)
                                      ↓
              CLI / stubborn.api / stubborn-mcp → LLM / Agent
```

Dev loop: `stubborn-watch` → indexer → `stubborn index --merge` → same `symbols.db`.
Contract path: OpenAPI/manifest → v4 contract tables → endpoint/schema context and evidence-tiered bindings in the same workspace view.

Full diagrams: [ARCHITECTURE.md](ARCHITECTURE.md).

## Validation entrypoints

Use the repo that owns the contract you want to prove. Full launcher contracts:
[DEMO-LAUNCHERS.md](DEMO-LAUNCHERS.md). PetClinic code + contract evidence:
[PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md).

| Scope | Canonical entrypoint | Owner |
|-------|----------------------|-------|
| ADR-009 merge contract | `stubborn-demo/demo-spring/scripts/run-merge-e2e.sh` | `stubborn-demo` |
| Multi-repo workspace graph | `stubborn-demo/multi-repo/scripts/run-e2e.sh` | `stubborn-demo` |
| PetClinic monolith scale-up | `stubborn-demo/spring-petclinic/scripts/run-e2e.sh` | `stubborn-demo` |
| PetClinic MS + contract bridge | `stubborn-demo/spring-petclinic-microservices/scripts/run-e2e.sh` | `stubborn-demo` |
| Contract graph minimal (fixtures) | `stubborn-demo/contract-graph-minimal/scripts/run-e2e.sh` | `stubborn-demo` |
| PetClinic MS MCP smoke | `stubborn-demo/spring-petclinic-microservices/scripts/mcp-smoke.sh` | `stubborn-mcp` + `stubborn-demo` |
| Watch / orchestration smoke | `stubborn-watch/tests/test_watch.py` | `stubborn-watch` |
| MCP surface smoke over prepared `symbols.db` | `stubborn-demo/demo-spring/scripts/mcp-smoke.sh` | `stubborn-mcp` + `stubborn-demo` assets |
| Federated doctor (per package) | `stubborn doctor`, `stubborn-mcp doctor`, `stubborn-watch doctor` | `stubborn`, `stubborn-mcp`, `stubborn-watch` |
| Doctor aggregation | `stubborn-status --json` | `stubborn-status` |
| Release matrix consistency | `stubborn-hub/scripts/check_release_matrix.py --pypi` | `stubborn-hub` — [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) |

## What is verified today

| Capability | Status |
|------------|--------|
| SCIP ingest → SQLite (`stubborn index`) | ✅ |
| OpenAPI endpoint/schema ingest (`stubborn index-openapi`) | ✅ |
| Explicit contract evidence ingest (`stubborn index-contract`) | ✅ |
| Source-neutral endpoint context (`openapi ...` targets) | ✅ |
| Prune + weave + token budget | ✅ |
| MCP code + contract tools via **stubborn-mcp** | ✅ |
| Multi-repo workspace composition | ✅ via `stubborn-demo/multi-repo` |
| PetClinic monolith + MS contract evidence | ✅ via `stubborn-demo/spring-petclinic*` |
| Contract graph minimal mixed workspace | ✅ via `stubborn-demo/contract-graph-minimal` |
| `stubborn diff` / PR symbol-diff workflow | ✅ |
| Incremental `--merge` (ADR-009) | ✅ |
| demo-spring save → merge → `list_symbols` host runbook | ✅ |
| `stubborn-watch` | ✅ PyPI beta + CLI smoke |
| Federated `doctor` (ADR-015) | ✅ `stubborn`, `stubborn-mcp`, `stubborn-watch` |
| `stubborn-status` aggregation (ADR-016) | ✅ PyPI `0.1.0b1` |

## Conventions (do not forget)

| Topic | Rule |
|-------|------|
| Chat with AI | Chinese is fine |
| Code comments, docs, commits | **English** |
| Machine index | SCIP for code symbols; OpenAPI for REST contracts; optional future ingest adapters are opt-in |
| Public vs draft | Stabilized docs → `stubborn-hub` or `stubborn`; raw thinking → `lab-notes` |
| Commits | Only when the user explicitly asks |

## Next work (priority)

1. ~~Milestone release checklist wired to `check_release_matrix.py`~~ → [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)
2. Charter `stubborn-onboard` (separate ADR candidate) for scip-java orchestration
3. `vscode-stubborn` doctor panel consuming `stubborn-status --json`

See **[AGENTS.md](../AGENTS.md)** for AI session bootstrap.

When the user says “continue Stubborn AI”, read in order:

1. This file
2. `AGENTS.md`
3. Latest `lab-notes/journal/*.md` (if available)
4. [stubborn CHANGELOG](https://github.com/stubborn-ai/stubborn/blob/main/CHANGELOG.md) for product releases

Do **not** assume chat history from prior sessions exists.
