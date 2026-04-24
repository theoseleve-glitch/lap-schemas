import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / ".githooks" / "post-commit"


def _bash() -> str:
    # On Windows, prefer git-bash over System32\bash.exe (which is WSL and does
    # not share filesystem mounts with the host).
    for candidate in (
        Path("C:/Program Files/Git/usr/bin/bash.exe"),
        Path("C:/Program Files/Git/bin/bash.exe"),
    ):
        if candidate.exists():
            return str(candidate)
    resolved = shutil.which("bash")
    return resolved or "bash"


def _init_repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    return tmp_path


def _commit(repo: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "msg"], cwd=repo, check=True)


def test_hook_warns_when_v1_pydantic_model_changes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    _commit(
        repo,
        {"python/src/lap_schemas/v1/data_quality.py": "class DataQuality:\n    pass\n"},
    )
    result = subprocess.run(
        [_bash(), HOOK.as_posix()],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "post-commit hook must never fail"
    assert "Pydantic model change" in result.stderr
    assert "data_quality.py" in result.stderr


def test_hook_stays_silent_for_unrelated_changes(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    _commit(repo, {"README.md": "hello\n"})
    result = subprocess.run(
        [_bash(), HOOK.as_posix()],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Pydantic model change" not in result.stderr
