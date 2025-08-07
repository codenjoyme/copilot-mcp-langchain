import mcp.types as types
import json
import os
import pathlib

async def tool_info() -> dict:
    """Returns information about the lng_javascript_add tool."""
    return {
        "description": """Store JavaScript functions for later execution.

**Parameters:**
- `function_name` (string, required): Name of the function (will be used as filename)
- `function_code` (string, required): Complete JavaScript function definition

**Functionality:**
- Store functions as .js files in mcp_server/javascript/ directory
- File naming convention: {function_name}.js
- Store complete function definition as provided by user
- Create directory if it doesn't exist

**Usage examples:**
- function_name: "add_numbers"
- function_code: "function add_numbers(a, b) { console.log('Adding:', a, b); return a + b; }"

This tool is useful for storing JavaScript functions that can later be executed with lng_javascript_exec.""",
        "schema": {
            "type": "object",
            "properties": {
                "function_name": {
                    "type": "string",
                    "description": "Name of the function (will be used as filename)"
                },
                "function_code": {
                    "type": "string", 
                    "description": "Complete JavaScript function definition"
                }
            },
            "required": ["function_name", "function_code"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Store JavaScript functions for later execution."""
    try:
        # Get parameters
        function_name = parameters.get("function_name", "").strip()
        function_code = parameters.get("function_code", "").strip()
        
        if not function_name:
            return [types.TextContent(type="text", text='{"error": "No function name provided."}')]
            
        if not function_code:
            return [types.TextContent(type="text", text='{"error": "No function code provided."}')]
        
        # Validate function name (basic sanitization)
        if not function_name.replace('_', '').replace('-', '').isalnum():
            return [types.TextContent(type="text", text='{"error": "Function name can only contain letters, numbers, underscores and hyphens."}')]
        
        # Get the project root directory and create the javascript directory path
        current_dir = pathlib.Path(__file__).parent.parent.parent.parent
        javascript_dir = current_dir / "javascript"
        
        # Create directory if it doesn't exist
        javascript_dir.mkdir(exist_ok=True)
        
        # Create the file path
        file_path = javascript_dir / f"{function_name}.js"
        
        # Write the function code to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(function_code)
        
        # Create result
        result_dict = {
            "success": True,
            "function_name": function_name,
            "file_path": str(file_path),
            "message": f"JavaScript function '{function_name}' stored successfully"
        }
        
        # Convert to JSON string
        json_result = json.dumps(result_dict, indent=2, ensure_ascii=False)
        
        return [types.TextContent(type="text", text=json_result)]
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Error storing JavaScript function: {str(e)}",
            "function_name": parameters.get("function_name", ""),
            "function_code": parameters.get("function_code", "")[:100] + "..." if len(parameters.get("function_code", "")) > 100 else parameters.get("function_code", "")
        }
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]