<#
.SYNOPSIS
Remove local coverage and stats artifacts.
.DESCRIPTION
Deletes generated coverage files from the project root, including
`luacov.report.out`, `luacov.stats.out`, `luacov.report.html`, and `lcov.info`.
#>

# Move to the project root directory.
Push-Location (Split-Path -Parent $PSScriptRoot)

# Define the list of files to remove, including the LCOV file for VS Code.
$filesToRemove = "luacov.report.out", "luacov.stats.out", "luacov.report.html", "lcov.info"

# Remove the files only if they exist to avoid red error messages.
Remove-Item -Path $filesToRemove -ErrorAction SilentlyContinue -Force

Write-Output "Cleanup: Coverage and stats files removed."

Pop-Location
