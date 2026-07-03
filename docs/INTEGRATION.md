# Integration with anchor-migration

Stubborn AI is an **independent organization**. Integration with [anchor-migration](https://github.com/anchor-migration) is **optional** and **weakly coupled**.

## Role split

| Program | Primary artifact | LLM use |
|---------|------------------|---------|
| **anchor-migration** | Schema SSOT + Java AST SSOT + rewrite + parity | Drafting mappings, recipe design |
| **stubborn-ai** | SCIP → pruned stub context | Agent context before codegen |

Stubborn does **not** replace `java-ast-ssot` or `db-metadata`. It compiles **SCIP symbol graphs**, not live DB exports or JavaParser AST snapshots.

## Documented integration

| Doc | Location |
|-----|----------|
| anchor-migration ADR-010 | [ADR-010-stubborn-integration](https://github.com/anchor-migration/migration-hub/blob/main/docs/ADR-010-anchor-stubborn-integration.md) |
| stubborn consumer guide | [stubborn INTEGRATION.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/INTEGRATION.md) |
| Duke's Bank LLM context | [DUKESBANK-DEMO Step 7](https://github.com/anchor-migration/migration-hub/blob/main/docs/DUKESBANK-DEMO.md) |

## Shared conventions (no code coupling)

- SQLite snapshot files as portable artifacts
- Stable symbol IDs for reconcile vocabulary
- Deterministic, test-gated deliverables
- Architecture-led, AI-assisted development model

## What we do not share

- No shared Python/Java library dependency between orgs
- No requirement to use anchor-migration to use Stubborn
- Product ADRs live in `stubborn/docs/adr/`; program ADRs in `stubborn-hub` when cross-cutting

## Local workspace

Authors may clone both trees:

```
C:\github\anchor-migration\   # migration-hub, java-ast-ssot, …
C:\github\stubborn-ai\        # stubborn-hub, stubborn, lab-notes
```

`anchor-migration.code-workspace` already includes `stubborn` as a folder pointing at `../stubborn-ai/stubborn`.
