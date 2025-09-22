# MCP Server Docker Run Script (PowerShell)
# Launches the langchain-mcp container with proper configuration

param(
    [Parameter(Mandatory=$true)]
    [string]$EnvFile
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to detect if running in MCP mode (no terminal attached)
function Test-McpMode {
    # In PowerShell, check if we're running non-interactively
    return (-not [Console]::IsInputRedirected -eq $false -or -not [Console]::IsOutputRedirected -eq $false)
}

# Colors for output (PowerShell equivalents)
function Write-Step {
    param([string]$Message)
    # В MCP режиме выводим через stderr, в интерактивном - как обычно
    [Console]::Error.WriteLine("[RUN] $Message")
}

function Write-Success {
    param([string]$Message)
    [Console]::Error.WriteLine("[SUCCESS] $Message")
}

function Write-Warning {
    param([string]$Message)
    [Console]::Error.WriteLine("[WARNING] $Message")
}

function Write-Error-Custom {
    param([string]$Message)
    [Console]::Error.WriteLine("[ERROR] $Message")
}

# Function to read .env file
function Read-EnvFile {
    param([string]$FilePath)
    
    $envVars = @{}
    
    if (Test-Path $FilePath) {
        Get-Content $FilePath | ForEach-Object {
            if ($_ -match '^([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                # Remove quotes if present
                $value = $value -replace '^["''](.*)["'']$', '$1'
                $envVars[$key] = $value
            }
        }
    }
    
    return $envVars
}

# Function to convert Windows paths to Docker format
function Convert-PathForDocker {
    param([string]$Path)
    
    # Convert Windows path to Docker format
    if ($Path -match '^[A-Za-z]:') {
        # Convert C:\path to /c/path for Docker Desktop on Windows
        $driveLetter = $Path.Substring(0,1).ToLower()
        $restOfPath = $Path.Substring(2) -replace '\\', '/'
        return "/$driveLetter$restOfPath"
    } else {
        return $Path -replace '\\', '/'
    }
}

try {
Write-Step "Starting MCP Server Docker container..."
Write-Step "Using .env file: $EnvFile"

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Error "Docker is not running or not accessible"
    Write-Error "Please start Docker Desktop and try again"
    exit 1
}

# Check if Docker image exists
try {
    docker image inspect langchain-mcp:latest | Out-Null
} catch {
    Write-Error "Docker image 'langchain-mcp:latest' not found"
    Write-Error "Please build the image first using: build.ps1"
    exit 1
}    # Validate .env file exists
    if (!(Test-Path $EnvFile)) {
        Write-Error-Custom ".env file not found: $EnvFile"
        exit 1
    }

    # Read .env file
    $envVars = Read-EnvFile -FilePath $EnvFile

    # Validate required variables
    $requiredVars = @('MCP_CONFIG_PATH', 'MCP_LOGS_PATH', 'MCP_PROJECTS_PATH')
    $missingVars = @()
    
    foreach ($var in $requiredVars) {
        if (!$envVars.ContainsKey($var) -or [string]::IsNullOrWhiteSpace($envVars[$var])) {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -gt 0) {
        Write-Error-Custom "Missing required variables in .env file:"
        foreach ($var in $missingVars) {
            Write-Error-Custom "  $var"
        }
        exit 1
    }

    # Convert paths for Docker compatibility
    $dockerConfigPath = Convert-PathForDocker -Path $envVars['MCP_CONFIG_PATH']
    $dockerLogsPath = Convert-PathForDocker -Path $envVars['MCP_LOGS_PATH']
    $dockerProjectsPath = Convert-PathForDocker -Path $envVars['MCP_PROJECTS_PATH']

    Write-Step "Volume mappings:"
    Write-Step "  Config: $dockerConfigPath -> /app/mcp_server/config"
    Write-Step "  Logs: $dockerLogsPath -> /app/mcp_server/logs"
    Write-Step "  Projects: $dockerProjectsPath -> /app/mcp_server/projects"

    # Initialize host directories with content from container if they're empty
    Write-Step "Initializing host directories..."
    
    # Create host directories if they don't exist
    @($envVars['MCP_CONFIG_PATH'], $envVars['MCP_LOGS_PATH'], $envVars['MCP_PROJECTS_PATH']) | ForEach-Object {
        if (!(Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force | Out-Null
        }
    }
    
    # Check if config directory is empty and copy defaults from container
    $configFiles = @(Get-ChildItem -Path $envVars['MCP_CONFIG_PATH'] -Recurse -Force 2>$null)
    if ($configFiles.Count -eq 0) {
        Write-Step "Config directory is empty, copying defaults from container..."
        $tempArgs = @(
            'run', '--rm'
            '-v', "${dockerConfigPath}:/host/config"
            'langchain-mcp:latest'
            'sh', '-c', 'cp -r /app/mcp_server/config/* /host/config/ 2>/dev/null || cp -r /app/templates/config/* /host/config/ 2>/dev/null || echo "No default config found"'
        )
        & docker @tempArgs | Out-Null
        Write-Success "Config directory initialized"
    }
    
    # Check if projects directory is empty and copy defaults from container  
    $projectFiles = @(Get-ChildItem -Path $envVars['MCP_PROJECTS_PATH'] -Recurse -Force 2>$null)
    if ($projectFiles.Count -eq 0) {
        Write-Step "Projects directory is empty, copying defaults from container..."
        $tempArgs = @(
            'run', '--rm'
            '-v', "${dockerProjectsPath}:/host/projects"
            'langchain-mcp:latest'
            'sh', '-c', 'cp -r /app/mcp_server/projects/* /host/projects/ 2>/dev/null || cp -r /app/templates/projects/* /host/projects/ 2>/dev/null || echo "No default projects found"'
        )
        & docker @tempArgs | Out-Null
        Write-Success "Projects directory initialized"
    }

    # Build Docker run command arguments
    $dockerArgs = @(
        'run', '--rm', '-i'
        '--env-file', $EnvFile
        '-v', "${dockerConfigPath}:/app/mcp_server/config"
        '-v', "${dockerLogsPath}:/app/mcp_server/logs"
        '-v', "${dockerProjectsPath}:/app/mcp_server/projects"
    )

    # Handle port mappings from MCP_PORTS
    if ($envVars.ContainsKey('MCP_PORTS') -and ![string]::IsNullOrWhiteSpace($envVars['MCP_PORTS'])) {
        Write-Step "Port mappings: $($envVars['MCP_PORTS'])"
        $ports = $envVars['MCP_PORTS'] -split ',' | ForEach-Object { $_.Trim() }
        foreach ($port in $ports) {
            if (![string]::IsNullOrWhiteSpace($port)) {
                $dockerArgs += @('-p', $port)
            }
        }
    } else {
        Write-Warning "No MCP_PORTS specified, no ports will be forwarded"
    }

    # Add image name
    $dockerArgs += 'langchain-mcp:latest'

    Write-Step "Executing Docker command..."
    Write-Step "Container ready for MCP communication via stdio"
    Write-Step "Docker args: $($dockerArgs -join ' ')"

    # Execute the Docker command
    & docker @dockerArgs

} catch {
    Write-Error-Custom "Run failed with error: $($_.Exception.Message)"
    exit 1
}
