import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def run_gh(
    cmd: list[str], env: dict[str, str] | None, cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def parse_github_repository(repository_url: str) -> str:
    repository_url = repository_url.strip()
    if not repository_url:
        raise ValueError('The "repositoryUrl" field in mod.json is empty.')

    if repository_url.startswith("git@github.com:"):
        repository_path = repository_url.removeprefix("git@github.com:")
    else:
        parsed_url = urlparse(repository_url)
        if parsed_url.netloc.lower() != "github.com":
            raise ValueError(
                f'Unsupported repositoryUrl host: "{parsed_url.netloc}". Expected github.com.'
            )
        repository_path = parsed_url.path.lstrip("/")

    repository_path = repository_path.removesuffix(".git").strip("/")
    parts = [part for part in repository_path.split("/") if part]
    if len(parts) < 2:
        raise ValueError(
            f'Could not extract "owner/repo" from repositoryUrl: "{repository_url}".'
        )

    return "/".join(parts[:2])


def load_github_repository(project_root: Path) -> str:
    mod_json_path = project_root / "mod.json"
    with open(mod_json_path, encoding="utf-8") as f:
        mod_metadata = json.load(f)

    repository_url = str(mod_metadata.get("repositoryUrl", "")).strip()
    if not repository_url:
        raise ValueError('The "repositoryUrl" field is missing or empty in mod.json.')

    return parse_github_repository(repository_url)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Delete draft GitHub release(s) for a given tag using "gh".'
    )
    parser.add_argument("--tag", default="v0.0.0-act")
    args = parser.parse_args()

    if shutil.which("gh") is None:
        raise RuntimeError('GitHub CLI "gh" is not installed or not in PATH.')

    project_root = Path(__file__).resolve().parent.parent
    env = None

    github_repository = load_github_repository(project_root)
    print("📦 GitHub repository: " + github_repository)

    list_cmd = [
        "gh",
        "release",
        "list",
        "--repo",
        github_repository,
        "--json",
        "tagName,name,isDraft",
    ]
    list_result = run_gh(list_cmd, env, project_root)
    if list_result.returncode != 0:
        stderr = (list_result.stderr or "").strip()
        raise RuntimeError(
            '"gh release list" failed. Run "gh auth login" (or set GH_TOKEN/GITHUB_TOKEN).'
            + (f" Details: {stderr}" if stderr else "")
        )

    releases = json.loads(list_result.stdout or "[]")
    targets = [
        release
        for release in releases
        if release.get("isDraft")
        and (release.get("tagName") == args.tag or release.get("name") == args.tag)
    ]

    print(f"🔍 Draft releases matching {args.tag!r}: {len(targets)}", flush=True)
    if not targets:
        print("✅ Nothing to delete.", flush=True)
        return 0

    for release in targets:
        target = release.get("tagName") or release.get("name")
        if not target:
            continue
        print(f"🧹 Deleting draft release: {target}", flush=True)
        delete_cmd = [
            "gh",
            "release",
            "delete",
            target,
            "--repo",
            github_repository,
            "--yes",
        ]
        delete_result = run_gh(delete_cmd, env, project_root)
        if delete_result.returncode != 0:
            stderr = (delete_result.stderr or "").strip()
            raise RuntimeError(
                f'"gh release delete" failed for {target}.'
                + (f" Details: {stderr}" if stderr else "")
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
