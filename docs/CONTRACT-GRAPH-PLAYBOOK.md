# Contract Graph playbook

How to add **HTTP contract evidence** to a Stubborn workspace and query it
alongside SCIP code facts. Normative design: [stubborn CONTRACT-GRAPH.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/CONTRACT-GRAPH.md) and ADR-011/012/013.

## Decision tree

```text
Do you have OpenAPI 3.x for a service?
├─ YES → stubborn index-openapi (strong endpoint/schema facts)
│         └─ Need code↔endpoint bindings?
│              ├─ Generated client traceable → future adapter (strong)
│              └─ Otherwise → stubborn index-contract manifest (declared)
└─ NO  → Do NOT invent endpoints from Java annotations in core.
          Use explicit manifest (declared) or fix the spec first.
```

| Goal | Command | Evidence |
|------|---------|----------|
| Endpoint + schema facts from spec | `stubborn index-openapi` | `strong` |
| Provider/consumer bindings | `stubborn index-contract` | `declared` |
| Code symbols only | `stubborn index` (SCIP) | SCIP graph |

**Never** rely on SCIP alone to prove HTTP routes across services ([ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md)).

## Required fields (workspace mode)

When multiple sources share one `symbols.db`, keep these **explicit and consistent**:

| Field | Where | Example |
|-------|-------|---------|
| `workspace` | every ingest | `contract-minimal`, `petclinic-ms` |
| `repo` | code ingest | `customers-service`, `visits-service` |
| `service` | `index-openapi` | `customers-service` |
| `version` | `index-openapi` | `v1` |

Endpoint stable IDs are derived from authority sources:

```text
openapi <service>:<version> <METHOD> <path-template>
```

Example:

```text
openapi customers-service:v1 GET /owners/{ownerId}
```

## Minimal mixed workspace (canonical E2E)

**Fastest path** — no Java toolchain:

```bash
pip install "stubborn-stub[openapi]"
git clone https://github.com/stubborn-ai/stubborn-demo.git
cd stubborn-demo/contract-graph-minimal
./scripts/run-e2e.sh
```

What it runs ([`scripts/verify_contract_graph_minimal.py`](https://github.com/stubborn-ai/stubborn-demo/blob/main/scripts/verify_contract_graph_minimal.py)):

1. Index two JSON SCIP fixtures as separate workspace repos
2. `index-openapi` for `customers-service`
3. `index-contract` for declared provider/consumer bindings
4. Assert `list-contracts`, endpoint `context`, and provider-type `context` include contract facts

Docker:

```bash
cd stubborn-demo
docker compose run --rm contract-graph-e2e
```

## Step-by-step (copy-paste)

Assume workspace `acme`, database `metadata/symbols.db`.

### 1. Code repos (SCIP)

```bash
stubborn index --scip customers/index.scip --out metadata/symbols.db \
  --workspace acme --repo customers-service

stubborn index --scip visits/index.scip --out metadata/symbols.db \
  --workspace acme --repo visits-service
```

JSON fixtures are valid for tests and the minimal demo; production uses scip-java output.

### 2. OpenAPI endpoints

```bash
stubborn index-openapi \
  --openapi specs/customers-openapi.yml \
  --service customers-service \
  --version v1 \
  --workspace acme \
  --out metadata/symbols.db
```

This writes **endpoint and schema constraint** rows. It does **not** create code bindings.

### 3. Declared bindings

`contracts/bindings.json` (shape):

```json
{
  "workspace": "acme",
  "contract_repo": "contract-manifests",
  "endpoints": [
    {
      "service": "customers-service",
      "version": "v1",
      "method": "GET",
      "path": "/owners/{ownerId}",
      "providers": [{ "repo": "customers-service", "display_name": "OwnerResource" }],
      "consumers": [{ "repo": "visits-service", "display_name": "CustomersClient" }]
    }
  ]
}
```

```bash
stubborn index-contract \
  --manifest contracts/bindings.json \
  --workspace acme \
  --out metadata/symbols.db
```

Bindings resolve `repo` + `display_name` to code `stable_id` values already in the workspace.

### 4. Inspect

```bash
stubborn info metadata/symbols.db --workspace acme
stubborn list-contracts metadata/symbols.db --workspace acme
stubborn list-symbols metadata/symbols.db --workspace acme --query OwnerResource
```

### 5. Query context

**Contract endpoint target** (protocol-first):

```bash
stubborn context metadata/symbols.db \
  --workspace acme \
  --target "openapi customers-service:v1 GET /owners/{ownerId}" \
  --format stubborn-dsl
```

**Code type target** (include declared cross-service edges — target the **bound type**, not only a method):

```bash
stubborn context metadata/symbols.db \
  --workspace acme \
  --target "semanticdb maven com/example/customers/OwnerResource#" \
  --format stubborn-dsl \
  --call-depth 1
```

Use `java-stub` when generating Java-shaped output; use `stubborn-dsl` when you need the `contracts:` block and evidence tiers visible.

## MCP equivalent

After `export STUBBORN_DB=metadata/symbols.db`:

1. `workspace_info` with `workspace: "acme"`
2. `list_contracts` with the same workspace
3. `get_context` with an `openapi …` or code `stable_id` target

See [stubborn-mcp MCP.md](https://github.com/stubborn-ai/stubborn-mcp/blob/main/docs/MCP.md).

## Evidence tiers (user-visible)

| Tier | Meaning | Default in strict mode |
|------|---------|------------------------|
| `strong` | OpenAPI / mechanical trace | Included |
| `declared` | Reviewed manifest | Included |
| `inferred` | Heuristic adapter only | Excluded unless opted in |
| `unknown` | Endpoint without binding | Endpoint facts only |

Contract sections in `stubborn-dsl` must not upgrade `declared` to proof language.

## Scale-up references

| Scenario | Demo / doc |
|----------|------------|
| Minimal mixed workspace (fixtures) | [`stubborn-demo/contract-graph-minimal`](https://github.com/stubborn-ai/stubborn-demo/tree/main/contract-graph-minimal) |
| Real Java microservices + MCP | [`spring-petclinic-microservices`](https://github.com/stubborn-ai/stubborn-demo/tree/main/spring-petclinic-microservices) |
| Validation model | [PETCLINIC-VALIDATION.md](PETCLINIC-VALIDATION.md) |
| Multi-repo code only (no HTTP) | [`stubborn-demo/multi-repo`](https://github.com/stubborn-ai/stubborn-demo/tree/main/multi-repo) |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `list-contracts` empty after SCIP-only ingest | Run `index-openapi` and/or `index-contract` |
| OpenAPI ingest without `--service` | `--service` is required |
| Workspace mismatch | Use the same `--workspace` on every ingest and query |
| Target a method, expect `contracts:` block | Bindings attach to types; target the provider **class** `stable_id` or the **endpoint** stable ID |
| Expect core to parse Spring MVC routes | Out of scope — add OpenAPI or manifest evidence |

Troubleshooting: [stubborn TROUBLESHOOTING.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/TROUBLESHOOTING.md).

## Related ADRs

- [ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md) — OpenAPI contract graph
- [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) — schema v4 tables
- [ADR-013](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-013-source-neutral-contract-queries.md) — source-neutral queries
