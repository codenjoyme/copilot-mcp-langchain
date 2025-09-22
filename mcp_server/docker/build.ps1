# MCP Server Docker Build Script (PowerShell)
# Builds the langchain-mcp Docker image

param()

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output (PowerShell equivalents)
function Write-Step {
    param([string]$Message)
    Write-Host "[BUILD] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

try {
    Write-Step "Starting MCP Server Docker build process..."

    # Check if we're in the correct directory
    if (!(Test-Path "Dockerfile")) {
        Write-Error-Custom "Dockerfile not found! Please run this script from mcp_server/docker directory"
        exit 1
    }

    # Check if parent directories exist
    if (!(Test-Path "../server.py")) {
        Write-Error-Custom "../server.py file not found!"
        exit 1
    }

    if (!(Test-Path "../../install.sh")) {
        Write-Error-Custom "../../install.sh file not found!"
        exit 1
    }

    # Look for .env file to get ports for logging
    $envFile = ""
    $exposePorts = ""

    # Check for .env file in common locations
    $envPaths = @("../../.env", "../../../.env", ".env.template")
    foreach ($envPath in $envPaths) {
        if (Test-Path $envPath) {
            $envFile = $envPath
            break
        }
    }

    if ($envFile) {
        Write-Step "Found .env file: $envFile"
        
        # Extract MCP_PORTS from .env file
        $mcpPorts = Get-Content $envFile | Where-Object { $_ -match "^MCP_PORTS=" } | Select-Object -First 1
        
        if ($mcpPorts) {
            $portsValue = ($mcpPorts -split "=", 2)[1].Trim('"').Trim("'")
            
            if ($portsValue) {
                # Parse ports from MCP_PORTS (format: "8080:8080,9000:9000,9001:9001")
                $portPairs = $portsValue -split ","
                $exposePortsArray = @()
                
                foreach ($pair in $portPairs) {
                    $pair = $pair.Trim()
                    # Extract container port (after colon)
                    if ($pair -match ":") {
                        $containerPort = ($pair -split ":")[1].Trim()
                    } else {
                        $containerPort = $pair
                    }
                    
                    if ($containerPort -match "^\d+$") {
                        $exposePortsArray += $containerPort
                    }
                }
                
                $exposePorts = $exposePortsArray -join " "
                Write-Step "Ports to expose: $exposePorts"
            }
        }
    } else {
        Write-Warning "No .env file found, using default ports: 8000 8080 9000 9001"
        $exposePorts = "8000 8080 9000 9001"
    }

    # Build Docker image
    $ImageName = "langchain-mcp"
    $Tag = "latest"
    $FullImageName = "${ImageName}:${Tag}"

    Write-Step "Building Docker image: $FullImageName"
    Write-Step "This may take several minutes..."

    # Build arguments (convert ports array to space-separated string)
    $buildArgs = @()
    if ($exposePorts) {
        $portsString = $exposePorts -join " "
        $buildArgs += "--build-arg", "EXPOSE_PORTS=$portsString"
    }

    # Build with build context in parent directory to access both mcp_server and install.sh
    $dockerCommand = "docker build -t `"$FullImageName`" -f Dockerfile"
    if ($buildArgs.Count -gt 0) {
        $dockerCommand += " " + ($buildArgs -join " ")
    }
    $dockerCommand += " ../.."
    
    Write-Step "Running: $dockerCommand"
    
    # Execute Docker build (simple approach - build succeeded manually)
    Write-Step "Executing Docker build..."
    
    try {
        # Build docker command parts with clean output flags
        $dockerArgs = @(
            "build", 
            "--progress=plain",     # Plain text output instead of interactive
            "--no-cache",           # Force fresh build to see all output
            "-t", $FullImageName, 
            "-f", "Dockerfile"
        )
        if ($buildArgs.Count -gt 0) {
            $dockerArgs += $buildArgs
        }
        $dockerArgs += "../.."
        
        Write-Step "Using --progress=plain for clean output (no progress bars)"
        
        # Simple direct execution with visible output
        Write-Host "Executing Docker build..." -ForegroundColor Yellow
        & docker @dockerArgs
        
        if ($LASTEXITCODE -ne 0) {
            throw "Docker build failed with exit code: $LASTEXITCODE"
        }
    } catch {
        Write-Error-Custom "Docker build failed: $($_.Exception.Message)"
        exit 1
    }

    Write-Success "Docker image built successfully: $FullImageName"

    # Display image information
    Write-Step "Image information:"
    & docker images $ImageName --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

    Write-Success "Build completed!"
    
    Write-Step "Next steps:"
    Write-Host "  1. Copy .env.template to your project root as .env and configure it"
    Write-Host "  2. Update your .vscode/mcp.json to use Docker configuration"
    Write-Host "  3. Test the container with: .\run.ps1 C:\path\to\your\.env"

    Write-Step "To rebuild the image later, run this script again"

} catch {
    Write-Error-Custom "Build failed with error: $($_.Exception.Message)"
    exit 1
}
