-- Initialize the Second Local Lua Debugger if enabled via environment variables.
-- See: https://marketplace.visualstudio.com/items?itemName=ismoh-games.second-local-lua-debugger-vscode
if os.getenv("LOCAL_LUA_DEBUGGER_VSCODE") == "1" then
    require("lldebugger").start()
end
