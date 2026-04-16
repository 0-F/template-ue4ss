<#
.SYNOPSIS
Apply a local fix for luacov HTML reporter static assets.
.DESCRIPTION
Copies the `src` directory from the installed luacov rock path to the reporter
path used by LuaRocks/Scoop, as a workaround for missing HTML assets.
#>

# https://github.com/lunarmodules/luacov/issues/122

$scoopPath = "$env:USERPROFILE\scoop"

$realPath = "$scoopPath\apps\luarocks\current\rocks\lib\luarocks\rocks-5.4\luacov\0.17.0-1\src"
$buggedPath = "$scoopPath\apps\luarocks\current\rocks\share\lua\5.4\luacov\reporter\src"

Copy-Item -Path $realPath -Destination $buggedPath -Recurse -Force

Write-Output "Patch applied! luacov HTML reporter should now find its static assets."
