# Release checklist

Coordinated beta release procedure for the Stubborn AI PyPI packages. The
**canonical version matrix** lives in [README.md](../README.md); this checklist
is the human runbook. Automation: [`scripts/check_release_matrix.py`](../scripts/check_release_matrix.py) and [`.github/workflows/release-consistency.yml`](../.github/workflows/release-consistency.yml).

**Versioning policy:** [ADR-017 Program versioning policy](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-017-program-versioning-policy.md) (summary below).

## Packages in scope

| PyPI package | Repo | Tag format | Typical lead |
|--------------|------|------------|--------------|
| `stubborn-stub` | `stubborn` | `v0.10.0bN` | **First** — core compiler |
| `stubborn-mcp` | `stubborn-mcp` | `v0.10.0bN` | After core is on PyPI |
| `stubborn-watch` | `stubborn-watch` | `v0.10.0bN` | After core is on PyPI |
| `stubborn-status` | `stubborn-status` | `v0.10.0bN` | Independent cadence |

Satellite packages pin `stubborn-stub>=<core-release>,<1.0` in `pyproject.toml`.

## Before you bump versions

1. **Scope** — decide which repos ship in this milestone (core-only vs coordinated).
2. **CHANGELOG** — move `[Unreleased]` entries to a dated version section in each shipping repo.
3. **Tests** — `pytest` + `ruff` green in each shipping repo.
4. **Docs** — hub `README.md` + `docs/START-HERE.md` release matrix rows match intended versions.

### Version bumps ([ADR-017](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-017-program-versioning-policy.md))

| Change | Bump | Example |
|--------|------|---------|
| New feature / release-worthy capability | **Minor** | `0.10.0b1` → `0.11.0b1` |
| Bug fix / safe refactor | **Patch** | `0.11.0b1` → `0.11.1b1` |
| Packaging / CI / metadata only | **Beta** | `0.11.0b1` → `0.11.0b2` |
| Breaking after 1.0 | **Major** | `1.0.0` → `2.0.0` |

Pre-1.0 features use the **minor** integer (`0.9` → `0.10`, not `0.9.1`). Coordinated
milestones share one **unified line** across all shipping packages. When unsure, prefer
**minor** over patch.

**Canonical vs display:** `pyproject.toml`, `__version__`, git tags, and PyPI always use
the full PEP 440 string (e.g. `0.11.0b1`). Hub docs may show `0.11.0` when meaning
first beta (`b1` omitted); `b2+` must stay visible. Tags: `v0.11.0b1`.

**Grandfathering:** `0.10.0b1` predates ADR-017; new rules apply from the **next**
release onward.

## Per-repo version files

| Package | Bump these |
|---------|------------|
| `stubborn-stub` | `pyproject.toml`, `src/stubborn/__init__.py`, `README.md`, `docs/BETA.md`, product docs citing the version |
| `stubborn-mcp` | `pyproject.toml`, `src/stubborn_mcp/__version__.py`, `CHANGELOG.md`, optional `docs/MCP.md` |
| `stubborn-watch` | `pyproject.toml`, `src/stubborn_watch/__init__.py`, `CHANGELOG.md` |
| `stubborn-status` | `pyproject.toml`, `src/stubborn_status/__init__.py`, `CHANGELOG.md`, `README.md` |

## Hub and org sync (same PR or immediately after tags)

Update version literals in:

- `stubborn-hub/README.md` — **release matrix** (canonical)
- `stubborn-hub/docs/START-HERE.md` — PyPI table + matrix
- `stubborn-hub/docs/ECOSYSTEM.md`, `docs/ROADMAP.md`, `AGENTS.md` as needed
- `stubborn-ai/.github/profile/README.md` — org profile PyPI table

Dependency column example:

```text
stubborn-stub>=0.10.0b2,<1.0
```

## Release order (coordinated)

```text
1. stubborn-stub  → commit → tag vX → push tag (triggers PyPI workflow)
2. Wait for PyPI to list the new core version
3. stubborn-mcp   → bump dep floor → tag → push
4. stubborn-watch → bump dep floor → tag → push
5. stubborn-status (if shipping) → tag → push
6. stubborn-hub + .github profile → commit → push (no tag)
```

Push tags over **SSH** (`git@github.com:stubborn-ai/<repo>.git`).

Each package's `Release` workflow runs on `v*` tag push and uploads to PyPI using `PYPI_API_TOKEN`.

**Release gate:** each package `release.yml` runs a `verify` job (`ruff check` + `pytest` on Python 3.12) before `pypi` publishes. A red lint or test blocks the upload and GitHub Release for that tag.

## Verify

### Local workspace (all repos checked out)

```bash
cd stubborn-hub
python3 scripts/check_release_matrix.py \
  --program-root /path/to/stubborn-ai \
  --pypi
```

Expect:

```text
Release consistency check passed.
```

### Hub CI

[Release Consistency](https://github.com/stubborn-ai/stubborn-hub/actions/workflows/release-consistency.yml) checks out sibling repos on every `main` push/PR and runs the same script with `--program-root`.

### Pre-tag hub PR (versions bumped, PyPI not updated yet)

```bash
python3 scripts/check_release_matrix.py \
  --program-root /path/to/stubborn-ai \
  --no-pypi
```

Use this while preparing a coordinated bump before tags land.

## Post-release smoke

```bash
pip install -U stubborn-stub stubborn-mcp stubborn-watch stubborn-status
stubborn try
stubborn doctor --db stubborn-try.symbols.db
stubborn-status --json
```

Optional contract path:

```bash
pip install "stubborn-stub[openapi]"
cd stubborn-demo/contract-graph-minimal && ./scripts/run-e2e.sh
```

## Troubleshooting

| Failure | Action |
|---------|--------|
| `ruff check` / `pytest` red on tagged commit | Release workflow `verify` job fails — fix on `main`, bump patch beta if needed, re-tag |
| `not listed on PyPI` | Confirm tag workflow succeeded; wait for PyPI index propagation |
| `missing git tag` | Push annotated tag `v<version>` to the package repo |
| Hub matrix mismatch | `README.md` and `START-HERE.md` must list identical versions |
| MCP import errors after release | `pip install -U` all packages; check `stubborn-stub` floor in satellite `pyproject.toml` |

## Related

- [ADR-017 Program versioning policy](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-017-program-versioning-policy.md) — full rules (unified line, dependency floors, 1.0 criteria)
- [USER-JOURNEY.md](USER-JOURNEY.md) — external install paths
- [stubborn-status RELEASE.md](https://github.com/stubborn-ai/stubborn-status/blob/main/docs/RELEASE.md) — first-time PyPI token notes
- [DEMO-LAUNCHERS.md](DEMO-LAUNCHERS.md) — validation entrypoints after release
