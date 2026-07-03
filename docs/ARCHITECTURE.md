# Architecture

## Overview

Stubborn AI is a **multi-repo program** for compiling SCIP symbol graphs into bounded, privacy-safe LLM context. The `stubborn` repo is the headless core; surrounding repos own surfaces, orchestration, and runnable validation projects. Shared contracts (`IndexSnapshot`, SQLite schema v1+, `stubborn.api`) link layers without a monorepo.

**Visual maps:** [Program overview](#program-overview) · [Developer experience layers](#developer-experience-layers) · [Repository map](#repository-map)

Significant design changes are recorded as ADRs in [`stubborn/docs/adr/`](https://github.com/stubborn-ai/stubborn/tree/main/docs/adr).

## Program overview

Repos are **independent**; integration is via **PyPI packages**, **CLI**, and **SQLite snapshot files** (`symbols.db`).

```mermaid
flowchart TB
  subgraph sources["Sources"]
    SRC["Source code"]
    SCIP_IDX["SCIP indexers<br/>(scip-java, …)"]
    ALT["Optional future ingest<br/>(OpenAPI, LSP, …)"]
  end

  subgraph L1["Layer 1 — Index & store"]
    ING["stubborn ingest"]
    DB[(symbols.db)]
    SRC --> SCIP_IDX --> ING
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
    IDE["IDE extensions (optional)"]
    WATCH --> SCIP_IDX
    WATCH --> ING
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
| Ingest | `stubborn` | SCIP | `symbols.db` |
| Context compile | `stubborn` | `symbols.db` + target | stub text |
| Agent access | `stubborn-mcp` | API calls | MCP tool JSON |
| Dev hot path | `stubborn-watch` | File events | merge into `symbols.db` |
| Demos / validation | `stubborn-demo` | Runnable projects | black-box proof via CLI / MCP |

## Developer experience layers

Complete DX requires all layers; beta today ships the headless core, MCP, watch scaffold, and runnable Java validation projects.

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

SCIP remains **canonical** for CI and reconcile. Optional non-SCIP ingest adapters (lab idea) are **opt-in** and must carry provenance — see `lab-notes/ideas/pluggable-ingest.md`.

## Repository map

```mermaid
flowchart LR
  HUB["stubborn-hub<br/>docs"]
  CORE["stubborn<br/>compiler"]
  MCP["stubborn-mcp"]
  WATCH["stubborn-watch"]
  DEMO["stubborn-demo"]
  NOTES["lab-notes<br/>private"]

  HUB -.-> CORE
  HUB -.-> MCP
  HUB -.-> DEMO
  MCP --> CORE
  WATCH --> CORE
  DEMO --> CORE
  DEMO --> MCP
  DEMO --> WATCH
  NOTES -.-> HUB
```

| Repository | Layer | Depends on |
|------------|-------|------------|
| `stubborn-hub` | Program docs | — |
| `stubborn` | Headless core: L1 + L2 + CLI + API | SCIP ecosystem |
| `stubborn-mcp` | L3 (MCP) | `stubborn-stub` |
| `stubborn-watch` | L4 (orchestration) | `stubborn-stub`, scip-java |
| `stubborn-demo` | Runnable demos / validation | `stubborn-stub`, `stubborn-mcp`, `stubborn-watch`, scip-java |
| `lab-notes` | Private drafts | — |

Future ideas (not committed repos): `stubborn-indexer` (multi-SCIP CLI glue), `vscode-stubborn`, `stubborn-ingest-openapi` — tracked in lab-notes only.

## Contracts (boundary protocols)

| Boundary | Contract | Document |
|----------|----------|----------|
| SCIP → snapshot | `IndexSnapshot`, ingest enrichment | [SCIP-INGEST](https://github.com/stubborn-ai/stubborn/blob/main/docs/SCIP-INGEST.md) |
| Snapshot → store | SQLite schema v1+ | [ADR-002](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-002-sqlite-symbol-graph-ssot.md) |
| Store → context | `stubborn.api`, budgets, weave options | `stubborn` source |
| Output formats | `java-stub`, `stubborn-dsl` grammars | [STUBBORN-DSL](https://github.com/stubborn-ai/stubborn/blob/main/docs/STUBBORN-DSL.md) |
| Agent tools | MCP tool schemas | [MCP.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/MCP.md) → moves to `stubborn-mcp` |

## Relationship to anchor-migration

Stubborn AI is an **independent org**. [anchor-migration](https://github.com/anchor-migration) may consume `stubborn` as optional horizontal LLM context — not as an SSOT pipeline layer. See [INTEGRATION.md](INTEGRATION.md).

## References

- [ECOSYSTEM.md](ECOSYSTEM.md)
- [ROADMAP.md](ROADMAP.md)
- [stubborn ADR index](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/README.md)
