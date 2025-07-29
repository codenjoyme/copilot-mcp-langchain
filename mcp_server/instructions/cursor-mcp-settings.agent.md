- Links contains `{workspaceFolder}` which should be replaced with absolute path to the project.

- **For Windows:**
```json
{
  "mcpServers": {
    "langchain-mcp":{
        "type": "stdio",
        "command": "C:\\Java\\CopipotTraining\\hello-langchain\\.virtualenv\\Scripts\\python.exe",
        "args": ["C:\\Java\\CopipotTraining\\hello-langchain\\mcp_server\\server.py"]
    }
  }
}
```

- **For macOS/Linux:**
```json
{
  "mcpServers": {
    "langchain-mcp":{
        "type": "stdio",
        "command": "/Users/username/copilot-mcp-langchain/.virtualenv/bin/python",
        "args": ["/Users/username/copilot-mcp-langchain/mcp_server/server.py"]
    }
  }
}
```

- **Quick Setup:**
  - **Windows:** Use `.cursor/mcp.json` (Windows paths with backslashes)
  - **macOS/Linux:** Use `.cursor/mcp-macos.json` (Unix paths with forward slashes)