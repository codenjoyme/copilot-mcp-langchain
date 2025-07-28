#!/bin/bash

# macOS-specific installation script for copilot-mcp-langchain
# This script ensures proper setup on macOS systems

green=92  # stages info
blue=94   # commands in eval_echo
yellow=93 # useful info
red=91    # errors

color() {
    message=$1
    color=$2

    echo -e "\033[${color}m"
    echo "$message"
    echo -e "\033[0m"
}

eval_echo() {
    to_run=$1
    echo -e "\033[${blue}m"
    echo "$to_run"
    echo -e "\033[0m"

    eval "$to_run"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    color "Warning: This script is designed for macOS. Use install.sh for other Unix systems." $yellow
fi

color "🍎 macOS Setup for copilot-mcp-langchain" $green

# Check Python version
eval_echo "python3 --version"

# Ensure we have python3 and pip3
if ! command -v python3 &> /dev/null; then
    color "❌ Python 3 is required. Please install Python 3 first." $red
    color "💡 Try: brew install python3" $yellow
    exit 1
fi

# Use python3 explicitly on macOS with built-in venv (modern approach)
color "📦 Creating virtual environment..." $green
eval_echo "python3 -m venv .virtualenv"
eval_echo "source ./.virtualenv/bin/activate"

if [ -n "$VIRTUAL_ENV" ]; then
    color "✅ Virtual environment activated: $VIRTUAL_ENV" $green
else
    color "❌ Virtual environment not activated!" $red
    exit 1
fi

eval_echo "python -c \"import sys; print('Python executable:', sys.executable)\""

# Install core MCP dependencies
color "📦 Installing MCP dependencies..." $green
eval_echo "pip install 'mcp[cli]'"
eval_echo "pip show mcp"

# Install other dependencies
color "📦 Installing additional dependencies..." $green
eval_echo "pip install python-dotenv PyYAML"

# Install FastAPI and Uvicorn for HTTP server
eval_echo "pip install fastapi uvicorn requests"

# Tool-specific dependencies are now managed via `settings.yaml` files.
color "📦 Installing tool-specific dependencies..." $green
eval_echo "python -m mcp_server.run install_dependencies"

color "🎉 Installation complete!" $green
color "📝 Next steps:" $yellow
echo "1. Copy .env.template to .env and configure your API keys"
echo "2. Use .vscode/mcp-macos.json or .cursor/mcp-macos.json for VS Code/Cursor"
echo "3. Run 'source ./.virtualenv/bin/activate' to activate the environment"
echo "4. Test with: python -m mcp_server.run list" 