<#
.SYNOPSIS
Run tests with coverage and generate text plus LCOV reports.
.DESCRIPTION
Executes `busted --coverage`, produces `lcov.info` for editor integrations, and
generates the standard luacov text report.
#>

Push-Location (Split-Path -Parent $PSScriptRoot)
$env:ANSICON = 'ON'
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Remove-Item -Path luacov.stats.out -ErrorAction SilentlyContinue
busted --coverage

# Generate lcov.info for Coverage Gutters.
# https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters
luacov -r lcov
Move-Item -Path luacov.report.out -Destination lcov.info -Force

luacov
Pop-Location
