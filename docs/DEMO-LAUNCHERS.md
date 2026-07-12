# Demo launcher contracts

Canonical index of **explicit inputs** for `stubborn-demo` validation scripts.

Host/bash launchers do not create virtual environments, chase sibling source trees,
or set undocumented `PYTHONPATH` fallbacks. Docker is the canonical cross-platform
path; bash wrappers are the fast local path on Unix-like shells.

CI enforces part of this contract in
[`stubborn-demo/.github/workflows/script-contract-guard.yml`](https://github.com/stubborn-ai/stubborn-demo/blob/main/.github/workflows/script-contract-guard.yml)
(syntax checks, `BANK_ROOT` failure mode, hidden-fallback grep, multi-repo unit
tests). This document is the human-readable companion.

## Execution tiers

| Tier | When to use | Entry shape |
|------|-------------|-------------|
| **Docker** | CI, reproducibility, Windows/macOS without local toolchain | `docker compose build toolchain` → `docker compose run --rm <service>` |
| **WSL/bash** | Fast local checks on Linux, macOS, WSL2 | `./scripts/run-e2e.sh` under each demo |
| **PowerShell** | Windows fallback only | Thin wrapper to the same target; do not fork assertions |

## Environment variables

| Variable | Required? | Default (Docker) | Used by |
|----------|-----------|------------------|---------|
| `BANK_ROOT` | **Yes on host** for dukesbank | `/bank` (compose mount) | `dukesbank/scripts/run-e2e.sh` |
| `STUBBORN_CMD` | No | `stubborn` | `scripts/verify_multi_repo_workspace.py` |
| `DEMO_ROOT` | No | `/demo` in Docker | `demo-spring` E2E scripts |
| `EXAMPLE_ROOT` | No | `/opt/stubborn-demo/<demo>` | Docker petclinic, petclinic-ms, dukesbank |
| `PETCLINIC_ROOT` | No | `/petclinic` | Docker petclinic E2E |
| `PETCLINIC_MS_ROOT` | No | `/petclinic-ms` | Docker petclinic-ms E2E |
| `PETCLINIC_TARGET` | No | `VetController` | Docker petclinic E2E |
| `STUBBORN_DB` | Set by MCP smoke scripts | — | `*/mcp-smoke.sh` (convention for MCP tools) |

There is **no** `JAVA_ROOT` environment variable. The monolith PetClinic verifier
takes an explicit CLI flag: `--java-root` on `verify_petclinic_context.py`.

## Host PATH / install requirements

| Command / package | Required by |
|-------------------|-------------|
| `docker`, `docker compose` | Docker tier |
| `bash` | All `.sh` launchers |
| `mvn`, `scip-java` | demo-spring, petclinic, petclinic-ms, dukesbank |
| `stubborn` CLI (`stubborn-stub`) | All E2E except MCP smoke alone |
| `stubborn-stub[openapi]` | `contract-graph-minimal` (OpenAPI ingest) |
| `python3` | All launchers |
| `git` | petclinic, petclinic-ms (clone pinned upstream) |
| `stubborn-mcp` | `demo-spring/scripts/mcp-smoke.sh`, `spring-petclinic-microservices/scripts/mcp-smoke.sh` |
| JDK 21+ | Documented prerequisite for host runs |

## Docker Compose services

| Service | Container entrypoint | Host equivalent |
|---------|---------------------|-----------------|
| `e2e` | `docker/run-e2e.sh` | `demo-spring/scripts/run-e2e.sh` |
| `merge-e2e` | `docker/run-merge-e2e.sh` | `demo-spring/scripts/run-merge-e2e.sh` |
| `multi-repo-e2e` | `scripts/verify_multi_repo_workspace.py` | `multi-repo/scripts/run-e2e.sh` |
| `contract-graph-e2e` | `scripts/verify_contract_graph_minimal.py` | `contract-graph-minimal/scripts/run-e2e.sh` |
| `petclinic-e2e` | `docker/run-petclinic-e2e.sh` | `spring-petclinic/scripts/run-e2e.sh` |
| `petclinic-ms-e2e` | `docker/run-petclinic-ms-e2e.sh` | `spring-petclinic-microservices/scripts/run-e2e.sh` |
| `dukesbank-e2e` | `docker/run-dukesbank-e2e.sh` | `dukesbank/scripts/run-e2e.sh` |
| `shell` | interactive bash | — |
| `cli` | arbitrary `stubborn` CLI | — |

Image build arg `STUBBORN_SPEC` defaults to
`git+https://github.com/stubborn-ai/stubborn.git`. Compose pins
`SCIP_JAVA_VERSION: "0.12.3"`.

## Launcher matrix

### demo-spring

| Field | Host `demo-spring/scripts/run-e2e.sh` | Docker `e2e` |
|-------|--------------------------------------|--------------|
| Env | `DEMO_ROOT` optional | `DEMO_ROOT` → `/demo` |
| PATH | `mvn`, `scip-java`, `stubborn`, `python3` | same (image) |
| Proves | SCIP → SQLite → `OrderService` context | same + `stubborn metrics` |

| Field | Host `demo-spring/scripts/run-merge-e2e.sh` | Docker `merge-e2e` |
|-------|---------------------------------------------|-------------------|
| Env | `DEMO_ROOT` optional | `DEMO_ROOT` → `/demo` |
| Python | imports `stubborn.store.reader`, `stubborn.store.writer` | same |
| Proves | ADR-009 incremental `stubborn index --merge --paths` — probe symbol appears, `OrderService` preserved, stable `index_run_id`, `mode=merged` | same |

| Field | `demo-spring/scripts/mcp-smoke.sh` |
|-------|-------------------------------------|
| Precondition | `metadata/symbols.db` exists (run E2E first) |
| Packages | `stubborn-mcp` |
| Proves | `workspace_info`, `list_contracts`, `list_symbols`, `get_context`, `metrics` |

### multi-repo

| Field | `multi-repo/scripts/run-e2e.sh` → `scripts/verify_multi_repo_workspace.py` |
|-------|-------------------------------------------------------------------------------|
| Env | `STUBBORN_CMD` optional |
| PATH | `python3`, `stubborn` |
| Proves | Jar-only `repo-a` context has `Service`, not `Helper`; merged fixture crosses into `Helper`; reverse context at `Service#` is one-way |

See [multi-repo/README.md](https://github.com/stubborn-ai/stubborn-demo/blob/main/multi-repo/README.md)
for the combined-fixture rationale.

### contract-graph-minimal

| Field | `contract-graph-minimal/scripts/run-e2e.sh` → `scripts/verify_contract_graph_minimal.py` |
|-------|---------------------------------------------------------------------------------------------|
| Env | `STUBBORN_CMD` optional |
| PATH | `python3`, `stubborn`; install `stubborn-stub[openapi]` |
| Proves | Workspace with 2 code repos + OpenAPI + manifest bindings; `list-contracts`; endpoint + provider `context` |

Playbook: [CONTRACT-GRAPH-PLAYBOOK.md](CONTRACT-GRAPH-PLAYBOOK.md).

### spring-petclinic (monolith)

| Field | Host `spring-petclinic/scripts/run-e2e.sh` | Docker `petclinic-e2e` |
|-------|-------------------------------------------|------------------------|
| Env | none | `PETCLINIC_ROOT`, `EXAMPLE_ROOT`, `PETCLINIC_TARGET` |
| Filesystem | clones pinned upstream to `upstream/` | clones to `/petclinic` |
| PATH | `git`, `mvn`, `scip-java`, `stubborn`, `python3` | same |
| Follow-up verifier | `verify_petclinic_context.py --java-root <upstream>/src/main/java` | same |
| Proves | Scale-up SCIP graph, VetController neighbors, ≥70% token savings | same |

Details: [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md).

### spring-petclinic-microservices

| Field | Host `spring-petclinic-microservices/scripts/run-e2e.sh` | Docker `petclinic-ms-e2e` |
|-------|--------------------------------------------------------|---------------------------|
| Env | none | `PETCLINIC_MS_ROOT`, `EXAMPLE_ROOT` |
| Filesystem | clones pinned upstream to `upstream/` | clones to `/petclinic-ms` |
| Stages | per-service SCIP → workspace index → baseline verify → `index-contract` → bridged verify → emit stubs | same |
| Follow-up | `scripts/mcp-smoke.sh` (requires prior E2E + `stubborn-mcp`) | manual on host |
| Proves | Multi-repo workspace graph + schema v4 HTTP contract bridge | same |

Details: [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md).

### dukesbank

| Field | Host `dukesbank/scripts/run-e2e.sh` | Docker `dukesbank-e2e` |
|-------|-------------------------------------|------------------------|
| Env | **`BANK_ROOT` required** (existing directory) | `BANK_ROOT` → `/bank` (compose mount) |
| PATH | `mvn`, `scip-java`, `stubborn`, `python3` | same |
| Optional follow-up | `python3 scripts/verify_dukesbank_context.py` (not invoked by launcher) | not run in Docker |
| Proves | Legacy Java EE module → `java-stub` + `stubborn-dsl` for `AccountControllerBean` | indexing + context emission |

## Python verifier helpers

These are not top-level launchers unless noted.

| Script | Invoked by | Required input | Proves |
|--------|-----------|----------------|--------|
| `verify_multi_repo_workspace.py` | multi-repo E2E | `STUBBORN_CMD` optional | Cross-repo graph composition |
| `verify_petclinic_context.py` | petclinic E2E | `--java-root` (required) | VetController neighbor types + compression floor |
| `verify_petclinic_ms_workspace.py` | petclinic-ms E2E | `--db`, `--mode baseline\|bridged\|emit-stubs` | Workspace repos, HTTP boundary, v4 contract bindings |
| `verify_dukesbank_context.py` | manual | prepared `metadata/symbols.db` | `AccountControllerBean` neighbor types |
| `resolve_symbol.py` | petclinic, dukesbank E2E | `db_path`, `--display-name` | SCIP `stable_id` resolution |
| `multi_repo_workspace.py` | imported + unit tests | — | Fixture merge logic (not a launcher) |

## CI workflow mapping

| Workflow | Triggers | What it runs |
|----------|----------|--------------|
| `script-contract-guard` | push/PR `main` | bash `-n`, `py_compile`, multi-repo unittest, `BANK_ROOT` guard, hidden-fallback grep |
| `demo-spring-e2e` | push/PR `main`, schedule | Docker `e2e`, `merge-e2e`, `multi-repo-e2e` |
| `petclinic-e2e` | schedule, `workflow_dispatch` | Docker `petclinic-e2e` |
| `petclinic-ms-e2e` | schedule, `workflow_dispatch` | Docker `petclinic-ms-e2e` |

PetClinic workflows are intentionally **not** on every PR — they are heavier and
pinned to upstream commits.

## Setup diagnostics (ADR-015 / ADR-016)

Each package owns a read-only `doctor` command with a narrow custody scope.
Inspecting `symbols.db` does **not** migrate schema — legacy versions warn and
recommend re-index. For a **single terminal or CI view**, use **`stubborn-status`**
to aggregate `doctor --json` output via subprocess — not IDE-specific.

Per-package checks:

```bash
stubborn doctor
stubborn-mcp doctor        # if using agents
stubborn-watch doctor      # if using dev watch loop
stubborn-indexer doctor    # future — scip-java toolchain
```

One-shot aggregate:

```bash
stubborn-status --json            # merges Doctor Report v1 JSON from installed packages
stubborn-status --require stubborn-mcp,stubborn-watch
```

Repo: [`stubborn-status`](https://pypi.org/project/stubborn-status/) (`0.10.0b2`).

Specs: [ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md),
[ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md).

### Host launcher preflight

Every host `scripts/run-e2e.sh` (and MCP smoke scripts) sources
[`scripts/stubborn-preflight.sh`](https://github.com/stubborn-ai/stubborn-demo/blob/main/scripts/stubborn-preflight.sh)
before the main workflow:

1. `stubborn doctor <project-root>` — blocking on **fail** (exit 1); **warn** (exit 2) continues
2. `stubborn-status --require …` when `stubborn-status` is installed (optional tip if missing)

| Launcher | `stubborn_preflight` root | `--require` packages |
|----------|---------------------------|----------------------|
| `demo-spring/scripts/run-e2e.sh` | `demo-spring/` | `stubborn-stub` (default) |
| `demo-spring/scripts/mcp-smoke.sh` | `demo-spring/` | `stubborn-stub,stubborn-mcp` |
| `spring-petclinic-microservices/scripts/mcp-smoke.sh` | example root | `stubborn-stub,stubborn-mcp` |
| `scripts/try-stubborn.sh` | `.` | skipped (`SKIP_STUBBORN_STATUS=1`) |

Docker `e2e` runs the same preflight when `/opt/stubborn-demo/scripts/stubborn-preflight.sh`
exists in the image.

On failure, scripts print links to
[TROUBLESHOOTING](https://github.com/stubborn-ai/stubborn/blob/main/docs/TROUBLESHOOTING.md)
and [USER-JOURNEY](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/USER-JOURNEY.md).

## Five-minute paths

Copy-paste entrypoints after `pip install stubborn-stub` (add `stubborn-stub[scip]` for binary `.scip`).

### 1. No Java — JSON fixture only

```bash
pip install stubborn-stub
stubborn try
```

Or from [`stubborn-demo`](https://github.com/stubborn-ai/stubborn-demo): `./scripts/try-stubborn.sh`.

Manual steps: `stubborn index --fixture minimal`, `stubborn list-symbols …`, `stubborn context …`.

### 2. Java monolith — host E2E shape

```bash
git clone https://github.com/stubborn-ai/stubborn-demo.git
cd stubborn-demo/demo-spring
stubborn doctor
./scripts/run-e2e.sh
```

Requires JDK 21+, Maven, `scip-java`, and `stubborn` on `PATH`. Docker alternative:
`docker compose run --rm e2e` from `stubborn-demo` root.

### 3. Microservices + contract evidence

```bash
cd stubborn-demo/spring-petclinic-microservices
stubborn doctor
./scripts/run-e2e.sh
./scripts/mcp-smoke.sh   # requires stubborn-mcp
```

See [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md) for pipeline stages.

## Host ↔ Docker differences worth remembering

1. **demo-spring E2E:** Docker also runs `stubborn metrics`; host script skips it.
2. **dukesbank:** Host fails fast without `BANK_ROOT`; Docker supplies `/bank` via mount.
3. **Upstream clones:** Host keeps persistent `upstream/`; Docker clones ephemerally unless volume-mounted.
4. **dukesbank context verifier:** documented as a separate manual host step.
5. **multi-repo Docker** runs the Python verifier directly (no bash wrapper).
