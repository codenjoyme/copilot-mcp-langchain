#!/bin/bash

# MCP Server Docker Build Script
# Builds the langchain-mcp Docker image

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step "Starting MCP Server Docker build process..."

# Check if we're in the correct directory
if [[ ! -f "Dockerfile" ]]; then
    print_error "Dockerfile not found! Please run this script from mcp_server/docker directory"
    exit 1
fi

# Check if parent directories exist
if [[ ! -f "../server.py" ]]; then
    print_error "../server.py file not found!"
    exit 1
fi

if [[ ! -f "../../install.sh" ]]; then
    print_error "../../install.sh file not found!"
    exit 1
fi

# Look for .env file to get ports for EXPOSE
ENV_FILE=""
EXPOSE_PORTS=""

# Check for .env file in common locations
for env_path in "../../.env" "../../../.env" ".env.template"; do
    if [[ -f "$env_path" ]]; then
        ENV_FILE="$env_path"
        break
    fi
done

if [[ -n "$ENV_FILE" ]]; then
    print_step "Found .env file: $ENV_FILE"
    
    # Extract MCP_PORTS from .env file
    if grep -q "^MCP_PORTS=" "$ENV_FILE"; then
        MCP_PORTS=$(grep "^MCP_PORTS=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
        
        if [[ -n "$MCP_PORTS" ]]; then
            # Parse ports from MCP_PORTS (format: "8080:8080,9000:9000,9001:9001")
            IFS=',' read -ra PORT_PAIRS <<< "$MCP_PORTS"
            EXPOSE_PORTS_ARRAY=()
            
            for pair in "${PORT_PAIRS[@]}"; do
                # Extract container port (after colon)
                if [[ "$pair" == *":"* ]]; then
                    container_port=$(echo "$pair" | cut -d':' -f2 | xargs)
                else
                    container_port=$(echo "$pair" | xargs)
                fi
                
                if [[ "$container_port" =~ ^[0-9]+$ ]]; then
                    EXPOSE_PORTS_ARRAY+=("$container_port")
                fi
            done
            
            EXPOSE_PORTS=$(IFS=' '; echo "${EXPOSE_PORTS_ARRAY[*]}")
            print_step "Ports to expose: $EXPOSE_PORTS"
        fi
    fi
else
    print_warning "No .env file found, using default ports: 8000 8080 9000 9001"
    EXPOSE_PORTS="8000 8080 9000 9001"
fi

# Build Docker image
IMAGE_NAME="langchain-mcp"
TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

print_step "Building Docker image: ${FULL_IMAGE_NAME}"
print_step "This may take several minutes..."

# Build arguments
BUILD_ARGS=()
if [[ -n "$EXPOSE_PORTS" ]]; then
    BUILD_ARGS+=(--build-arg "EXPOSE_PORTS=$EXPOSE_PORTS")
fi

print_step "Running Docker build with arguments: ${BUILD_ARGS[*]}"

# Execute Docker build with detailed output settings
print_step "Executing Docker build..."

# Build with clean output flags for better visibility
DOCKER_ARGS=(
    "build"
    "--progress=plain"      # Plain text output instead of interactive
    "--no-cache"           # Force fresh build to see all output
    "-t" "${FULL_IMAGE_NAME}"
    "-f" "Dockerfile"
)

# Add build args if any
if [[ ${#BUILD_ARGS[@]} -gt 0 ]]; then
    DOCKER_ARGS+=("${BUILD_ARGS[@]}")
fi

# Add build context
DOCKER_ARGS+=("../..")

print_step "Using --progress=plain for clean output (no progress bars)"
print_step "Build command: docker ${DOCKER_ARGS[*]}"

# Execute Docker build
if docker "${DOCKER_ARGS[@]}"; then
    print_success "Docker image built successfully: ${FULL_IMAGE_NAME}"
else
    print_error "Docker build failed with exit code: $?"
    exit 1
fi

# Display image information
print_step "Image information:"
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

print_success "Build completed!"
print_step "Next steps:"
echo "  1. Copy .env.template to your project root as .env and configure it"
echo "  2. Update your .vscode/mcp.json to use Docker configuration"
echo "  3. Test the container with: ./run.sh /path/to/your/.env"

print_step "To rebuild the image later, run this script again"
