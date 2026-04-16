"""
Generate a list of release files and export as env var RELEASE_FILES_LIST.

Scans a release directory for files, prints them, and exports a semicolon-separated
list to the environment (and to GITHUB_ENV for CI). Returns non-zero if the
release directory does not exist.
"""

import os
from pathlib import Path


def main() -> int:
    project_root_dir = os.environ.get("PROJECT_ROOT_DIR", "")
    release_dir_name = os.environ.get("RELEASE_NAME_DIR", "")
    release_dir = Path(project_root_dir) / release_dir_name

    print(f"🔍 Searching for release files in: {release_dir}")

    if not release_dir.exists():
        print(f"⚠ Release directory does not exist: {release_dir}")
        return 1

    file_list = [str(p.resolve()) for p in release_dir.iterdir() if p.is_file()]
    if not file_list:
        print("No files found.")
        os.environ["RELEASE_FILES_LIST"] = ""
        github_env = os.environ.get("GITHUB_ENV")
        if github_env:
            with open(github_env, "a", encoding="utf-8") as f:
                f.write("RELEASE_FILES_LIST=\n")
        return 0

    files_string = ",".join(file_list)
    print("Detected files:")
    for file_path in file_list:
        print(f" - {Path(file_path).name}")

    os.environ["RELEASE_FILES_LIST"] = files_string
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a", encoding="utf-8") as f:
            f.write(f"RELEASE_FILES_LIST={files_string}\n")

    print(
        "✅ Local environment variable 'RELEASE_FILES_LIST' has been set for this session."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
