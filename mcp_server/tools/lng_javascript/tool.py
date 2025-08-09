import mcp.types as types
import json
import os
from py_mini_racer import py_mini_racer
from mcp_server.file_state_manager import FileStateManager

# Create file state manager for JavaScript functions
javascript_manager = FileStateManager("mcp_server/javascript")

async def tool_info() -> dict:
    """Returns information about the lng_javascript tool."""
    return {
        "description": """JavaScript function management and execution tool.

**Commands:**

**1. add - Save JavaScript Function**
Save JavaScript functions to filesystem for later execution.

**Parameters:**
- `command` (string, required): Must be "add"
- `function_name` (string, required): Name of the function (must match function declaration)
- `function_code` (string, required): JavaScript function code (must be declared function, not arrow function)

**Example:**
```json
{
    "command": "add",
    "function_name": "calculateSum", 
    "function_code": "function calculateSum(params) { return params.a + params.b; }"
}
```

**2. execute - Run JavaScript Function**
Execute previously saved JavaScript functions with parameters.

**Parameters:**
- `command` (string, required): Must be "execute"
- `function_name` (string, required): Name of the saved function to execute
- `parameters` (string, required): Parameters to pass (JSON string or plain string)

**Parameter Handling:**
- If parameters is valid JSON string → parsed and passed as object
- If parameters is plain string → passed as string directly

**Examples:**
```json
{
    "command": "execute",
    "function_name": "calculateSum",
    "parameters": "{\\"a\\": 5, \\"b\\": 3}"
}
```

```json
{
    "command": "execute", 
    "function_name": "greet",
    "parameters": "World"
}
```

**3. list - List Saved Functions**
Show all saved JavaScript functions.

**Parameters:**
- `command` (string, required): Must be "list"

**Example:**
```json
{
    "command": "list"
}
```

**Function Requirements:**
- Must be declared functions (not arrow functions)
- Function name must match the function_name parameter
- Functions can contain any JavaScript code including async/await
- Functions are stored in mcp_server/javascript/ directory with .js extension

**Output:**
- Success: Returns actual function result (JSON or text)
- Error: JSON object with error message: {"error": "error_description"}

This tool provides JavaScript execution via PyMiniRacer engine with full support for modern JavaScript features.""",
        "schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command to execute: 'add', 'execute', or 'list'",
                    "enum": ["add", "execute", "list"]
                },
                "function_name": {
                    "type": "string", 
                    "description": "Name of the JavaScript function (required for add and execute commands)"
                },
                "function_code": {
                    "type": "string",
                    "description": "JavaScript function code (required for add command)"
                },
                "parameters": {
                    "type": "string",
                    "description": "Parameters to pass to function - JSON string or plain string (required for execute command)"
                }
            },
            "required": ["command"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Executes JavaScript functions based on command."""
    try:
        command = parameters.get("command", "")
        
        if not command:
            return [types.TextContent(type="text", text='{"error": "No command specified. Use add, execute, or list."}')]
        
        if command == "add":
            return await handle_add_command(parameters)
        elif command == "execute":
            return await handle_execute_command(parameters)
        elif command == "list":
            return await handle_list_command(parameters)
        else:
            return [types.TextContent(type="text", text=f'{{"error": "Unknown command: {command}. Use add, execute, or list."}}')]
            
    except Exception as e:
        error_result = {"error": f"Error in lng_javascript tool: {str(e)}"}
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]

async def handle_add_command(parameters: dict) -> list[types.Content]:
    """Handle the add command to save JavaScript functions."""
    try:
        function_name = parameters.get("function_name", "")
        function_code = parameters.get("function_code", "")
        
        if not function_name:
            return [types.TextContent(type="text", text='{"error": "function_name is required for add command."}')]
        
        if not function_code:
            return [types.TextContent(type="text", text='{"error": "function_code is required for add command."}')]
        
        # Validate that function_code contains a function declaration with the correct name
        if f"function {function_name}" not in function_code:
            return [types.TextContent(type="text", text=f'{{"error": "Function code must contain a declared function named {function_name}. Arrow functions are not allowed."}}')]
        
        # Save the function to the filesystem
        javascript_manager.set(function_name, function_code, extension=".js")
        
        result = {
            "message": f"Function '{function_name}' saved successfully",
            "function_name": function_name,
            "storage_path": f"mcp_server/javascript/{function_name}.js"
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        error_result = {"error": f"Error saving function: {str(e)}"}
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]

async def handle_execute_command(parameters: dict) -> list[types.Content]:
    """Handle the execute command to run JavaScript functions."""
    try:
        function_name = parameters.get("function_name", "")
        function_parameters = parameters.get("parameters", "")
        
        if not function_name:
            return [types.TextContent(type="text", text='{"error": "function_name is required for execute command."}')]
        
        # Load the function from the filesystem
        function_code = javascript_manager.get(function_name, extension=".js")
        
        if function_code is None:
            return [types.TextContent(type="text", text=f'{{"error": "Function {function_name} not found. Use add command to save it first."}}')]
        
        # Parse parameters
        parsed_params = parse_parameters(function_parameters)
        
        # Execute the JavaScript function
        result = execute_javascript_function(function_code, function_name, parsed_params)
        
        # Return the result - if it's already a string (JSON or plain text), return as-is
        if isinstance(result, str):
            return [types.TextContent(type="text", text=result)]
        else:
            # Convert to JSON if it's not a string
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
        
    except Exception as e:
        error_result = {"error": f"Error executing function: {str(e)}"}
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]

async def handle_list_command(parameters: dict) -> list[types.Content]:
    """Handle the list command to show all saved functions."""
    try:
        # Get all JavaScript functions
        function_names = javascript_manager.list_files(extension=".js")
        
        if not function_names:
            result = {
                "message": "No JavaScript functions saved",
                "functions": []
            }
        else:
            result = {
                "message": f"Found {len(function_names)} saved JavaScript function(s)",
                "functions": function_names,
                "storage_directory": "mcp_server/javascript/"
            }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        error_result = {"error": f"Error listing functions: {str(e)}"}
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]

def parse_parameters(param_string: str):
    """Parse parameters - try JSON first, fallback to string."""
    if not param_string:
        return None
    
    # Try to parse as JSON
    try:
        return json.loads(param_string)
    except json.JSONDecodeError:
        # If JSON parsing fails, return as string
        return param_string

def execute_javascript_function(function_code: str, function_name: str, parameters):
    """Execute JavaScript function using PyMiniRacer."""
    try:
        # Create PyMiniRacer context
        ctx = py_mini_racer.MiniRacer()
        
        # Evaluate the function code to define the function
        ctx.eval(function_code)
        
        # Call the function with parameters
        if parameters is not None:
            result = ctx.call(function_name, parameters)
        else:
            result = ctx.call(function_name)
        
        return result
        
    except Exception as e:
        raise Exception(f"JavaScript execution error: {str(e)}")