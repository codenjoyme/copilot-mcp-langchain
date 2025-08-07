#!/usr/bin/env python3

"""
Comprehensive test suite for JavaScript execution tools
Tests both lng_javascript_add and lng_javascript_exec functionality
"""

import json
import pathlib
import sys
import tempfile
import shutil

# Try to import py_mini_racer
try:
    from py_mini_racer import py_mini_racer
    MINI_RACER_AVAILABLE = True
except ImportError:
    MINI_RACER_AVAILABLE = False
    print("❌ py-mini-racer not available, some tests will be skipped")

def simulate_add_tool(function_name: str, function_code: str) -> dict:
    """Simulate the lng_javascript_add tool functionality"""
    try:
        if not function_name.strip():
            return {"error": "No function name provided."}
            
        if not function_code.strip():
            return {"error": "No function code provided."}
        
        # Validate function name (basic sanitization)
        if not function_name.replace('_', '').replace('-', '').isalnum():
            return {"error": "Function name can only contain letters, numbers, underscores and hyphens."}
        
        # Get the current directory and create the javascript directory path
        current_dir = pathlib.Path(__file__).parent
        javascript_dir = current_dir / "javascript"
        
        # Create directory if it doesn't exist
        javascript_dir.mkdir(exist_ok=True)
        
        # Create the file path
        file_path = javascript_dir / f"{function_name}.js"
        
        # Write the function code to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(function_code)
        
        return {
            "success": True,
            "function_name": function_name,
            "file_path": str(file_path),
            "message": f"JavaScript function '{function_name}' stored successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error storing JavaScript function: {str(e)}",
            "function_name": function_name,
            "function_code": function_code[:100] + "..." if len(function_code) > 100 else function_code
        }

def execute_javascript(function_code: str, function_name: str, param_values: list) -> dict:
    """Execute JavaScript code using py_mini_racer."""
    try:
        # Create a context
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
                param_args.append(str(value))
        
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

def simulate_exec_tool(function_name: str, parameters: str) -> dict:
    """Simulate the lng_javascript_exec tool functionality"""
    try:
        if not MINI_RACER_AVAILABLE:
            return {"error": "py-mini-racer is not installed. Please install it with: pip install py-mini-racer"}
        
        if not function_name.strip():
            return {"error": "No function name provided."}
            
        if not parameters.strip():
            return {"error": "No parameters provided."}
        
        # Parse the parameters JSON
        try:
            params_dict = json.loads(parameters)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in parameters: {str(e)}"}
        
        # Extract parameter values in alphabetical key order
        sorted_keys = sorted(params_dict.keys())
        param_values = [params_dict[key] for key in sorted_keys]
        
        # Get the current directory and find the JavaScript file
        current_dir = pathlib.Path(__file__).parent
        javascript_dir = current_dir / "javascript"
        file_path = javascript_dir / f"{function_name}.js"
        
        # Check if file exists
        if not file_path.exists():
            return {"error": f"JavaScript function file not found: {function_name}.js"}
        
        # Read the function code
        with open(file_path, 'r', encoding='utf-8') as f:
            function_code = f.read()
        
        # Execute the JavaScript
        result = execute_javascript(function_code, function_name, param_values)
        
        return result
        
    except Exception as e:
        return {
            "result": None,
            "console": "",
            "error": f"Error executing JavaScript function: {str(e)}",
            "function_name": function_name,
            "parameters": parameters
        }

def test_simple_function():
    """Test storing and executing a simple function"""
    print("=== Testing Simple Function ===")
    
    # Test lng_javascript_add
    result = simulate_add_tool("add_numbers", "function add_numbers(a, b) { console.log('Adding:', a, b); return a + b; }")
    print(f"Add result: {json.dumps(result, indent=2)}")
    
    if not result.get("success"):
        print("❌ Failed to add function")
        return False
    
    if not MINI_RACER_AVAILABLE:
        print("⚠️  Skipping execution test - py-mini-racer not available")
        return True
    
    # Test lng_javascript_exec
    result = simulate_exec_tool("add_numbers", '{"a":5,"b":3}')
    print(f"Exec result: {json.dumps(result, indent=2)}")
    
    if result.get("error"):
        print("❌ Failed to execute function")
        return False
        
    if result.get("result") != 8:
        print(f"❌ Expected result 8, got {result.get('result')}")
        return False
        
    if "Adding: 5 3" not in result.get("console", ""):
        print(f"❌ Expected console output, got: {result.get('console')}")
        return False
    
    print("✅ Simple function test passed")
    return True

def test_parameter_ordering():
    """Test parameter ordering (alphabetical key order)"""
    print("\n=== Testing Parameter Ordering ===")
    
    if not MINI_RACER_AVAILABLE:
        print("⚠️  Skipping parameter ordering test - py-mini-racer not available")
        return True
    
    # Test with reversed parameter order in JSON
    result = simulate_exec_tool("add_numbers", '{"b":10,"a":5}')
    print(f"Reversed order result: {json.dumps(result, indent=2)}")
    
    if result.get("error"):
        print("❌ Failed to execute function with reversed parameters")
        return False
        
    if result.get("result") != 15:
        print(f"❌ Expected result 15, got {result.get('result')}")
        return False
        
    # Check that parameters were passed in alphabetical order (a=5, b=10)
    if "Adding: 5 10" not in result.get("console", ""):
        print(f"❌ Expected 'Adding: 5 10' in console, got: {result.get('console')}")
        return False
    
    print("✅ Parameter ordering test passed")
    return True

def test_complex_parameters():
    """Test complex JSON object parameters"""
    print("\n=== Testing Complex Parameters ===")
    
    # Store complex function
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
    
    result = simulate_add_tool("process_objects", function_code)
    print(f"Add complex function result: {json.dumps(result, indent=2)}")
    
    if not result.get("success"):
        print("❌ Failed to add complex function")
        return False
    
    if not MINI_RACER_AVAILABLE:
        print("⚠️  Skipping execution test - py-mini-racer not available")
        return True
    
    # Test execution with complex parameters
    # Note: alphabetical order is config, data
    params = '{"data":{"items":[1,2,3]}, "config":{"sort":true}}'
    result = simulate_exec_tool("process_objects", params)
    print(f"Complex exec result: {json.dumps(result, indent=2)}")
    
    if result.get("error"):
        print("❌ Failed to execute complex function")
        return False
        
    expected_result = {"items": [1, 2, 3], "sorted": True, "count": 3}
    if result.get("result") != expected_result:
        print(f"❌ Expected result {expected_result}, got {result.get('result')}")
        return False
    
    console_output = result.get("console", "")
    if "Processing data:" not in console_output or "Config:" not in console_output:
        print(f"❌ Expected console output missing, got: {console_output}")
        return False
    
    print("✅ Complex parameters test passed")
    return True

def test_error_handling():
    """Test error handling scenarios"""
    print("\n=== Testing Error Handling ===")
    
    # Test invalid function name
    result = simulate_add_tool("invalid@name", "function test() { return 1; }")
    if not result.get("error"):
        print("❌ Expected error for invalid function name")
        return False
    print("✅ Invalid function name error handling works")
    
    # Test empty function name
    result = simulate_add_tool("", "function test() { return 1; }")
    if not result.get("error"):
        print("❌ Expected error for empty function name")
        return False
    print("✅ Empty function name error handling works")
    
    # Test empty function code
    result = simulate_add_tool("test", "")
    if not result.get("error"):
        print("❌ Expected error for empty function code")
        return False
    print("✅ Empty function code error handling works")
    
    if not MINI_RACER_AVAILABLE:
        print("⚠️  Skipping execution error tests - py-mini-racer not available")
        return True
    
    # Test nonexistent function execution
    result = simulate_exec_tool("nonexistent", '{"a":1}')
    if not result.get("error"):
        print("❌ Expected error for nonexistent function")
        return False
    print("✅ Nonexistent function error handling works")
    
    # Test invalid JSON parameters
    result = simulate_exec_tool("add_numbers", '{"a":1,}')  # invalid JSON
    if not result.get("error"):
        print("❌ Expected error for invalid JSON")
        return False
    print("✅ Invalid JSON error handling works")
    
    print("✅ Error handling tests passed")
    return True

def cleanup_test_files():
    """Clean up test files"""
    current_dir = pathlib.Path(__file__).parent
    javascript_dir = current_dir / "javascript"
    if javascript_dir.exists():
        shutil.rmtree(javascript_dir)
    print("🧹 Test files cleaned up")

def main():
    """Run all tests"""
    print("🧪 JavaScript Execution Tools Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    try:
        # Run tests
        all_passed &= test_simple_function()
        all_passed &= test_parameter_ordering()
        all_passed &= test_complex_parameters()
        all_passed &= test_error_handling()
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 All tests passed!")
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
            
    finally:
        cleanup_test_files()

if __name__ == "__main__":
    main()