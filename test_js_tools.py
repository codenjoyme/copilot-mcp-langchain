#!/usr/bin/env python3

import json
import pathlib
import sys

# Simple test of the JavaScript functionality without MCP dependencies

def test_add_function():
    """Test storing a JavaScript function"""
    function_name = "add_numbers"
    function_code = "function add_numbers(a, b) { console.log('Adding:', a, b); return a + b; }"
    
    # Get the project root directory and create the javascript directory path
    current_dir = pathlib.Path(__file__).parent
    javascript_dir = current_dir / "javascript"
    
    # Create directory if it doesn't exist
    javascript_dir.mkdir(exist_ok=True)
    
    # Create the file path
    file_path = javascript_dir / f"{function_name}.js"
    
    # Write the function code to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(function_code)
    
    print(f"✅ Function '{function_name}' stored successfully at {file_path}")
    return file_path

def test_exec_function():
    """Test executing a JavaScript function"""
    try:
        from py_mini_racer import py_mini_racer
    except ImportError:
        print("❌ py-mini-racer not available")
        return
    
    function_name = "add_numbers"
    params_json = '{"a": 5, "b": 3}'
    
    # Parse parameters
    params_dict = json.loads(params_json)
    sorted_keys = sorted(params_dict.keys())
    param_values = [params_dict[key] for key in sorted_keys]
    
    print(f"📝 Parameters: {params_dict}")
    print(f"📝 Sorted keys: {sorted_keys}")
    print(f"📝 Parameter values: {param_values}")
    
    # Get the JavaScript file
    current_dir = pathlib.Path(__file__).parent
    javascript_dir = current_dir / "javascript"
    file_path = javascript_dir / f"{function_name}.js"
    
    if not file_path.exists():
        print(f"❌ JavaScript function file not found: {function_name}.js")
        return
    
    # Read the function code
    with open(file_path, 'r', encoding='utf-8') as f:
        function_code = f.read()
    
    print(f"📝 Function code: {function_code}")
    
    # Execute JavaScript
    try:
        print("📝 Creating MiniRacer context...")
        # Create a context
        ctx = py_mini_racer.MiniRacer()
        
        print("📝 Adding console implementation...")
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
        
        print("📝 Executing function code...")
        # Execute the function code
        ctx.eval(function_code)
        
        print("📝 Preparing function call...")
        # Prepare function call - for simple values, pass directly
        param_args = []
        for value in param_values:
            if isinstance(value, (dict, list)):
                param_args.append(json.dumps(value))
            else:
                param_args.append(str(value))
        
        print(f"📝 param_args: {param_args}")
        print(f"📝 param_args types: {[type(x) for x in param_args]}")
        
        # Create the function call string
        call_string = f"{function_name}({', '.join(param_args)})"
        
        print(f"📝 Call string: {call_string}")
        
        print("📝 Executing function call...")
        # Execute the function call
        result = ctx.eval(call_string)
        
        print("📝 Getting console output...")
        # Get console output - convert JSObject to list
        console_output = ctx.eval("JSON.stringify(consoleCapture)")
        print(f"📝 Console output (JSON): {console_output}")
        if console_output:
            console_list = json.loads(console_output)
            console_text = '\n'.join(console_list)
        else:
            console_text = ""
        
        print(f"✅ Result: {result}")
        print(f"✅ Console: {console_text}")
        
        return {
            "result": result,
            "console": console_text,
            "error": ""
        }
        
    except Exception as e:
        print(f"❌ JavaScript execution error: {str(e)}")
        return {
            "result": None,
            "console": "",
            "error": f"JavaScript execution error: {str(e)}"
        }

def test_complex_parameters():
    """Test with complex JSON objects"""
    try:
        from py_mini_racer import py_mini_racer
    except ImportError:
        print("❌ py-mini-racer not available")
        return
    
    # Store a complex function first
    function_name = "process_objects"
    function_code = """
    function process_objects(config, data) {
        console.log('Processing data:', JSON.stringify(data));
        console.log('Config:', JSON.stringify(config));
        return {
            items: data.items,
            sorted: config.sort,
            count: data.items.length
        };
    }
    """
    
    # Save the function
    current_dir = pathlib.Path(__file__).parent
    javascript_dir = current_dir / "javascript"
    javascript_dir.mkdir(exist_ok=True)
    file_path = javascript_dir / f"{function_name}.js"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(function_code)
    
    print(f"✅ Complex function '{function_name}' stored successfully")
    
    # Test with complex parameters
    params_json = '{"data":{"items":[1,2,3]}, "config":{"sort":true}}'
    
    # Parse parameters
    params_dict = json.loads(params_json)
    sorted_keys = sorted(params_dict.keys())
    param_values = [params_dict[key] for key in sorted_keys]
    
    print(f"📝 Parameters: {params_dict}")
    print(f"📝 Sorted keys: {sorted_keys}")
    print(f"📝 Parameter values: {param_values}")
    
    # Read the function code
    with open(file_path, 'r', encoding='utf-8') as f:
        function_code = f.read()
    
    # Execute JavaScript
    try:
        ctx = py_mini_racer.MiniRacer()
        
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
        ctx.eval(function_code)
        
        # For complex parameters, pass as JSON objects
        param_args = []
        for value in param_values:
            if isinstance(value, (dict, list)):
                # Pass the JSON object directly
                param_args.append(json.dumps(value))
            else:
                param_args.append(str(value))
        
        call_string = f"{function_name}({', '.join(param_args)})"
        print(f"📝 Call string: {call_string}")
        
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
        
        print(f"✅ Result: {result}")
        print(f"✅ Console: {console_text}")
        
    except Exception as e:
        print(f"❌ JavaScript execution error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing JavaScript tools...")
    print("\n--- Testing add function ---")
    test_add_function()
    
    print("\n--- Testing exec function ---")
    test_exec_function()
    
    print("\n--- Testing complex parameters ---")
    test_complex_parameters()