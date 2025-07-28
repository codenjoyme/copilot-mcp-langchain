# macOS Setup Guide for copilot-mcp-langchain

This guide provides macOS-specific setup instructions for the copilot-mcp-langchain project.

## 🍎 Prerequisites

### 1. Install Python 3
```bash
# Using Homebrew (recommended)
brew install python3

# Verify installation
python3 --version
```

### 2. Install PowerShell (Optional but Recommended)
```bash
brew install --cask powershell
```

## 🚀 Quick Setup

### Option 1: macOS-Specific Script (Recommended)
```bash
./install-macos.sh
```

### Option 2: PowerShell Script (Cross-Platform)
```bash
pwsh ./install.ps1
```

### Option 3: Fixed Unix Script
```bash
./install.sh
```

## ⚙️ Configuration

### 1. Environment Variables
```bash
# Copy the template and edit
cp env.template .env
nano .env  # or vim/code .env
```

Required variables:
- For OpenAI: Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY`
- For Azure: Set `LLM_PROVIDER=azure` and Azure-specific variables

### 2. VS Code Configuration
Copy the macOS-specific MCP configuration:
```bash
cp .vscode/mcp-macos.json .vscode/mcp.json
```

### 3. Cursor Configuration  
Copy the macOS-specific configuration:
```bash
cp .cursor/mcp-macos.json .cursor/mcp.json
```

**Important:** Update the `{workspaceFolder}` placeholder with your actual absolute path:
```json
{
  "mcpServers": {
    "langchain-mcp":{
        "command": "/Users/yourusername/path/to/copilot-mcp-langchain/.virtualenv/bin/python",
        "args": ["/Users/yourusername/path/to/copilot-mcp-langchain/mcp_server/server.py"]
    }
  }
}
```

## 🧪 Testing

### 1. Activate Virtual Environment
```bash
source ./.virtualenv/bin/activate
```

### 2. Test Tools
```bash
# List available tools
python -m mcp_server.run list

# Test a simple tool
python -m mcp_server.run run lng_count_words '{"input_text":"Hello macOS!"}'

# Test the math calculator
python -m mcp_server.run run lng_math_calculator '{"expression":"2+3*4"}'
```

### 3. Test MCP Server
```bash
python mcp_server/test/server.py
```

### 4. Test LLM Connection
```bash
python simple_openai.py    # or simple_azure.py or simple_both.py
```

## 🔧 VS Code/Cursor Setup

### 1. Enable MCP in VS Code
Add to `.vscode/settings.json`:
```json
{
    "chat.mcp.enabled": true,
    "github.copilot.chat.codeGeneration.useInstructionFiles": false
}
```

### 2. Restart VS Code/Cursor
After configuration, restart your editor to load the MCP server.

## 📁 macOS-Specific Files

The following files have been created for macOS compatibility:
- `.vscode/mcp-macos.json` - VS Code MCP configuration with Unix paths
- `.cursor/mcp-macos.json` - Cursor MCP configuration with Unix paths  
- `install-macos.sh` - macOS-optimized installation script
- `env.template` - Environment variables template
- `SETUP-MACOS.md` - This setup guide

## ❗ Troubleshooting

### Virtual Environment Issues
```bash
# If activation fails, try recreating
rm -rf .virtualenv
python3 -m virtualenv .virtualenv
source ./.virtualenv/bin/activate
```

### Path Issues in MCP Config
- Ensure absolute paths (no `~` or relative paths)
- Use forward slashes `/` not backslashes `\`
- Verify the Python executable exists: `ls -la .virtualenv/bin/python`

### Permission Issues
```bash
# Make scripts executable
chmod +x install-macos.sh
chmod +x test.sh
```

### API Key Issues
- Verify `.env` file exists and has correct format
- Check API key validity with simple test scripts
- Ensure no extra spaces around `=` in `.env` file

## 🆚 Differences from Windows

| Component | Windows | macOS |
|-----------|---------|-------|
| Virtual env path | `.virtualenv/Scripts/` | `.virtualenv/bin/` |
| Python executable | `python.exe` | `python` |
| Path separators | `\` (backslash) | `/` (forward slash) |
| Script activation | `Scripts\Activate.ps1` | `bin/activate` |

## 🎯 Next Steps

1. Set up your API keys in `.env`
2. Test the basic functionality
3. Configure your editor (VS Code/Cursor)
4. Start using the enhanced GitHub Copilot capabilities!

For more details, see the main [README.md](README.md) file. 