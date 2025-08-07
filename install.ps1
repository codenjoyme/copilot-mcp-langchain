# PowerShell colors
$green = "Green"     # stages info
$blue = "Blue"       # commands in eval_echo
$yellow = "Yellow"   # useful info
$red = "Red"         # errors

function Color {
    param(
        [string]$message,
        [string]$color = "White"
    )
    
    Write-Host $message -ForegroundColor $color
}

function Eval-Echo {
    param(
        [string]$toRun
    )
    
    Write-Host ""
    Write-Host $toRun -ForegroundColor $blue
    Write-Host ""
    
    Invoke-Expression $toRun
}

Eval-Echo "python --version"

# create virtual environment
Eval-Echo "pip install virtualenv"
Eval-Echo "python -m virtualenv .virtualenv"
Eval-Echo "& .\.virtualenv\Scripts\Activate.ps1"
if ($env:VIRTUAL_ENV) {
    Color "Virtual environment activated: $env:VIRTUAL_ENV" $green
} else {
    Color "Virtual environment not activated!" $red
}
Eval-Echo "python -c `"import sys; print('Python executable:', sys.executable)`""

# install core MCP dependencies
Eval-Echo "pip install 'mcp[cli]'"
Eval-Echo "pip show mcp"

# install other stuff
Eval-Echo "pip install python-dotenv PyYAML"

# install FastAPI and Uvicorn for HTTP server
Eval-Echo "pip install fastapi uvicorn requests"

# install py-mini-racer for JavaScript execution tools (lng_javascript_add, lng_javascript_exec)
Eval-Echo "pip install py-mini-racer"

# Tool-specific dependencies are now managed via `settings.yaml` files.
# Run this to install dependencies for enabled tools:
Eval-Echo "python -m mcp_server.run install_dependencies"
