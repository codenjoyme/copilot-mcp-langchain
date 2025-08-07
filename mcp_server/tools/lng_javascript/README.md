# JavaScript Execution Tools

This directory contains two MCP tools for JavaScript function management and execution:

## Tools

### `lng_javascript_add`
Stores JavaScript functions for later execution.

**Parameters:**
- `function_name` (string): Name of the function (used as filename)
- `function_code` (string): Complete JavaScript function definition

**Example:**
```bash
python -m mcp_server.run run lng_javascript_add '{"function_name":"add_numbers","function_code":"function add_numbers(a, b) { console.log(\"Adding:\", a, b); return a + b; }"}'
```

### `lng_javascript_exec`
Loads and executes stored JavaScript functions.

**Parameters:**
- `function_name` (string): Name of the function to execute
- `parameters` (string): JSON string containing function parameters

**Example:**
```bash
python -m mcp_server.run run lng_javascript_exec '{"function_name":"add_numbers","parameters":"{\"a\":5,\"b\":3}"}'
```

## Key Features

- **Parameter Ordering**: JSON keys are sorted alphabetically before function call
- **Console Capture**: All `console.log` outputs are captured and returned
- **Complex Objects**: Supports nested JSON objects as function parameters
- **Error Handling**: Comprehensive error handling for all scenarios

## Dependencies

- `py-mini-racer`: Modern V8 JavaScript engine for Python

## Storage

JavaScript functions are stored as `.js` files in the `mcp_server/javascript/` directory.