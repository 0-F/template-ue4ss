<#
.SYNOPSIS
Open a new Windows Terminal tab with a custom title and working directory.
.DESCRIPTION
Starts `wt` with a preconfigured PowerShell session, preserving UTF-8 output
settings for tooling in this repository.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [Parameter(Mandatory = $true)]
    [string]$WorkDir
)

$argList = @(
    "--title", $Title,
    "-d", $WorkDir,
    "pwsh.exe",
    "-NoExit",
    "-Command",
    "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8"
)

Start-Process -FilePath "wt" -ArgumentList $argList
