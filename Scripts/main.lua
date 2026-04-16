local logging = require("lib.lua-mods-libs.logging")
local format = string.format

local modInfo = (function()
    local info = debug.getinfo(2, "S")
    local source = info.source:gsub("\\", "/")
    return {
        name = source:match("@?.+/([^/]+)/[Ss]cripts/"),
        file = source:sub(2),
        currentDirectory = source:match("@?(.+)/"),
        currentModDirectory = source:match("@?(.+)/[Ss]cripts/"),
        modsDirectory = source:match("@?(.+)/[^/]+/[Ss]cripts/"),
    }
end)()

---@param filename string
---@return boolean
local function doesFileExist(filename)
    local file = io.open(filename, "r")
    if file ~= nil then
        io.close(file)
        return true
    else
        return false
    end
end

---@return MOD_OPTIONS
local function loadOptions()
    local file = format([[%s\options.lua]], modInfo.currentModDirectory)

    if not doesFileExist(file) then
        local cmd = format(
            [[copy "%s\options.example.lua" "%s\options.lua"]],
            modInfo.currentModDirectory,
            modInfo.currentModDirectory
        )

        print("Copy example options to options.lua. Execute command: " .. cmd .. "\n")

        os.execute(cmd)
    end

    return dofile(file)
end

---@return table
local function loadDevOptions()
    local file = format([[%s\options.dev.lua]], modInfo.currentModDirectory)

    if doesFileExist(file) then
        return dofile(file)
    end

    return {}
end

---@param base table
---@param override table
local function mergeOptions(base, override)
    for k, v in pairs(override) do
        if type(v) == "table" and type(base[k]) == "table" then
            mergeOptions(base[k], v)
        else
            base[k] = v
        end
    end
end

--------------------------------------------------------------------------------

local options = loadOptions()
local devOptions = loadDevOptions() or {}
mergeOptions(options, devOptions)
_G.Options = options

-- Default logging levels. They can be overwritten in the options file.
_G.LOG_LEVEL = _G.LOG_LEVEL or "INFO" ---@type _LogLevel
_G.MIN_LEVEL_OF_FATAL_ERROR = _G.MIN_LEVEL_OF_FATAL_ERROR or "ERROR" ---@type _LogLevel
_G.Log = logging.new(_G.LOG_LEVEL, _G.MIN_LEVEL_OF_FATAL_ERROR)
local log = _G.Log

--------------------------------------------------------------------------------
