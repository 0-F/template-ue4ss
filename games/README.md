## Games folder

This folder is used for game-specific overrides and custom files.

Each subfolder inside `games/` should represent a single game and may contain assets, configuration,
or that apply to that game.

In particular, the release workflow can look for an optional script at:
`games/<GAME_NAME>/ci/create_release.py`

If that script exists, it is executed to create an additional game-specific release step without
affecting the default template behavior.

Use this folder when a game needs custom logic while keeping the shared template generic and
reusable.
