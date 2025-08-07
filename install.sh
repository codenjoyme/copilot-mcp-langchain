green=92  # stages info
blue=94   # commands in eval_echo
yellow=93 # useful info
red=91    # errors

color() {
    message=$1
    color=$2

    echo "[${color}m"
    echo $message
    echo "[0m"
}

eval_echo() {
    to_run=$1
    echo "[${blue}m"
    echo $to_run
    echo "[0m"

    eval $to_run
}

eval_echo "python --version"

# create virtual environment
eval_echo "pip install virtualenv"
eval_echo "python -m virtualenv .virtualenv"
eval_echo ". ./.virtualenv/Scripts/activate"
if [ -n "$VIRTUAL_ENV" ]; then
    color "Virtual environment activated: $VIRTUAL_ENV" $green
else
    color "Virtual environment not activated!" $red
fi
eval_echo "python -c \"import sys; print('Python executable:', sys.executable)\""

# install core MCP dependencies
eval_echo "pip install 'mcp[cli]'"
eval_echo "pip show mcp"

# install oter stuff
eval_echo "pip install python-dotenv PyYAML"

# install FastAPI and Uvicorn for HTTP server
eval_echo "pip install fastapi uvicorn requests"

# install py-mini-racer for JavaScript execution tools (lng_javascript_add, lng_javascript_exec)
eval_echo "pip install py-mini-racer"

# Tool-specific dependencies are now managed via `settings.yaml` files.
# Run this to install dependencies for enabled tools:
eval_echo "python -m mcp_server.run install_dependencies"