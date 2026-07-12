# User journey

Where to start as an **external user** — by goal, not by repository map.

For the full program index see [START-HERE.md](START-HERE.md). For failures and
copy-paste fixes see [stubborn TROUBLESHOOTING](https://github.com/stubborn-ai/stubborn/blob/main/docs/TROUBLESHOOTING.md).

## Choose your path

```text
Goal                          Start here
────────────────────────────────────────────────────────────────
Try Stubborn in 30 seconds    Journey A (pip, no Java)
Use Cursor / MCP on my repo   Journey B (agents)
Real Java / Spring project    Journey C (SCIP pipeline)
Microservices + HTTP contracts Journey D (workspace + contract graph)
CI / release engineering      Journey E (Docker + doctor + matrix)
```

---

## Journey A — Try in 30 seconds (no Java)

**You need:** Python 3.11+, `pip`.

```bash
pip install stubborn-stub
stubborn try
```

From [`stubborn-demo`](https://github.com/stubborn-ai/stubborn-demo): `./scripts/try-stubborn.sh` (same CLI flow).

Notes:

- `stubborn try` uses the **bundled JSON fixture** inside `stubborn-stub` (no clone, no Java).
- Manual steps: `stubborn index --fixture minimal`, `stubborn list-symbols …`, `stubborn context …`.
- This proves the **compiler** only — not weave quality on your codebase.

**Next steps (pick one):**

| If you… | Go to |
|---------|-------|
| Use **Cursor / MCP** | [Journey B](#journey-b--cursor--mcp-agents) — `pip install stubborn-mcp`, build `symbols.db`, configure `.cursor/mcp.json` |
| Have a **Java / Spring** repo | [Journey C](#journey-c--real-java--spring-project) — `scip-java` + `stubborn index` |
| Work on **microservices + OpenAPI** | [Journey D](#journey-d--microservices--contract-graph) |
| Hit errors | [stubborn TROUBLESHOOTING](https://github.com/stubborn-ai/stubborn/blob/main/docs/TROUBLESHOOTING.md) or `stubborn-status --json` |

`stubborn try` prints the same Journey B/C pointers when it finishes.

**Next:** Journey C if you have Java; Journey B if you want MCP.

---

## Journey B — Cursor / MCP agents

**You need:** Python 3.11+, a prepared `symbols.db`, [`stubborn-mcp`](https://pypi.org/project/stubborn-mcp/).

### B1. Code graph (typical)

```bash
pip install "stubborn-stub[scip]" stubborn-mcp
# After you have index.scip from scip-java (Journey C):
stubborn index --scip index.scip --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp doctor
```

Cursor `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "stubborn": {
      "command": "stubborn-mcp",
      "env": {
        "STUBBORN_DB": "${workspaceFolder}/metadata/symbols.db"
      }
    }
  }
}
```

Agent workflow:

1. `workspace_info` (when using a named workspace)
2. `list_symbols` with `query` → pick a `stable_id`
3. `get_context` with that target before codegen
4. Optional: `metrics` with your Java `sources` tree

Full tool reference: [stubborn-mcp docs/MCP.md](https://github.com/stubborn-ai/stubborn-mcp/blob/main/docs/MCP.md).

### B2. Contract-only smoke (OpenAPI)

Requires an OpenAPI file you own. For a runnable reference, clone
[`stubborn-demo`](https://github.com/stubborn-ai/stubborn-demo) and follow
[spring-petclinic-microservices](https://github.com/stubborn-ai/stubborn-demo/tree/main/spring-petclinic-microservices)
after `./scripts/run-e2e.sh` (produces a workspace DB with contract evidence).

### Diagnostics

```bash
pip install stubborn-status
stubborn-status --json
stubborn-status --require stubborn-mcp
```

Specs: [ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md),
[ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md).

**Planned:** `vscode-stubborn` IDE panel over `stubborn-status --json`.

---

## Journey C — Real Java / Spring project

**You need:** JDK 21+, Maven, [scip-java](https://github.com/sourcegraph/scip-java) on `PATH`,
`pip install "stubborn-stub[scip]"`.

```bash
scip-java index --build-tool maven
stubborn index --scip index.scip --out metadata/symbols.db
stubborn list-symbols metadata/symbols.db --query YourService
stubborn context metadata/symbols.db --target "<stable_id>" --out context.stub.java
```

**Fastest validated reference:** [`stubborn-demo/demo-spring`](https://github.com/stubborn-ai/stubborn-demo/tree/main/demo-spring)

| Tier | Command |
|------|---------|
| Docker (canonical) | From `stubborn-demo` root: `docker compose run --rm e2e` |
| Host | `cd demo-spring && ./scripts/run-e2e.sh` |

**Dev loop (save → re-index → merge):**

```bash
pip install stubborn-watch
stubborn-watch watch --root . --db metadata/symbols.db
```

See [ADR-009](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-009-incremental-index-merge.md) and
`demo-spring/scripts/run-merge-e2e.sh`.

**Not in core (by design):** automatic scip-java orchestration. Future home:
`stubborn-onboard` / indexer layer (ADR TBD). Until then, use demo scripts or
your own CI step.

---

## Journey D — Microservices + contract graph

**You need:** Everything in Journey C **per service repo**, plus explicit contract
facts (OpenAPI and/or manifest). Stubborn does **not** infer HTTP routes from
SCIP alone.

Canonical proof: [`spring-petclinic-microservices`](https://github.com/stubborn-ai/stubborn-demo/tree/main/spring-petclinic-microservices)

```bash
# Docker (from stubborn-demo root)
docker compose run --rm petclinic-ms-e2e

# Host
cd spring-petclinic-microservices && ./scripts/run-e2e.sh
```

Read:

- [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md) (microservices section)
- [stubborn CONTRACT-GRAPH.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/CONTRACT-GRAPH.md)

Commands you will use:

```bash
stubborn index-openapi --openapi <spec> --service <name> --workspace <ws> --out metadata/symbols.db
stubborn index-contract --manifest <manifest> --out metadata/symbols.db
stubborn list-contracts metadata/symbols.db --workspace <ws>
stubborn context metadata/symbols.db --target "openapi <service>:<ver> <METHOD> <path>" ...
```

Canonical minimal E2E: [CONTRACT-GRAPH-PLAYBOOK.md](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/CONTRACT-GRAPH-PLAYBOOK.md) and [`stubborn-demo/contract-graph-minimal`](https://github.com/stubborn-ai/stubborn-demo/tree/main/contract-graph-minimal).

---

## Journey E — CI, doctor, release matrix

**Docker E2E:** [DEMO-LAUNCHERS.md](DEMO-LAUNCHERS.md) — explicit env/CLI contracts
for every validation script.

**Federated doctor (read-only):**

```bash
stubborn doctor --json
stubborn-mcp doctor --json
stubborn-watch doctor --json
stubborn-status --json --db metadata/symbols.db
```

**Release consistency (maintainers):**

```bash
python stubborn-hub/scripts/check_release_matrix.py --pypi --program-root .
```

---

## Package cheat sheet

| Install | CLI | When |
|---------|-----|------|
| `stubborn-stub` | `stubborn` | Always — compiler |
| `stubborn-stub[scip]` | `stubborn` | Binary `.scip` / NDJSON from scip-java |
| `stubborn-mcp` | `stubborn-mcp` | Cursor / agents |
| `stubborn-watch` | `stubborn-watch` | Dev loop watch → merge |
| `stubborn-status` | `stubborn-status` | Aggregate doctor JSON |

PyPI package name **`stubborn-stub`** ≠ GitHub repo **`stubborn`**. The CLI is
**`stubborn`** (alias `stub`).

---

## Honest expectations

| Expectation | Reality |
|-------------|---------|
| `pip install` → instant repo map | **No** — SCIP (or bundled fixture) required |
| One command indexes my Java app | **Not in core** — use scip-java + `stubborn index` or future onboard layer |
| MCP works without `symbols.db` | **No** — build the DB first (or use Journey A fixture for a smoke) |
| Contract graph from code alone | **No** — OpenAPI/manifest evidence is explicit ([ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md)) |

See [POSITIONING.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/POSITIONING.md) for competitor trade-offs.
