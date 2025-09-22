# Docker Containerization for MCP Server

## Task Description
Need to create a Docker container for MCP (Model Context Protocol) server to simplify deployment and distribution of the solution.

## Current State
Currently MCP server runs locally through Python virtualenv:
```json
{
  "servers": {
    "langchain-mcp": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.virtualenv\\Scripts\\python.exe",
      "args": ["${workspaceFolder}\\mcp_server\\server.py"]
    }
  }
}
```

## Requirements

### 1. Docker Image
- **Image name**: `langchain-mcp:latest`
- **Base image**: Python 3.13.5 (matches local version)
- **Working directory**: `/app/mcp_server`
- **Entry point**: `python server.py`
- **Include**: all mcp_server code, installed dependencies, folder structure

### 2. Volume Mapping
Container should support mounting external folders:
- `.env` file: `host → container` (read-only)
- `config/` folder: bidirectional volume (container creates defaults, host can override)
- `logs/` folder: `container → host` (logging)
- `projects/` folder: bidirectional volume

### 3. Configuration via .env
All paths and settings are passed through environment variables in `.env` file:
- `MCP_CONFIG_PATH` - path to config folder on host
- `MCP_LOGS_PATH` - path to logs folder on host  
- `MCP_PROJECTS_PATH` - path to projects folder on host
- `MCP_PORTS` - list of ports for forwarding (comma-separated, e.g. `8080:8080,9000:9000,9001:9001`)
- All other environment variables (API keys, LLM settings, etc.) also passed through `.env`

### 4. Updated mcp.json
New configuration for Docker launch:
```json
{
  "servers": {
    "langchain-mcp-docker": {
      "type": "stdio",
      "command": "${workspaceFolder}/mcp_server/docker/run.sh",
      "args": ["${workspaceFolder}/.env"]
    }
  }
}
```

**Note**: All Docker configuration (volume mapping, port forwarding, environment variables) is handled internally by the `run.sh` script. The script takes `.env` file path as argument and reads all necessary variables from it.

### 5. Network Communication
- Support for port forwarding for webhook servers and other services
- Ports are determined from environment variables in `.env` file

## Solution Architecture

### File Structure
```
mcp_server/
├── docker/
│   ├── Dockerfile
│   ├── build.sh
│   ├── run.sh
│   ├── .env.template
│   └── README.md
└── ...
```

### Build Process
1. Copy entire project (`mcp_server/`, `install.sh`) to container
2. Install dependencies via `install.sh` inside container
3. Configure `WORKDIR=/app/mcp_server` and `CMD=["python", "server.py"]`
4. Configure `EXPOSE` for standard ports passed from the `.env` file via `MCP_PORTS` as a list separated by the `,` character.

### Launch Process
1. VS Code calls `run.sh` script with `.env` file path
2. Script reads all variables from `.env` file
3. Script internally handles volume mapping and port forwarding
4. Docker container starts with MCP server
5. VS Code connects to container via stdio

## Project Goals
- **Easy deployment**: single Docker image contains everything needed
- **Portability**: works on any servers with Docker
- **Configuration flexibility**: setup via .env file
- **Compatibility**: works with existing VS Code MCP client
- **Data persistence**: preserve `config/logs/projects` between restarts

## Expected Result
After implementation user will be able to:
1. Build Docker image: `cd mcp_server/docker && ./build.sh`
2. Configure `.env` file with paths and ports (based on .env.template)
3. Update `mcp.json` to use Docker variant
4. Run MCP server in container: VS Code connects to container via stdio
5. Use all existing tools (webhook, telegram, file operations, etc.)

## Additional Requirements
- All artifacts in the `mcp_server/docker` folder
- Build and setup documentation (`README.md` in `docker/ folder`)
- `.env` file template (`.env.template`) with examples of all variables
- Scripts for build automation (`build.sh`) and launch (`run.sh`) 
- Compatibility with existing functionality of all `lng_*` tools
- Support for both Windows and Linux paths in volume mapping
- Verify stdio interface works with VS Code through Docker

## MCP Technical Features
- **Stdio protocol**: MCP uses standard input/output streams for communication
- **JSON-RPC**: All messages are passed in JSON-RPC format via stdin/stdout
- **Interactivity**: Container must support interactive mode (-i flag)
- **No TTY**: MCP doesn't require pseudo-terminal, only -i flag

## Important Limitations
- Container must be stateless (state stored in volumes)
- All secrets only through `.env` file (don't embed in image)
- Support fast container restart when code changes
- Compatibility with existing paths and configurations
