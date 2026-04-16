<#
.SYNOPSIS
Run busted continuously when Lua files change.
.DESCRIPTION
Configures UTF-8 console output and executes `watchexec` to launch `busted`
on each relevant file change.
#>

$env:ANSICON = "ON"
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

watchexec --exts lua --clear=reset busted
