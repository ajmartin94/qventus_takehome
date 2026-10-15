"""The dependency rule (implementation plan, Section 2.1) is enforced, not just documented."""

from __future__ import annotations

import os

from importlinter.cli import lint_imports

from tests.conftest import PROJECT_ROOT


def test_import_contracts_hold() -> None:
    cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    try:
        exit_code = lint_imports(config_filename="pyproject.toml", no_cache=True, no_logo=True)
    finally:
        os.chdir(cwd)
    assert exit_code == 0, "an import contract in pyproject.toml is broken; run `lint-imports` for details"
