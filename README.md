# UE4SS mod

## First steps

Run the setup script to generate your local development environment:

```powershell
.\tools\init.ps1
```

## Python scripts

This project uses `uv` to run Python scripts and manage the local Python environment.\
Website: https://docs.astral.sh/uv/

## Tools installation

### Using Scoop (Windows)
`Scoop` is a command-line installer for Windows that simplifies the installation of tools.\
Website: https://scoop.sh/

```shell
scoop install lua
scoop install luarocks
scoop install watchexec
luarocks install busted
luarocks install luacov
luarocks install luacov-reporter-lcov
```

## Other tools

### ScopedSort

Website: https://scopedsort.netlify.app/

There are `npm` scripts in `package.json` for this tool.

ScopedSort sorts code between these comments:

```lua
-- { sort-start ... }
-- { sort-end }
```

## `ci/release-files.txt`

The `ci/release-files.txt` file defines which project files and folders are copied into the release
directory before the ZIP archive is created.

Each line represents a path relative to the project root.

Example:

```text
Scripts/
options.example.lua
```

In this example:
- `Scripts/` includes the entire `Scripts` directory
- `options.example.lua` includes that file from the project root

Usage rules:
- put one path on each line
- use paths relative to the project root
- end directory entries with `/` if you want to make them explicit
- do not add automatically generated files such as `enabled.txt` or `version.txt`; the release
  script creates them

If a listed path does not exist, release creation fails to avoid producing an incomplete or
incorrect archive.
