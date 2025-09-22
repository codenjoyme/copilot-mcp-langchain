#!/bin/bash

# MCP Server Docker Run Script  
# Launches the langchain-mcp container with proper configuration

set -e  # Exit on any error

# Function to handle errors (similar to PowerShell try-catch)
handle_error() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        print_error "Run failed with exit code: $exit_code"
        exit $exit_code
    fi
}

# Set up error trap
trap 'handle_error' ERR

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect if running in MCP mode (no terminal attached)
is_mcp_mode() {
    [[ ! -t 0 && ! -t 1 ]]
}

print_step() {
    echo -e "${BLUE}[RUN]${NC} $1" >&2
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

print_debug() {
    if ! is_mcp_mode; then
        echo -e "${BLUE}[DEBUG]${NC} $1" >&2
    fi
}

# Check arguments
if [[ $# -ne 1 ]]; then
    print_error "Usage: $0 <path_to_env_file>"
    print_error "Example: $0 /path/to/your/.env"
    exit 1
fi

# Detect if we're running on Windows (Git Bash/WSL)
is_windows() {
    [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "$WINDIR" || -n "$WSL_DISTRO_NAME" ]]
}

# Detect if we're running in Git Bash on Windows
is_git_bash() {
    [[ "$OSTYPE" == "msys" ]]
}

# Detect if we're running in WSL
is_wsl() {
    [[ -n "$WSL_DISTRO_NAME" ]]
}

# Convert path for Docker volume mapping
convert_path_for_docker() {
    local path="$1"
    
    if is_git_bash; then
        # Git Bash: Keep Windows-style paths for Docker Desktop
        # Convert forward slashes back to backslashes and ensure proper format
        if [[ "$path" =~ ^/[a-z]/ ]]; then
            # Convert /c/path/to/file back to C:/path/to/file
            echo "$path" | sed 's|^/\([a-z]\)/|\U\1:/|' 
        elif [[ "$path" =~ ^[A-Za-z]: ]]; then
            # Already Windows format, just normalize slashes
            echo "$path" | sed 's|\\|/|g'
        else
            echo "$path"
        fi
    elif is_wsl; then
        # WSL: Convert Windows paths to WSL format
        if [[ "$path" =~ ^[A-Za-z]: ]]; then
            # Convert C:\path to /mnt/c/path
            echo "$path" | sed 's|^\([A-Za-z]\):|/mnt/\L\1|' | sed 's|\\|/|g'
        else
            echo "$path"
        fi
    else
        # Pure Linux: use as is
        echo "$path"
    fi
}

# Convert Windows path to Unix format for file operations
convert_windows_path() {
    local path="$1"
    if is_windows && [[ "$path" =~ ^[A-Za-z]:.*$ ]]; then
        # Convert C:\path\to\file to /c/path/to/file (for Git Bash file operations)
        echo "$path" | sed 's|^\([A-Za-z]\):|/\L\1|' | sed 's|\\|/|g'
    else
        echo "$path"
    fi
}

ENV_FILE=$(convert_windows_path "$1")

# Validate .env file exists
if [[ ! -f "$ENV_FILE" ]]; then
    print_error ".env file not found: $ENV_FILE"
    if is_windows; then
        print_error "Note: Running on Windows - paths should use forward slashes in bash"
        print_error "Original path: $1"
        print_error "Converted path: $ENV_FILE"
    fi
    exit 1
fi

print_step "Starting MCP Server Docker container..."
print_step "Using .env file: $ENV_FILE"
if is_windows; then
    print_step "Detected Windows environment - converting paths for Docker compatibility"
fi

# Check if Docker is running
if ! docker version >/dev/null 2>&1; then
    print_error "Docker is not running or not accessible"
    print_error "Please start Docker Desktop and try again"
    exit 1
fi

# Check if Docker image exists
if ! docker image inspect langchain-mcp:latest >/dev/null 2>&1; then
    print_error "Docker image 'langchain-mcp:latest' not found"
    print_error "Please build the image first using: build.sh or build.ps1"
    exit 1
fi

# Function to read .env file (similar to PowerShell version)
read_env_file() {
    local file_path="$1"
    declare -gA env_vars
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip empty lines and comments
        [[ "$line" =~ ^[[:space:]]*$ || "$line" =~ ^[[:space:]]*# ]] && continue
        
        # Match KEY=VALUE pattern
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local value="${BASH_REMATCH[2]}"
            # Remove quotes if present
            value=$(echo "$value" | sed 's/^["\'"'"']//' | sed 's/["\'"'"']$//')
            env_vars["$key"]="$value"
        fi
    done < "$file_path"
}

# Read .env file into associative array
read_env_file "$ENV_FILE"

# Validate required variables
required_vars=("MCP_CONFIG_PATH" "MCP_LOGS_PATH" "MCP_PROJECTS_PATH")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [[ -z "${env_vars[$var]:-}" ]]; then
        missing_vars+=("$var")
    fi
done

if [[ ${#missing_vars[@]} -gt 0 ]]; then
    print_error "Missing required variables in .env file:"
    for var in "${missing_vars[@]}"; do
        print_error "  $var"
    done
    exit 1
fi

# Convert paths for Docker compatibility using env_vars array
DOCKER_CONFIG_PATH=$(convert_path_for_docker "${env_vars[MCP_CONFIG_PATH]}")
DOCKER_LOGS_PATH=$(convert_path_for_docker "${env_vars[MCP_LOGS_PATH]}")
DOCKER_PROJECTS_PATH=$(convert_path_for_docker "${env_vars[MCP_PROJECTS_PATH]}")

print_step "Volume mappings:"
if is_windows; then
    print_step "  Environment: $(if is_git_bash; then echo "Git Bash"; elif is_wsl; then echo "WSL"; else echo "Windows"; fi)"
    print_step "  Config: ${env_vars[MCP_CONFIG_PATH]} -> $DOCKER_CONFIG_PATH -> /app/mcp_server/config"
    print_step "  Logs: ${env_vars[MCP_LOGS_PATH]} -> $DOCKER_LOGS_PATH -> /app/mcp_server/logs"
    print_step "  Projects: ${env_vars[MCP_PROJECTS_PATH]} -> $DOCKER_PROJECTS_PATH -> /app/mcp_server/projects"
else
    print_step "  Environment: Linux"
    print_step "  Config: $DOCKER_CONFIG_PATH -> /app/mcp_server/config"
    print_step "  Logs: $DOCKER_LOGS_PATH -> /app/mcp_server/logs"
    print_step "  Projects: $DOCKER_PROJECTS_PATH -> /app/mcp_server/projects"
fi

# Initialize host directories with content from container if they're empty
print_step "Initializing host directories..."

# Create host directories if they don't exist (use original paths for mkdir)
mkdir -p "${env_vars[MCP_CONFIG_PATH]}" "${env_vars[MCP_LOGS_PATH]}" "${env_vars[MCP_PROJECTS_PATH]}"

if is_windows; then
    print_step "Created directories using original Windows paths"
fi

# Check if config directory is empty and copy defaults from container
config_files=$(find "${env_vars[MCP_CONFIG_PATH]}" -mindepth 1 2>/dev/null | wc -l)
if [[ $config_files -eq 0 ]]; then
    print_step "Config directory is empty, copying defaults from container..."
    temp_args=(
        "run" "--rm"
        "-v" "${DOCKER_CONFIG_PATH}:/host/config"
        "langchain-mcp:latest"
        "sh" "-c" "cp -r /app/mcp_server/config/* /host/config/ 2>/dev/null || cp -r /app/templates/config/* /host/config/ 2>/dev/null || echo 'No default config found'"
    )
    docker "${temp_args[@]}" >/dev/null
    print_success "Config directory initialized"
fi

# Check if projects directory is empty and copy defaults from container
project_files=$(find "${env_vars[MCP_PROJECTS_PATH]}" -mindepth 1 2>/dev/null | wc -l)
if [[ $project_files -eq 0 ]]; then
    print_step "Projects directory is empty, copying defaults from container..."
    temp_args=(
        "run" "--rm"
        "-v" "${DOCKER_PROJECTS_PATH}:/host/projects"
        "langchain-mcp:latest"
        "sh" "-c" "cp -r /app/mcp_server/projects/* /host/projects/ 2>/dev/null || cp -r /app/templates/projects/* /host/projects/ 2>/dev/null || echo 'No default projects found'"
    )
    docker "${temp_args[@]}" >/dev/null
    print_success "Projects directory initialized"
fi

# Build Docker run command arguments (similar to PowerShell version)
if is_mcp_mode; then
    # MCP mode: minimal output, clean stdio
    docker_args=(
        "run" "--rm" "-i"
        "--env-file" "$ENV_FILE"
        "-v" "${DOCKER_CONFIG_PATH}:/app/mcp_server/config"
        "-v" "${DOCKER_LOGS_PATH}:/app/mcp_server/logs"
        "-v" "${DOCKER_PROJECTS_PATH}:/app/mcp_server/projects"
    )
else
    # Interactive mode: can use TTY
    docker_args=(
        "run" "--rm" "-it"
        "--env-file" "$ENV_FILE"
        "-v" "${DOCKER_CONFIG_PATH}:/app/mcp_server/config"
        "-v" "${DOCKER_LOGS_PATH}:/app/mcp_server/logs"
        "-v" "${DOCKER_PROJECTS_PATH}:/app/mcp_server/projects"
    )
fi

# Handle port mappings from MCP_PORTS
if [[ -n "${env_vars[MCP_PORTS]:-}" ]]; then
    print_step "Port mappings: ${env_vars[MCP_PORTS]}"
    IFS=',' read -ra PORTS <<< "${env_vars[MCP_PORTS]}"
    for port in "${PORTS[@]}"; do
        # Trim whitespace
        port=$(echo "$port" | xargs)
        if [[ -n "$port" ]]; then
            docker_args+=("-p" "$port")
        fi
    done
else
    print_warning "No MCP_PORTS specified, no ports will be forwarded"
fi

# Add image name
docker_args+=("langchain-mcp:latest")

# Check if debug mode is requested
if [[ "${env_vars[MCP_DEBUG]:-}" == "true" ]]; then
    print_step "Debug mode enabled - running container interactively"
    docker_args+=("--entrypoint" "bash")
    docker "${docker_args[@]}"
else
    print_step "Executing Docker command..."
    print_step "Container ready for MCP communication via stdio"
    print_step "Docker args: ${docker_args[*]}"
    
    # Execute the Docker command using array expansion (safer than eval)
    exec docker "${docker_args[@]}"
fi
