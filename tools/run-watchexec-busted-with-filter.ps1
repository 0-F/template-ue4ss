<#
.SYNOPSIS
Run filtered busted tests continuously with watchexec.
.DESCRIPTION
Configures UTF-8 console output and watches Lua files.
#>

$env:ANSICON = "ON"
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

watchexec $argsList --watch . --watch tools/busted-filter.txt `
    --exts lua --clear=reset tools/run-busted-with-filter.ps1
