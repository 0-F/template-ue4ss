<#
.SYNOPSIS
Run tests with coverage and generate an HTML luacov report.
.DESCRIPTION
Executes `busted --coverage`, runs luacov with the HTML reporter, then renames
the output to `luacov.report.html`.
#>

Push-Location (Split-Path -Parent $PSScriptRoot)
$env:ANSICON = 'ON'
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Remove-Item -Path luacov.stats.out -ErrorAction SilentlyContinue
busted --coverage
luacov --reporter html
Move-Item -Path luacov.report.out -Destination luacov.report.html -Force
Pop-Location
