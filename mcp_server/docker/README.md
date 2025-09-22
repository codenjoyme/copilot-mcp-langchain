# MCP Server Docker Setup

This directory contains Docker configuration for running the MCP (Model Context Protocol) server in a containerized environment.

## Quick Start

### 1. Build the Docker Image

**Linux/macOS/WSL:**
```bash
cd mcp_server/docker
./build.sh
```

**Windows PowerShell:**
```powershell
cd mcp_server\docker
.\build.ps1
```

### 2. Configure Environment

Copy the template and customize your settings:
```bash
cp .env.template ../../.env
# Edit .env with your configuration
```

### 3. Update VS Code Configuration

Add to your `.vscode/mcp.json`:

**Linux/macOS/WSL:**
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

**Windows:**
```json
{
  "servers": {
    "langchain-mcp-docker": {
      "type": "stdio",
      "command": "powershell.exe",
      "args": ["-File", "${workspaceFolder}\\mcp_server\\docker\\run.ps1", "${workspaceFolder}\\.env"]
    }
  }
}
```

### 4. Test the Setup

**Linux/macOS/WSL:**
```bash
./run.sh /path/to/your/.env
```

**Windows PowerShell:**
```powershell
.\run.ps1 C:\path\to\your\.env
```

## Files Overview

- **`Dockerfile`** - Docker image definition
- **`build.sh`** / **`build.ps1`** - Automated build scripts (Linux/Windows)
- **`run.sh`** / **`run.ps1`** - Container launch scripts (called by VS Code)
- **`.env.template`** - Configuration template
- **`README.md`** - This documentation

## Configuration

### Environment Variables (.env)

The container is configured via environment variables in your `.env` file:

#### Required Variables
```bash
# Volume paths (absolute paths on host)
MCP_CONFIG_PATH=/path/to/config
MCP_LOGS_PATH=/path/to/logs  
MCP_PROJECTS_PATH=/path/to/projects

# Port forwarding (comma-separated host:container pairs)
MCP_PORTS=8080:8080,9000:9000,9001:9001
```

#### Optional Variables
All other environment variables (API keys, service configurations, etc.) are passed through to the container.

### Volume Mapping

The container mounts three host directories:

- **config/** - Tool configurations (bidirectional)
- **logs/** - Application logs (container → host)  
- **projects/** - Project-specific data (bidirectional)

### Port Forwarding

Services running inside the container (webhooks, HTTP servers, etc.) can be accessed from the host via port mappings specified in `MCP_PORTS`.

## Development Workflow

### Building Changes
```bash
# Rebuild image after code changes
./build.sh
```

### Debugging
```bash
# Check container logs
docker logs <container_id>

# Interactive container access
docker run -it --rm langchain-mcp:latest /bin/bash
```

### VS Code Integration

The `run.sh` script is designed to work seamlessly with VS Code's MCP client:

1. VS Code calls `run.sh` with `.env` file path
2. Script reads configuration and starts container
3. VS Code communicates with container via stdin/stdout
4. Container automatically stops when VS Code disconnects

## Troubleshooting

### Common Issues

**Build fails with "file not found":**
- Ensure you're running `build.sh` from `mcp_server/docker/` directory
- Check that `../mcp_server/` and `../install.sh` exist

**Container won't start:**
- Verify `.env` file exists and contains required variables
- Check that host directories in volume mappings exist
- Ensure Docker is running

**VS Code can't connect:**
- Verify `mcp.json` configuration
- Check that `run.sh` has execute permissions: `chmod +x run.sh`
- Test manual run: `./run.sh /path/to/.env`

**Port conflicts:**
- Adjust `MCP_PORTS` in `.env` to use different host ports
- Check for other services using the same ports

### Windows-Specific Notes

- Use forward slashes in paths: `C:/path/to/folder`
- Docker Desktop must be running
- WSL2 backend recommended for best performance

### Path Conversion

The `run.sh` script automatically converts Windows paths (C:\path) to Docker-compatible format (/c/path).

## Architecture

```
Host Machine                Container
├── .env              →     Environment Variables
├── config/           ↔     /app/mcp_server/config/
├── logs/             ←     /app/mcp_server/logs/
├── projects/         ↔     /app/mcp_server/projects/
└── ports:8080        ↔     container:8080
```

## Security Considerations

- **Secrets**: All sensitive data (API keys, tokens) stay in `.env` file on host
- **Read-only**: Environment file is mounted read-only in container
- **Isolation**: Container runs without privileged access
- **Stateless**: No persistent state in container itself

## Performance Tips

- Use `.dockerignore` to exclude unnecessary files from build context
- Regular cleanup: `docker system prune`
- Monitor resource usage: `docker stats langchain-mcp`
