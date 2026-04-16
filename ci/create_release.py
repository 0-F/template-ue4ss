import os
import shutil
import zipfile
from pathlib import Path


def zip_directory(src_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in src_dir.rglob("*"):
            zf.write(item, item.relative_to(src_dir.parent))


def load_includes(path: Path) -> set[str]:
    if not path.exists():
        raise FileNotFoundError(f"Included files list not found: {path}")

    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def copy_included_path(
    project_root: Path, target_root: Path, include_entry: str
) -> None:
    relative_path = Path(include_entry.rstrip("/\\"))
    source_path = project_root / relative_path
    target_path = target_root / relative_path

    if not source_path.exists():
        raise FileNotFoundError(f"Included path not found: {source_path}")

    if source_path.is_dir():
        shutil.copytree(source_path, target_path)
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)


def main() -> int:
    project_root = (Path(__file__).resolve().parent / "..").resolve()
    os.chdir(project_root)

    release_name_dir = Path(os.environ["RELEASE_NAME_DIR"])
    target_name_dir = Path(os.environ["TARGET_DIR"])
    release_rel_path = Path(os.environ["RELEASE_REL_PATH"])
    version = os.environ["VERSION"]

    # Under act, the job runs inside a container and github_workspace_dir is the
    # mounted repository root, so writing there makes the ZIP visible to the host.
    github_workspace_dir = Path("/github/workspace")

    if not release_name_dir.exists():
        release_name_dir.mkdir(parents=True, exist_ok=True)

    if target_name_dir.exists():
        shutil.rmtree(target_name_dir)

    target_name_dir.mkdir(parents=True, exist_ok=True)

    includes = load_includes(project_root / "ci" / "release-files.txt")
    for include_entry in sorted(includes):
        copy_included_path(project_root, target_name_dir, include_entry)

    (target_name_dir / "enabled.txt").touch()
    (target_name_dir / "version.txt").write_text(version + "\n", encoding="utf-8")

    zip_directory(target_name_dir, release_rel_path)
    print(f"ZIP created: {release_rel_path}")

    if not release_rel_path.exists():
        raise RuntimeError("ZIP release failed.")

    if os.environ.get("ACT_HOST_PROJECT_ROOT", "").strip():
        host_release_dir = Path(os.environ["ACT_HOST_PROJECT_ROOT"]) / release_name_dir
        host_release_dir.mkdir(parents=True, exist_ok=True)

        host_zip_path = host_release_dir / release_rel_path.name
        shutil.copy2(release_rel_path, github_workspace_dir / release_name_dir)

        print(f"ZIP copied to host workspace: {host_zip_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
