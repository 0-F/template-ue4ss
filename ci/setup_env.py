import argparse
import os
import re
from pathlib import Path


def compute_values(
    github_ref_name: str, github_repository: str, script_dir: Path
) -> dict[str, str]:
    project_root_dir = str((script_dir / "..").resolve())
    version = re.sub(r"^v(?=\d+\.\d+\.\d+)", "", github_ref_name)
    repo_owner, repo_name = github_repository.split("/", 1)

    temp_name_dir = ".TEMP"
    release_name_dir = ".RELEASE"
    resources_name_dir = "resources"
    target_dir = str(Path(release_name_dir) / repo_name)
    release_filename = f"{repo_name}.zip"
    release_rel_path = str(Path(release_name_dir) / release_filename)

    return {
        "PROJECT_ROOT_DIR": project_root_dir,
        "VERSION": version,
        "REPO_OWNER": repo_owner,
        "REPO_NAME": repo_name,
        "GITHUB_REPOSITORY": github_repository,
        "RESOURCES_NAME_DIR": resources_name_dir,
        "TEMP_NAME_DIR": temp_name_dir,
        "RELEASE_NAME_DIR": release_name_dir,
        "TARGET_DIR": target_dir,
        "RELEASE_FILENAME": release_filename,
        "RELEASE_REL_PATH": release_rel_path,
    }


def export_values(values: dict[str, str]) -> None:
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a", encoding="utf-8") as f:
            for key, value in values.items():
                f.write(f"{key}={value}\n")
    else:
        os.environ.update(values)


def ensure_dirs(values: dict[str, str], cwd: Path) -> None:
    for dir_name in (
        values["RESOURCES_NAME_DIR"],
        values["TEMP_NAME_DIR"],
        values["RELEASE_NAME_DIR"],
    ):
        directory = cwd / dir_name
        if not directory.exists():
            print(f"📁 Create directory: {dir_name}")
            directory.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize release-related environment variables."
    )
    parser.add_argument("github_ref_name")
    parser.add_argument("github_repository")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = (script_dir / "..").resolve()

    print(f"github_ref_name: {args.github_ref_name}")
    print(f"github_repository: {args.github_repository}")

    values = compute_values(args.github_ref_name, args.github_repository, script_dir)
    export_values(values)
    ensure_dirs(values, project_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
