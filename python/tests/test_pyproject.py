import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def _load() -> dict:
    with PYPROJECT.open("rb") as f:
        return tomllib.load(f)


def test_pyproject_declares_build_system() -> None:
    # pip install -e . requires a PEP 517 build backend to be declared.
    cfg = _load()
    build = cfg.get("build-system")
    assert build is not None, "missing [build-system] table"
    assert "build-backend" in build
    assert "requires" in build
    assert isinstance(build["requires"], list) and build["requires"]


def test_pyproject_hatch_wheel_points_at_src_layout() -> None:
    cfg = _load()
    wheel = (
        cfg.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel")
    )
    assert wheel is not None, "missing [tool.hatch.build.targets.wheel]"
    assert wheel.get("packages") == ["src/lap_schemas"]


def test_pyproject_does_not_reference_files_outside_project_root() -> None:
    # setuptools (and hatchling by default) reject readme paths that escape
    # the project directory. Keep references inside python/ to preserve
    # `pip install -e lap-schemas/python` portability.
    cfg = _load()
    project = cfg.get("project", {})
    readme = project.get("readme")
    if readme is not None:
        if isinstance(readme, str):
            assert not readme.startswith("../"), "readme path escapes project root"
        elif isinstance(readme, dict) and "file" in readme:
            assert not readme["file"].startswith("../")
