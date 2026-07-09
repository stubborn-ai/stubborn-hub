# Architecture

## Overview

Stubborn AI is a **multi-repo program** for compiling deterministic graph facts into bounded, privacy-safe LLM context. SCIP remains the canonical code-symbol input; OpenAPI is the canonical REST contract input. The `stubborn` repo is the headless core; surrounding repos own surfaces, orchestration, and runnable validation projects. Shared contracts (`IndexSnapshot`, schema v4 contract tables, `stubborn.api`) link layers without a monorepo.

**Visual maps:** [Program overview](#program-overview) · [Developer experience layers](#developer-experience-layers) · [Repository map](#repository-map)

Significant design changes are recorded as ADRs in [`stubborn/docs/adr/`](https://github.com/stubborn-ai/stubborn/tree/main/docs/adr).

## Program overview

Repos are **independent**; integration is via **PyPI packages**, **CLI**, and **SQLite snapshot files** (`symbols.db`).

```mermaid
flowchart TB
  subgraph sources["Sources"]
    SRC["Source code"]
    OPENAPI["OpenAPI specs"]
    SCIP_IDX["SCIP indexers<br/>(scip-java, …)"]
    ALT["Optional future ingest<br/>(LSP, DB, …)"]
  end

  subgraph L1["Layer 1 — Index & store"]
    ING["stubborn ingest<br/>(SCIP + contract)"]
    DB[(symbols.db)]
    SRC --> SCIP_IDX --> ING
    OPENAPI --> ING
    ALT -.-> ING
    ING --> DB
  end

  subgraph L2["Layer 2 — Context compiler"]
    PRU["prune"]
    WEA["weave"]
    DB --> PRU --> WEA
  end

  subgraph L3["Layer 3 — Surfaces"]
    CLI["stubborn CLI"]
    API["stubborn.api"]
    MCP["stubborn-mcp"]
    WEA --> CLI
    WEA --> API
    API --> MCP
  end

  subgraph L4["Layer 4 — Dev orchestration"]
    WATCH["stubborn-watch"]
    IDE["vscode-stubborn<br/>(planned thin bridge)"]
    WATCH --> SCIP_IDX
    WATCH --> ING
    IDE --> MCP
    IDE --> WATCH
  end

  subgraph VAL["Validation & demos"]
    DEMO["stubborn-demo"]
    DEMO --> SCIP_IDX
    DEMO --> CLI
    DEMO --> MCP
  end
```

| Stage | Owner | Input | Output |
|-------|-------|-------|--------|
| SCIP indexing | External indexer | Source tree | `index.scip` |
| Code ingest | `stubborn` | SCIP / JSON fixture | code-symbol graph facts |
| Contract ingest | `stubborn` | OpenAPI spec or explicit manifest | endpoint/schema/binding facts |
| Store | `stubborn` | code + contract facts | `symbols.db` |
| Context compile | `stubborn` | `symbols.db` + code or endpoint target | `java-stub` / `stubborn-dsl` context |
| Agent access | `stubborn-mcp` | API calls | source-neutral MCP tool JSON |
| Dev hot path | `stubborn-watch` | File events | merge into `symbols.db` |
| IDE bridge | `vscode-stubborn` | VS Code commands/settings | MCP setup + sidecar stubs |
| Demos / validation | `stubborn-demo` | Runnable projects | black-box proof via CLI / MCP |

## Developer experience layers

Complete DX requires all layers; beta today ships the headless core, MCP, watch package, and runnable Java validation projects.

```mermaid
flowchart LR
  subgraph hot["Development (fast)"]
    S1["Save file"]
    S2["watch + merge"]
    S3["MCP sees new symbol"]
    S1 --> S2 --> S3
  end

  subgraph cold["Build / CI (authoritative)"]
    C1["compile"]
    C2["scip-java index"]
    C3["stubborn index snapshot"]
    C4["diff / guards"]
    C1 --> C2 --> C3 --> C4
  end
```

| Mode | Trigger | Stubborn command | Index run semantics |
|------|---------|------------------|---------------------|
| **Hot** | Save / watch | `index --merge` | Update active run by `relative_path` ([ADR-009](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-009-incremental-index-merge.md)) |
| **Cold** | Compile / CI | `index` (default) | Append full snapshot `index_run` |

SCIP remains **canonical** for code-symbol CI and reconcile. OpenAPI contract graph support is implemented in `stubborn index-openapi`; explicit bindings use `stubborn index-contract`. Contract facts are physically separate from SCIP facts and are composed at query time ([ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md), [ADR-013](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-013-source-neutral-contract-queries.md)).

## Repository map

```mermaid
flowchart LR
  HUB["stubborn-hub<br/>docs"]
  CORE["stubborn<br/>compiler"]
  MCP["stubborn-mcp"]
  WATCH["stubborn-watch"]
  VSCODE["vscode-stubborn"]
  DEMO["stubborn-demo"]
  NOTES["lab-notes<br/>private"]

  HUB -.-> CORE
  HUB -.-> MCP
  HUB -.-> DEMO
  MCP --> CORE
  WATCH --> CORE
  VSCODE --> MCP
  VSCODE --> WATCH
  DEMO --> CORE
  DEMO --> MCP
  DEMO --> WATCH
  NOTES -.-> HUB
```

| Repository | Layer | Depends on |
|------------|-------|------------|
| `stubborn-hub` | Program docs | — |
| `stubborn` | Headless core: L1 + L2 + CLI + API | SCIP ecosystem, OpenAPI specs |
| `stubborn-mcp` | L3 (MCP) | `stubborn-stub` |
| `stubborn-watch` | L4 (orchestration) | `stubborn-stub`, scip-java |
| `vscode-stubborn` | L4 (VS Code bridge) | `stubborn-mcp`, `stubborn-watch`, `stubborn-status` (planned) |
| `stubborn-status` | L4 (setup aggregation) | federated `doctor` CLIs via subprocess ([ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md)) |
| `stubborn-demo` | Runnable demos / validation | `stubborn-stub`, `stubborn-mcp`, `stubborn-watch`, scip-java |
| `lab-notes` | Private drafts | — |

Future ideas (not committed repos): `stubborn-indexer` (multi-SCIP CLI glue), `intellij-stubborn`, LSP/DB ingest adapters beyond OpenAPI — tracked in lab-notes only. **`stubborn-status`** ships in [ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md).

## Contracts (boundary protocols)

| Boundary | Contract | Document |
|----------|----------|----------|
| SCIP → snapshot | `IndexSnapshot`, ingest enrichment | [SCIP-INGEST](https://github.com/stubborn-ai/stubborn/blob/main/docs/SCIP-INGEST.md) |
| OpenAPI/manifest → contract graph | Endpoint stable IDs, schema constraints, binding evidence tiers | [ADR-011](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-011-openapi-contract-graph.md), [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) |
| Snapshot/contract → store | SQLite schema v4 | [ADR-002](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-002-sqlite-symbol-graph-ssot.md), [ADR-012](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-012-schema-v4-contract-evidence.md) |
| Store → context | Source-neutral `stubborn.api`, budgets, weave options | [ADR-013](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-013-source-neutral-contract-queries.md) |
| Output formats | `java-stub`, `stubborn-dsl` grammars | [STUBBORN-DSL](https://github.com/stubborn-ai/stubborn/blob/main/docs/STUBBORN-DSL.md) |
| Agent tools | MCP tool schemas (`workspace_info`, `list_symbols`, `list_contracts`, `get_context`, `metrics`) | [stubborn-mcp MCP.md](https://github.com/stubborn-ai/stubborn-mcp/blob/main/docs/MCP.md) |
| Setup diagnostics | Doctor Report v1, Status Report v1 | [ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md), [ADR-016](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-016-doctor-status-aggregation.md) |

## Relationship to anchor-migration

Stubborn AI is an **independent org**. [anchor-migration](https://github.com/anchor-migration) may consume `stubborn` as optional horizontal LLM context — not as an SSOT pipeline layer. See [INTEGRATION.md](INTEGRATION.md).

## References

- [ECOSYSTEM.md](ECOSYSTEM.md)
- [ROADMAP.md](ROADMAP.md)
- [stubborn ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md)
