# PetClinic validation

How the two PetClinic demos prove Stubborn behavior — monolith code graph vs
multi-service workspace with explicit HTTP contract evidence.

Launcher contracts and CI mapping:
[DEMO-LAUNCHERS.md](DEMO-LAUNCHERS.md).

Smallest mixed-workspace proof (fixtures only, no Java):
[`stubborn-demo/contract-graph-minimal`](https://github.com/stubborn-ai/stubborn-demo/tree/main/contract-graph-minimal) and
[CONTRACT-GRAPH-PLAYBOOK.md](CONTRACT-GRAPH-PLAYBOOK.md).

## Two tracks

| Track | Demo path | Primary claim | Contract ingest |
|-------|-----------|---------------|-----------------|
| **Monolith** | `stubborn-demo/spring-petclinic` | Scale-up SCIP → prune → weave on ~30 Java files | none (code graph only) |
| **Microservices** | `stubborn-demo/spring-petclinic-microservices` | Workspace composition + HTTP bridge via schema v4 evidence | `stubborn index-contract` |

Both pin upstream commits in `upstream.pin` and clone to a local `upstream/`
directory on host runs.

## Monolith: spring-petclinic

### Pipeline

```text
upstream.pin → git clone
  → mvn package
  → scip-java index --build-tool maven
  → stubborn index → metadata/symbols.db
  → resolve VetController stable_id
  → stubborn context + metrics
  → verify_petclinic_context.py --java-root <upstream>/src/main/java
```

### Entrypoints

| Tier | Command |
|------|---------|
| Docker | `docker compose run --rm petclinic-e2e` |
| Host | `cd spring-petclinic && ./scripts/run-e2e.sh` |

### Verifier contract: `verify_petclinic_context.py`

| Input | Required? | Notes |
|-------|-----------|-------|
| `--java-root` | **Yes** | Path to `src/main/java` for token-savings metrics |
| `metadata/symbols.db` | implicit | Must exist from E2E |
| `metadata/expected-context-types-vet-controller.txt` | implicit | Expected type names in pruned context |

Checks:

1. `VetController` context contains every expected neighbor type.
2. `get_metrics` reports ≥ **70%** token savings vs raw sources.

This demo does **not** exercise `index-contract` or MCP contract tools. It
validates code-graph quality at larger scale than `demo-spring`.

### Case doc

[vet-controller-context.md](https://github.com/stubborn-ai/stubborn-demo/blob/main/spring-petclinic/cases/vet-controller-context.md)

### CI

Workflow: `petclinic-e2e` — `workflow_dispatch` + weekly schedule. Not on
every PR (heavier than demo-spring).

---

## Microservices: spring-petclinic-microservices

### Workspace layout

Upstream is one Git repo; Stubborn indexes four service directories as separate
workspace repos under `petclinic-ms`:

| `repo_key` | Upstream path |
|------------|---------------|
| `api-gateway` | `spring-petclinic-api-gateway` |
| `customers-service` | `spring-petclinic-customers-service` |
| `vets-service` | `spring-petclinic-vets-service` |
| `visits-service` | `spring-petclinic-visits-service` |

Config/discovery/observability services are intentionally skipped for the first
graph validation pass.

### Pipeline (8 stages)

```text
[0] clone/checkout upstream.pin
[1] mvn package (whole upstream)
[2] per-service scip-java index → metadata/indexes/*.scip
[3] stubborn index --workspace petclinic-ms --repo <key> (×4) → petclinic-workspace.db
[4] verify_petclinic_ms_workspace.py --mode baseline
[5] stubborn index-contract --manifest contracts/http.yml
[6] verify_petclinic_ms_workspace.py --mode bridged
[7] verify_petclinic_ms_workspace.py --mode emit-stubs
```

### Contract manifest: `contracts/http.yml`

Declares HTTP endpoints as **explicit graph facts** (not SCIP-inferred routing):

- `GET /owners/{ownerId}` on `customers-service`
  - consumers: `CustomersServiceClient`, `ApiGatewayController` (`api-gateway`)
  - providers: `OwnerResource` (`customers-service`)
- `GET /pets/visits` on `visits-service` (indexed for completeness; primary case uses owners)

`stubborn index-contract` writes schema v4 contract tables with
`evidence=declared`. Endpoint stable IDs follow the source-neutral model
(ADR-013), e.g. `openapi customers-service:v1 GET /owners/{ownerId}`.

### Verifier modes: `verify_petclinic_ms_workspace.py`

| Mode | When | Asserts |
|------|------|---------|
| `baseline` | After stage 3, **before** contract ingest | Four repo keys present; forward context at `CustomersServiceClient` does **not** include `OwnerResource`; no contract bindings yet |
| `bridged` | After `index-contract` | Contract bindings exist with `declared` evidence; forward context includes visit→customer types; reverse context at `OwnerResource` includes owner-impact types; `stubborn-dsl` output has `contracts:` block with `evidence=declared`; structured `contract_edges` present |
| `emit-stubs` | Final stage | Writes `visit-to-customer.stub.java` and `owner-impact-radius.stub.java` |

The baseline forbidden-neighbor check is deliberate: it proves the demo does not
accidentally rely on unsupported HTTP inference from SCIP alone.

### MCP smoke: `scripts/mcp-smoke.sh`

Run **after** host E2E. Requires `stubborn-mcp` in the same environment.

Exercises on `metadata/petclinic-workspace.db`:

| Tool | Check |
|------|-------|
| `workspace_info("petclinic-ms")` | 4 code repos, 1 contract source, 2 endpoints |
| `list_contracts` | Expected endpoint stable IDs |
| `get_context` | Forward `CustomersServiceClient` and reverse `OwnerResource` in `stubborn-dsl` with `contracts:` + `evidence=declared` |

This connects the demo to the same MCP surface documented in
[stubborn-mcp](https://github.com/stubborn-ai/stubborn-mcp).

### Case docs

| Case | Doc |
|------|-----|
| visit-to-customer | [visit-to-customer-context.md](https://github.com/stubborn-ai/stubborn-demo/blob/main/spring-petclinic-microservices/cases/visit-to-customer-context.md) |
| owner-impact-radius | [owner-id-impact-radius.md](https://github.com/stubborn-ai/stubborn-demo/blob/main/spring-petclinic-microservices/cases/owner-id-impact-radius.md) |

### Entrypoints

| Tier | Command |
|------|---------|
| Docker | `docker compose run --rm petclinic-ms-e2e` |
| Host E2E | `cd spring-petclinic-microservices && ./scripts/run-e2e.sh` |
| Host MCP | `./scripts/mcp-smoke.sh` (after E2E) |

### CI

Workflow: `petclinic-ms-e2e` — `workflow_dispatch` + weekly schedule.

---

## Product ADRs this demo exercises

| ADR | Role in PetClinic demos |
|-----|-------------------------|
| [ADR-011 OpenAPI contract graph](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md) | Contract facts as first-class graph input |
| [ADR-012 Schema v4 contract evidence](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) | `declared` evidence tier in SQLite + output |
| [ADR-013 Source-neutral contract queries](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-013-source-neutral-contract-queries.md) | `openapi …` endpoint targets in context/MCP |

## Honest boundary

PetClinic microservices does **not** claim that SCIP resolves HTTP, WebClient,
Feign, or gateway routing. The claim is narrower:

> Stubborn composes deterministic source graphs across service boundaries when
> service contracts are represented as explicit graph facts.

SCIP supplies per-service code graphs; `index-contract` supplies the bridge.
