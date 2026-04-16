import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run_gh(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete draft GitHub releases named or tagged v0.0.0-act."
    )
    parser.add_argument("github_repository", help="Format: OWNER/REPO")
    parser.add_argument("--tag", default="v0.0.0-act")
    args = parser.parse_args()

    print(
        f"🔍 Searching for {args.tag} drafts in: {args.github_repository}", flush=True
    )

    if shutil.which("gh") is None:
        raise RuntimeError("GitHub CLI (gh) not found.")

    project_root = Path(__file__).resolve().parent.parent

    list_result = run_gh(
        [
            "gh",
            "release",
            "list",
            "--repo",
            args.github_repository,
            "--json",
            "tagName,name,isDraft",
        ],
        project_root,
    )
    if list_result.returncode != 0:
        stderr = (list_result.stderr or "").strip()
        raise RuntimeError(
            '"gh release list" failed. You may need to run "gh auth login" or check your GITHUB_TOKEN.'
            + (f" Details: {stderr}" if stderr else "")
        )

    releases = json.loads(list_result.stdout or "[]")
    drafts_to_delete = [
        release
        for release in releases
        if release.get("isDraft")
        and (release.get("name") == args.tag or release.get("tagName") == args.tag)
    ]

    if not drafts_to_delete:
        print(f"✅ No draft releases named {args.tag} found.", flush=True)
        return 0

    for release in drafts_to_delete:
        target = release.get("tagName") or release.get("name")
        if not target:
            continue
        print(f"🧹 Deleting draft release: {target}", flush=True)
        delete_result = run_gh(
            [
                "gh",
                "release",
                "delete",
                target,
                "--repo",
                args.github_repository,
                "--yes",
            ],
            project_root,
        )
        if delete_result.returncode != 0:
            stderr = (delete_result.stderr or "").strip()
            raise RuntimeError(
                f'"gh release delete" failed for {target}.'
                + (f" Details: {stderr}" if stderr else "")
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
