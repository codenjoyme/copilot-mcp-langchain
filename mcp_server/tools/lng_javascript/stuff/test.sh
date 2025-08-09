#!/bin/bash

####################################
### activate virtual environment ###
####################################
cd ../../../../
if [ -f "./.virtualenv/Scripts/activate" ]; then
    # Windows
    . ./.virtualenv/Scripts/activate
elif [ -f "./.virtualenv/bin/activate" ]; then
    # Linux/Unix
    . ./.virtualenv/bin/activate
else
    echo "Virtual environment not found!"
    exit 1
fi

#####################
### lng_javascript ###
#####################
# Testing JavaScript function management and execution

echo "🚀 lng_javascript tool testing - comprehensive coverage"
echo

# Test 1: List functions when none exist
echo "📋 TEST 1: List functions when none exist"
python -m mcp_server.run run lng_javascript '{"command": "list"}'
echo

# Test 2: Add a simple greeting function
echo "📋 TEST 2: Add simple greeting function"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "greet", "function_code": "function greet(params) { return \"Hello, \" + params; }"}'
echo

# Test 3: Execute greeting function with string parameter
echo "📋 TEST 3: Execute greeting function with string parameter"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "greet", "parameters": "World"}'
echo

# Test 4: Add function with JSON parameters
echo "📋 TEST 4: Add function that handles JSON parameters"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "calculateSum", "function_code": "function calculateSum(params) { return params.a + params.b; }"}'
echo

# Test 5: Execute function with JSON parameters
echo "📋 TEST 5: Execute function with JSON parameters"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "calculateSum", "parameters": "{\"a\": 5, \"b\": 3}"}'
echo

# Test 6: Add complex function with modern JavaScript features
echo "📋 TEST 6: Add function with modern JavaScript features (array methods, destructuring)"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "processArray", "function_code": "function processArray(params) { const { numbers, operation } = params; if (operation === \"sum\") return numbers.reduce((a, b) => a + b, 0); if (operation === \"average\") return numbers.reduce((a, b) => a + b, 0) / numbers.length; return \"Unknown operation\"; }"}'
echo

# Test 7: Execute modern function with array sum
echo "📋 TEST 7: Execute modern function - array sum"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "processArray", "parameters": "{\"numbers\": [1, 2, 3, 4, 5], \"operation\": \"sum\"}"}'
echo

# Test 8: Execute modern function with array average
echo "📋 TEST 8: Execute modern function - array average"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "processArray", "parameters": "{\"numbers\": [10, 20, 30], \"operation\": \"average\"}"}'
echo

# Test 9: List all saved functions
echo "📋 TEST 9: List all saved functions"
python -m mcp_server.run run lng_javascript '{"command": "list"}'
echo

# Test 10: Error handling - execute nonexistent function
echo "📋 TEST 10: Error handling - execute nonexistent function"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "nonexistent", "parameters": "test"}'
echo

# Test 11: Error handling - invalid function name
echo "📋 TEST 11: Error handling - function name mismatch"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "wrongName", "function_code": "function correctName(params) { return params; }"}'
echo

# Test 12: Error handling - missing command
echo "📋 TEST 12: Error handling - missing command parameter"
python -m mcp_server.run run lng_javascript '{}'
echo

# Test 13: Error handling - missing function code
echo "📋 TEST 13: Error handling - missing function code"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "testFunc"}'
echo

# Test 14: Complex function with conditional logic
echo "📋 TEST 14: Add complex function with conditional logic"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "complexCalc", "function_code": "function complexCalc(params) { const { operation, value1, value2 } = params; switch(operation) { case \"multiply\": return value1 * value2; case \"divide\": return value2 !== 0 ? value1 / value2 : \"Division by zero\"; case \"power\": return Math.pow(value1, value2); default: return \"Unknown operation\"; } }"}'
echo

# Test 15: Execute complex function - multiplication
echo "📋 TEST 15: Execute complex function - multiplication"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "complexCalc", "parameters": "{\"operation\": \"multiply\", \"value1\": 7, \"value2\": 6}"}'
echo

# Test 16: Execute complex function - power
echo "📋 TEST 16: Execute complex function - power"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "complexCalc", "parameters": "{\"operation\": \"power\", \"value1\": 2, \"value2\": 8}"}'
echo

# Test 17: Function with string manipulation
echo "📋 TEST 17: Add function with string manipulation"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "processText", "function_code": "function processText(params) { const text = params.text || \"\"; return { original: text, uppercase: text.toUpperCase(), length: text.length, words: text.split(\" \").length, reversed: text.split(\"\").reverse().join(\"\") }; }"}'
echo

# Test 18: Execute string manipulation function
echo "📋 TEST 18: Execute string manipulation function"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "processText", "parameters": "{\"text\": \"Hello JavaScript World\"}"}'
echo

# Test 19: Function with date operations (modern JS)
echo "📋 TEST 19: Add function with date operations"
python -m mcp_server.run run lng_javascript '{"command": "add", "function_name": "dateOperations", "function_code": "function dateOperations(params) { const now = new Date(); const dayNames = [\"Sunday\", \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\"]; return { timestamp: now.getTime(), dayOfWeek: dayNames[now.getDay()], formatted: now.toISOString(), year: now.getFullYear() }; }"}'
echo

# Test 20: Execute date operations function
echo "📋 TEST 20: Execute date operations function"
python -m mcp_server.run run lng_javascript '{"command": "execute", "function_name": "dateOperations", "parameters": "{}"}'
echo

echo "🎉 lng_javascript testing completed!"
echo "All major JavaScript function management features have been tested."