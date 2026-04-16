import os
import re
import subprocess
import sys
from pathlib import Path


def main():
    repo_owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "")
    script_to_execute = "script.py"

    if len(sys.argv) > 1:
        repo_owner = sys.argv[1]
    if len(sys.argv) > 2:
        script_to_execute = sys.argv[2]

    if Path(script_to_execute).suffix != ".py":
        raise ValueError(
            f"Only Python game-specific scripts are supported, got: {script_to_execute}"
        )

    script_dir = Path(__file__).parent.resolve()
    parent_dir = script_dir.parent
    print(f"VERBOSE: Changing location to {parent_dir}")
    os.chdir(parent_dir)

    match = re.search(r"-([^-]+)-mods", repo_owner)
    if match:
        game_name = match.group(1)
        print(f"🕹️ Run custom script for the game: {game_name}")

        game_name_lower = game_name.lower()
        github_env = os.environ.get("GITHUB_ENV")
        if github_env:
            with open(github_env, "a", encoding="utf-8") as f:
                f.write(f"GAME_NAME={game_name_lower}\n")
        else:
            print("🟡 GITHUB_ENV not set, unable to export variable.")

        script_path = Path("games") / game_name_lower / "ci" / script_to_execute

        if script_path.exists():
            print(
                f"🚀 Executing custom script '{script_to_execute}' for the game ({game_name}): {script_path}"
            )
            try:
                subprocess.run([sys.executable, str(script_path)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Script failed with exit code {e.returncode}")
                sys.exit(e.returncode)
        else:
            print(
                f"Custom script ({script_to_execute}) for the game '{game_name}' does not exist. scriptPath: {script_path}"
            )
    else:
        print(f"🟡 Cannot get the game name from repository owner: {repo_owner}")


if __name__ == "__main__":
    main()
