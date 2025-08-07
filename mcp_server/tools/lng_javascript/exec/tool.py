import mcp.types as types
import json
import os
import pathlib
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# Try to import py_mini_racer, handle ImportError gracefully
try:
    from py_mini_racer import py_mini_racer
    MINI_RACER_AVAILABLE = True
except ImportError:
    MINI_RACER_AVAILABLE = False

async def tool_info() -> dict:
    """Returns information about the lng_javascript_exec tool."""
    return {
        "description": """Load and execute stored JavaScript functions.

**Parameters:**
- `function_name` (string, required): Name of the function to execute
- `parameters` (string, required): JSON string containing function parameters

**Functionality:**
- Load function from mcp_server/javascript/{function_name}.js
- Parse parameters JSON and extract values in alphabetical key order for function arguments
- Simple JSON {"a":1, "b":2} → call fun(1, 2) (a=1, b=2 in alphabetical order)
- Complex JSON {"a":{"c":1}, "b":{"d":2}} → call fun({"c":1}, {"d":2}) (pass actual JSON objects)
- Return structured result object

**Parameter Handling:**
- Input: JSON string in parameters field
- Parse JSON and extract values in alphabetical key order for function arguments
- Pass actual JSON objects (not strings) for complex parameters
- Example: {"b":2, "a":1} → extract as [1, 2] → call fun(1, 2)

**Return Object Structure:**
{
  "result": "JSON representation of function return value, or string representation if not JSON-serializable",
  "console": "captured console.log outputs",
  "error": "detailed error information if any"
}

**Usage examples:**
- function_name: "add_numbers"
- parameters: '{"a":5,"b":3}'

This tool is useful for executing stored JavaScript functions with parameter parsing.""",
        "schema": {
            "type": "object",
            "properties": {
                "function_name": {
                    "type": "string",
                    "description": "Name of the function to execute"
                },
                "parameters": {
                    "type": "string", 
                    "description": "JSON string containing function parameters"
                }
            },
            "required": ["function_name", "parameters"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Load and execute stored JavaScript functions."""
    try:
        # Check if py_mini_racer is available
        if not MINI_RACER_AVAILABLE:
            return [types.TextContent(type="text", text='{"error": "py-mini-racer is not installed. Please install it with: pip install py-mini-racer"}')]
        
        # Get parameters
        function_name = parameters.get("function_name", "").strip()
        params_json = parameters.get("parameters", "").strip()
        
        if not function_name:
            return [types.TextContent(type="text", text='{"error": "No function name provided."}')]
            
        if not params_json:
            return [types.TextContent(type="text", text='{"error": "No parameters provided."}')]
        
        # Parse the parameters JSON
        try:
            params_dict = json.loads(params_json)
        except json.JSONDecodeError as e:
            return [types.TextContent(type="text", text=f'{{"error": "Invalid JSON in parameters: {str(e)}"}}')]
        
        # Extract parameter values in alphabetical key order
        sorted_keys = sorted(params_dict.keys())
        param_values = [params_dict[key] for key in sorted_keys]
        
        # Get the project root directory and find the JavaScript file
        current_dir = pathlib.Path(__file__).parent.parent.parent.parent
        javascript_dir = current_dir / "javascript"
        file_path = javascript_dir / f"{function_name}.js"
        
        # Check if file exists
        if not file_path.exists():
            return [types.TextContent(type="text", text=f'{{"error": "JavaScript function file not found: {function_name}.js"}}')]
        
        # Read the function code
        with open(file_path, 'r', encoding='utf-8') as f:
            function_code = f.read()
        
        # Execute the JavaScript
        result = execute_javascript(function_code, function_name, param_values)
        
        # Convert to JSON string
        json_result = json.dumps(result, indent=2, ensure_ascii=False)
        
        return [types.TextContent(type="text", text=json_result)]
        
    except Exception as e:
        error_result = {
            "result": None,
            "console": "",
            "error": f"Error executing JavaScript function: {str(e)}",
            "function_name": parameters.get("function_name", ""),
            "parameters": parameters.get("parameters", "")
        }
        return [types.TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]

def execute_javascript(function_code: str, function_name: str, param_values: list) -> dict:
    """Execute JavaScript code using py_mini_racer."""
    try:
        # Create a context
        ctx = py_mini_racer.MiniRacer()
        
        # Capture console output
        console_output = []
        
        # Add console.log implementation
        console_js = """
        var console = {
            log: function(...args) {
                consoleCapture.push(args.map(arg => 
                    typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
                ).join(' '));
            }
        };
        var consoleCapture = [];
        """
        
        ctx.eval(console_js)
        
        # Execute the function code
        ctx.eval(function_code)
        
        # Prepare function call
        param_args = []
        for value in param_values:
            if isinstance(value, (dict, list)):
                # For complex objects, pass as JSON
                param_args.append(json.dumps(value))
            else:
                # For simple values, pass directly
                param_args.append(json.dumps(value))
        
        # Create the function call string
        call_string = f"{function_name}({', '.join(param_args)})"
        
        # Execute the function call
        result = ctx.eval(call_string)
        
        # Convert result to JSON if it's an object
        if hasattr(result, '__dict__') or str(type(result)).startswith("<class 'py_mini_racer"):
            try:
                result = ctx.eval(f"JSON.stringify({call_string})")
                result = json.loads(result)
            except:
                result = str(result)
        
        # Get console output
        console_output = ctx.eval("JSON.stringify(consoleCapture)")
        if console_output:
            console_list = json.loads(console_output)
            console_text = '\n'.join(console_list)
        else:
            console_text = ""
        
        # Prepare the result
        return {
            "result": result,
            "console": console_text,
            "error": ""
        }
        
    except Exception as e:
        return {
            "result": None,
            "console": "",
            "error": f"JavaScript execution error: {str(e)}"
        }