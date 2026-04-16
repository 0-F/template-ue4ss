import os
import platform
import subprocess
from pathlib import Path


def candidate_paths(project_root: Path) -> list[Path]:
    home = Path.home()
    user_profile = Path(os.environ.get("USERPROFILE", ""))
    candidates = [
        project_root / ".TEMP" / "act",
        home / ".cache" / "act",
        home / "Library" / "Caches" / "act",
    ]

    if str(user_profile):
        candidates.append(user_profile / ".cache" / "act")

    # Keep order and remove duplicates.
    unique: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path.resolve()) if path.exists() else str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def open_path(path: Path) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
        return
    if system == "Darwin":
        subprocess.run(["open", str(path)], check=False)
        return
    subprocess.run(["xdg-open", str(path)], check=False)


def main() -> int:
    project_root = (Path(__file__).resolve().parent / ".." / "..").resolve()
    candidates = candidate_paths(project_root)
    work_dir = next((p for p in candidates if p.exists()), None)

    if work_dir is None:
        checked = ", ".join(str(p) for p in candidates)
        print(f"⚠ Warning: No act work directory found. Checked: {checked}")
        return 1

    print(f"📂 Opening act work directory: {work_dir.resolve()}")
    open_path(work_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
