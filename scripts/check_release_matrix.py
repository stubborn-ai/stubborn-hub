#!/usr/bin/env python3
"""Verify hub release-matrix docs match PyPI and optional local package repos."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

PACKAGES = ("stubborn-stub", "stubborn-mcp", "stubborn-watch")

MATRIX_ROW = re.compile(
    r"^\|\s*`(" + "|".join(re.escape(p) for p in PACKAGES) + r")`\s*\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)

PYPROJECT_VERSION = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)
MODULE_VERSION = re.compile(r'^__version__\s*=\s*"([^"]+)"', re.MULTILINE)

DOC_MATRIX_FILES = (
    "README.md",
    "docs/START-HERE.md",
)

REPO_LAYOUT = {
    "stubborn-stub": {
        "dir": "stubborn",
        "pyproject": "pyproject.toml",
        "version_files": ("src/stubborn/__init__.py",),
    },
    "stubborn-mcp": {
        "dir": "stubborn-mcp",
        "pyproject": "pyproject.toml",
        "version_files": ("src/stubborn_mcp/__version__.py",),
    },
    "stubborn-watch": {
        "dir": "stubborn-watch",
        "pyproject": "pyproject.toml",
        "version_files": (),
    },
}


@dataclass(frozen=True)
class Failure:
    check: str
    detail: str


def parse_release_matrix(text: str, source: str) -> dict[str, str]:
    versions = {package: version for package, version in MATRIX_ROW.findall(text)}
    missing = [package for package in PACKAGES if package not in versions]
    if missing:
        raise ValueError(f"{source}: release matrix missing {', '.join(missing)}")
    return versions


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_pyproject_version(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = PYPROJECT_VERSION.search(read_text(path))
    return match.group(1) if match else None


def read_module_versions(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return MODULE_VERSION.findall(read_text(path))


def pypi_has_version(package: str, version: str) -> tuple[bool, str]:
    url = f"https://pypi.org/pypi/{package}/json"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        return False, f"PyPI HTTP {exc.code} for {package}"
    except urllib.error.URLError as exc:
        return False, f"PyPI request failed for {package}: {exc.reason}"

    releases = payload.get("releases", {})
    if version not in releases:
        return False, f"{package} {version} is not listed on PyPI"
    if not releases[version]:
        return False, f"{package} {version} exists on PyPI but has no release files"
    return True, f"{package} {version} is published on PyPI"


def git_has_tag(repo_root: Path, version: str) -> tuple[bool, str]:
    tag = f"v{version}"
    completed = subprocess.run(
        ["git", "-C", str(repo_root), "tag", "--list", tag],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        return False, f"git tag lookup failed in {repo_root}: {completed.stderr.strip()}"
    if not completed.stdout.strip():
        return False, f"missing git tag {tag} in {repo_root.name}"
    return True, f"{repo_root.name} has tag {tag}"


def check_doc_matrices(hub_root: Path, canonical: dict[str, str]) -> list[Failure]:
    failures: list[Failure] = []
    for relative in DOC_MATRIX_FILES:
        path = hub_root / relative
        try:
            documented = parse_release_matrix(read_text(path), relative)
        except ValueError as exc:
            failures.append(Failure("doc-matrix", str(exc)))
            continue
        for package, version in canonical.items():
            if documented.get(package) != version:
                failures.append(
                    Failure(
                        "doc-matrix",
                        (
                            f"{relative} documents {package} as "
                            f"{documented.get(package)!r}, expected {version!r}"
                        ),
                    )
                )
    return failures


def check_local_repos(program_root: Path, canonical: dict[str, str]) -> list[Failure]:
    failures: list[Failure] = []
    for package, version in canonical.items():
        layout = REPO_LAYOUT[package]
        repo_root = program_root / layout["dir"]
        if not repo_root.is_dir():
            failures.append(
                Failure(
                    "local-repo",
                    f"{package}: repo directory not found at {repo_root}",
                )
            )
            continue

        pyproject_version = read_pyproject_version(repo_root / layout["pyproject"])
        if pyproject_version is None:
            failures.append(
                Failure("local-repo", f"{package}: could not read {layout['pyproject']} version")
            )
        elif pyproject_version != version:
            failures.append(
                Failure(
                    "local-repo",
                    (
                        f"{package}: {layout['pyproject']} has {pyproject_version!r}, "
                        f"hub documents {version!r}"
                    ),
                )
            )

        for relative in layout["version_files"]:
            module_path = repo_root / relative
            module_versions = read_module_versions(module_path)
            if not module_versions:
                failures.append(
                    Failure("local-repo", f"{package}: could not read __version__ in {relative}")
                )
                continue
            for module_version in module_versions:
                if module_version != version:
                    failures.append(
                        Failure(
                            "local-repo",
                            (
                                f"{package}: {relative} has {module_version!r}, "
                                f"hub documents {version!r}"
                            ),
                        )
                    )

        tag_ok, tag_detail = git_has_tag(repo_root, version)
        if not tag_ok:
            failures.append(Failure("git-tag", tag_detail))

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hub-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to stubborn-hub checkout",
    )
    parser.add_argument(
        "--program-root",
        type=Path,
        default=None,
        help="Optional workspace root containing stubborn/, stubborn-mcp/, stubborn-watch/",
    )
    parser.add_argument(
        "--pypi",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Verify documented versions are published on PyPI",
    )
    parser.add_argument(
        "--local-repos",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Verify sibling package repos and git tags (default: on when --program-root is set)",
    )
    args = parser.parse_args()

    hub_root = args.hub_root.resolve()
    program_root = args.program_root.resolve() if args.program_root else None
    check_local = args.local_repos if args.local_repos is not None else program_root is not None

    failures: list[Failure] = []
    try:
        canonical = parse_release_matrix(read_text(hub_root / "README.md"), "README.md")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Canonical release matrix (README.md):")
    for package in PACKAGES:
        print(f"  - {package}: {canonical[package]}")

    failures.extend(check_doc_matrices(hub_root, canonical))

    if args.pypi:
        print("\nPyPI checks:")
        for package in PACKAGES:
            ok, detail = pypi_has_version(package, canonical[package])
            print(f"  {'OK' if ok else 'FAIL'}: {detail}")
            if not ok:
                failures.append(Failure("pypi", detail))

    if check_local:
        if program_root is None:
            print("\nSkipping local repo checks (no --program-root).", file=sys.stderr)
        else:
            print(f"\nLocal repo checks under {program_root}:")
            local_failures = check_local_repos(program_root, canonical)
            failures.extend(local_failures)
            if not local_failures:
                print("  OK: pyproject, module versions, and git tags align with hub docs")

    if failures:
        print("\nRelease consistency check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  [{failure.check}] {failure.detail}", file=sys.stderr)
        return 1

    print("\nRelease consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
