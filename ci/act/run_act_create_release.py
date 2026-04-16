import argparse
import os
import subprocess
from pathlib import Path


def open_path_if_exists(path: Path, label: str) -> None:
    if not path.exists():
        print(f"⚠ Warning: {label} not found: {path}")
        return

    resolved = path.resolve()
    print(f"📂 Opening {label}: {resolved}")
    os.startfile(str(resolved))


def newest_zip_in(directory: Path) -> Path | None:
    if not directory.exists():
        return None

    candidates = sorted(
        [p for p in directory.rglob("*.zip") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def find_release_zip(release_dir: Path, project_root: Path) -> Path | None:
    for candidate_dir in (
        release_dir,
        project_root / ".artifacts",
        project_root,
    ):
        release_zip = newest_zip_in(candidate_dir)
        if release_zip is not None:
            return release_zip

    return None


def open_act_work_dir_if_exists(project_root: Path) -> None:
    candidates = [
        project_root / ".TEMP" / "act",
        Path(os.environ.get("USERPROFILE", "")) / ".cache" / "act",
    ]

    work_dir = next((p for p in candidates if p.exists()), None)
    if work_dir is None:
        checked = ", ".join(str(p) for p in candidates)
        print(f"⚠ Warning: No act work directory found. Checked: {checked}")
        return

    open_path_if_exists(work_dir, "act work directory")


def open_release_zip_if_exists(release_dir: Path, project_root: Path) -> None:
    release_zip = find_release_zip(release_dir, project_root)
    if release_zip is None:
        print(
            f"⚠ Warning: No ZIP file found in: {release_dir} (or elsewhere in the workspace)."
        )
        return

    open_path_if_exists(release_zip, "release ZIP")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the release workflow locally with act."
    )
    parser.add_argument("--open-release-zip", action="store_true")
    parser.add_argument("--open-release-dir", action="store_true")
    parser.add_argument("--open-work-dir", action="store_true")
    parser.add_argument("pass_thru_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    project_root = (Path(__file__).resolve().parent / ".." / "..").resolve()
    secret_file = ".LOCAL/.secrets"
    event_file = "ci/act/create-release-event.json"
    workflow = ".github/workflows/create-release.yml"
    release_dir = project_root / ".RELEASE"

    print(f"Project root: {project_root}")

    check_act = subprocess.run(
        ["act", "--version"],
        cwd=str(project_root),
        check=False,
        capture_output=True,
        text=True,
    )

    if check_act.returncode != 0:
        raise RuntimeError("act is not installed. Visit https://nektosact.com/")

    print("🚀 Running act...")

    release_dir.mkdir(parents=True, exist_ok=True)

    container_target = "/github/workspace/.RELEASE"

    cmd = [
        "act",
        "-P",
        "ubuntu-latest=ghcr.io/catthehacker/ubuntu:gh-latest",
        "--env",
        "ACT=true",
        "--env",
        f"ACT_HOST_PROJECT_ROOT={project_root}",
        "--pull=false",
        "--secret-file",
        secret_file,
        "-e",
        event_file,
        "-W",
        workflow,
        "--container-options",
        f"--mount type=bind,source={release_dir.as_posix()},target={container_target}",
        *args.pass_thru_args,
    ]

    result = subprocess.run(cmd, cwd=str(project_root), check=False)
    if result.returncode != 0:
        print(
            f"⚠ Warning: act failed with exit code {result.returncode}. Skipping post-success open actions."
        )
        return result.returncode

    if args.open_release_dir:
        open_path_if_exists(release_dir, "release directory")

    if args.open_release_zip:
        open_release_zip_if_exists(release_dir, project_root)

    if args.open_work_dir:
        open_act_work_dir_if_exists(project_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
