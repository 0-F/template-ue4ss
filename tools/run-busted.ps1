<#
.SYNOPSIS
Run busted continuously with watchexec.
.DESCRIPTION
Configures UTF-8 console output and launches `watchexec` to rerun `busted` when
Lua files change.
#>

$env:ANSICON = "ON"
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
watchexec -e lua --clear reset busted
