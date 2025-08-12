# then ask for API keys and update .env file
# we need to set LLM_PROVIDER
# and either
# AZURE_OPENAI_API_KEY
# AZURE_OPENAI_ENDPOINT
# or 
# OPENAI_API_KEY

####################################
### activate virtual environment ###
####################################
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then    
    # Windows 
    . ./.virtualenv/Scripts/activate
else    
    # Linux/Unix 
    source ./.virtualenv/bin/activate
fi

############################################################
### to check connection to the OpenAI/Azure LLM provider ###
############################################################
python mcp_server/simple/query_openai.py 
python mcp_server/simple/query_azure.py 

############################################
### to test simple LangChain examples ###
############################################
python mcp_server/simple/rag.py
python mcp_server/simple/agent.py
python mcp_server/simple/structured_output.py
python mcp_server/simple/chain_of_thought.py
python mcp_server/simple/prompt_template.py 

##########################################
### to test MCP server with MCP client ###
##########################################
python mcp_server/test/server.py

##########################
### lng_get_tools_info ###
##########################
# it returns all available MCP tools and their descriptions
python -m mcp_server.run run lng_get_tools_info

#######################
### lng_count_words ###
#######################
# it counts words in the input text
# sample of how to run python function
python -m mcp_server.run run lng_count_words '{\"input_text\":\"Hello pirate!\"}'

#########################
### lng_llm_run_chain ###
#########################
# it runs a simple chain with the input text
# sample of how to run several python functions with langchain
python -m mcp_server.run run lng_llm_run_chain '{\"input_text\":\"Hello pirate!\"}'

##########################
### lng_llm_agent_demo ###
##########################
# it runs a simple agent demo with the input text
# sample of how to run several python functions with langchain in Agent mode
python -m mcp_server.run run lng_llm_agent_demo '{\"input_text\":\"Hello pirate!\",\"task\":\"Reverse this text and then capitalize it\"}'

#################################
### lng_llm_structured_output ###
#################################
# it formats the output in different formats
# possible output formats: json, xml, csv, yaml, pydantic

# json
python -m mcp_server.run run lng_llm_structured_output '{\"question\":\"Tell me more about Matrix\",\"output_format\":\"json\"}'

# xml
python -m mcp_server.run run lng_llm_structured_output '{\"question\":\"Tell me more about Matrix\",\"output_format\":\"xml\"}'

# csv
python -m mcp_server.run run lng_llm_structured_output '{\"question\":\"Tell me more about Matrix\",\"output_format\":\"csv\"}'

# yaml
python -m mcp_server.run run lng_llm_structured_output '{\"question\":\"Tell me more about Matrix\",\"output_format\":\"yaml\"}'

# pydantic
python -m mcp_server.run run lng_llm_structured_output '{\"question\":\"Tell me more about Matrix\",\"output_format\":\"pydantic\"}'

################################
### lng_llm_chain_of_thought ###
################################
# it runs a chain of thought with memory
# it allows to ask several questions in a row and remember the context
# demonstration of technique

# Run both questions in sequence within the same Python process to maintain memory
python -m mcp_server.run batch lng_llm_chain_of_thought '{\"question\":\"If John has 5 apples and he gives 2 to Mary, how many apples does John have left?\",\"session_id\":\"apple_problem\",\"new_session\":true}' lng_llm_chain_of_thought '{\"question\":\"If John then buys 3 more apples, how many does he have now?\",\"session_id\":\"apple_problem\",\"new_session\":false}'

###############################
### lng_llm_prompt_template ###
###############################
# demonstration of unified prompt template management with file storage
# it allows to save prompt templates to files and then use them with different parameters
# lng_llm_prompt_template - unified tool with commands: save, use, list

# Save and use a template
python -m mcp_server.run run lng_llm_prompt_template '{\"command\":\"save\",\"template_name\":\"pirate_style\",\"template\":\"Tell me about {topic} in the style of {style}.\"}'
python -m mcp_server.run run lng_llm_prompt_template '{\"command\":\"use\",\"template_name\":\"pirate_style\",\"topic\":\"artificial intelligence\",\"style\":\"a pirate\"}'

########################
### lng_rag_add_data ### 
### lng_rag_search   ###
########################
# it adds data to the RAG system and then searches for it
# demonstration of RAG tools
# NOTE: RAG search now requires a prompt template to be created first

# Run three tools in sequence: create template, add data, then search
python -m mcp_server.run batch lng_llm_prompt_template '{\"command\":\"save\",\"template_name\":\"rag_default\",\"template\":\"Based on the following context:\\n\\n{context}\\n\\nAnswer this query: {query}\"}' lng_llm_rag_add_data '{\"input_text\":\"Hello pirate!\"}' lng_llm_rag_search '{\"query\":\"Pirate\",\"prompt_template\":\"rag_default\"}'

#################################################
### WinAPI tools testing (Windows automation) ###
#################################################

#################################
### lng_winapi_list_processes ###
#################################
# try to find processes with windows
python -m mcp_server.run run lng_winapi_list_processes '{\"filter\":\"chrome\",\"only_with_windows\":true}'

##############################
### lng_winapi_window_tree ###
##############################
# show window element tree structure
python -m mcp_server.run run lng_winapi_window_tree '{\"pid\":18672}'

#####################################
### lng_winapi_get_window_content ###
#####################################
# deep analysis of window content (structure mode)
python -m mcp_server.run run lng_winapi_get_window_content '{\"pid\":18672,\"mode\":\"structure\",\"max_depth\":3}'

# text extraction mode
python -m mcp_server.run run lng_winapi_get_window_content '{\"pid\":18672,\"mode\":\"text_only\",\"max_depth\":2}'

# interactive elements only
python -m mcp_server.run run lng_winapi_get_window_content '{\"pid\":18672,\"mode\":\"interactive\",\"max_depth\":4}'

# full analysis with specific element types
python -m mcp_server.run run lng_winapi_get_window_content '{\"pid\":18672,\"mode\":\"full\",\"element_types\":[\"Button\",\"Edit\",\"Text\"],\"max_depth\":2}'

##############################
### lng_winapi_send_hotkey ###
##############################
# single hotkey (Ctrl+T for new tab)
python -m mcp_server.run run lng_winapi_send_hotkey '{\"pid\":18672,\"hotkey\":\"^t\"}'

# system key (F12 for DevTools) - uses 'key' parameter instead of 'hotkey'
python -m mcp_server.run run lng_winapi_send_hotkey '{\"pid\":18672,\"key\":\"F12\"}'

# text input - uses 'text' parameter  
python -m mcp_server.run run lng_winapi_send_hotkey '{\"pid\":18672,\"text\":\"Hello Windows Automation!\"}'

################################
### lng_winapi_clipboard_set ###
### lng_winapi_clipboard_get ###
################################
# Set text to clipboard and then read it back
python -m mcp_server.run batch lng_winapi_clipboard_set '{\"text\":\"Hello clipboard! 🎉\"}' lng_winapi_clipboard_get '{}'

# Set complex Unicode text with multiple languages
python -m mcp_server.run run lng_winapi_clipboard_set '{\"text\":\"English + Русский + 中文 + Emojis: 🚀🌍✨\"}'

# Read current clipboard content
python -m mcp_server.run run lng_winapi_clipboard_get '{}'

# Set text with custom retry attempts for busy systems
python -m mcp_server.run run lng_winapi_clipboard_set '{\"text\":\"Test with retries\",\"timeout_attempts\":20}'

#####################
### lng_batch_run ###
#####################

# Simple clipboard copy pipeline
python -m mcp_server.run run lng_batch_run '{\"pipeline\": [{\"tool\": \"lng_winapi_clipboard_get\", \"params\": {}, \"output\": \"clipboard_text\"}, {\"tool\": \"lng_winapi_clipboard_set\", \"params\": {\"text\": \"${clipboard_text.content}\"}}], \"final_result\": \"ok\"}'

# Process clipboard text with property access
python -m mcp_server.run run lng_batch_run '{\"pipeline\": [{\"tool\": \"lng_winapi_clipboard_get\", \"params\": {}, \"output\": \"clipboard_text\"}, {\"tool\": \"lng_winapi_clipboard_set\", \"params\": {\"text\": \"Processed: ${clipboard_text.content}\"}}], \"final_result\": \"${clipboard_text.success}\"}'

# Count words in clipboard and set result back
python -m mcp_server.run run lng_batch_run '{\"pipeline\": [{\"tool\": \"lng_winapi_clipboard_get\", \"params\": {}, \"output\": \"clipboard_text\"}, {\"tool\": \"lng_count_words\", \"params\": {\"input_text\": \"${clipboard_text.content}\"}, \"output\": \"word_count\"}, {\"tool\": \"lng_winapi_clipboard_set\", \"params\": {\"text\": \"Word count: ${word_count}\"}}], \"final_result\": \"completed\"}'

#########################
### lng_webhook_server ###
#########################
# Universal webhook server constructor with pipeline integration

# List existing webhooks
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"list\"}'

# Create simple webhook
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"start\",\"name\":\"simple-test\",\"port\":8080,\"path\":\"/test\",\"response\":{\"status\":200,\"body\":{\"message\":\"Hello ${webhook.body.user}!\",\"timestamp\":\"${webhook.timestamp}\"}}}'

# Create webhook with pipeline (word counting)
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"start\",\"name\":\"word-counter\",\"port\":8081,\"path\":\"/count\",\"pipeline\":[{\"tool\":\"lng_count_words\",\"params\":{\"input_text\":\"${webhook.body.message}\"},\"output\":\"stats\"}],\"response\":{\"body\":{\"word_count\":\"${stats.wordCount}\",\"original\":\"${webhook.body.message}\"}}}'

# Test webhook with HTTP request
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"test\",\"name\":\"simple-test\",\"test_data\":{\"user\":\"tester\",\"message\":\"Hello webhook!\"}}'

# Test pipeline webhook
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"test\",\"name\":\"word-counter\",\"test_data\":{\"message\":\"This is a test message with several words\"}}'

# Create and test webhook in batch mode
python -m mcp_server.run batch lng_webhook_server '{\"operation\":\"start\",\"name\":\"batch-test\",\"port\":8082,\"path\":\"/batch\",\"response\":{\"body\":{\"success\":true,\"received\":\"${webhook.body}\"}}}' lng_webhook_server '{\"operation\":\"test\",\"name\":\"batch-test\",\"test_data\":{\"message\":\"batch test\"}}'

# Stop webhooks
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"stop\",\"name\":\"simple-test\"}'
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"stop\",\"name\":\"word-counter\"}'
python -m mcp_server.run run lng_webhook_server '{\"operation\":\"stop\",\"name\":\"batch-test\"}'

# Universal test suite (comprehensive testing)
cd mcp_server/tools/lng_webhook_server/stuff && python test_webhook_universal.py && cd ../../../../

##############################
### lng_javascript_list    ###
### lng_javascript_add     ###
### lng_javascript_execute ###
##############################
# JavaScript function management and execution with PyMiniRacer

# List all saved JavaScript functions (initially empty)
python -m mcp_server.run run lng_javascript_list '{}'

# Save a simple greeting function using lng_javascript_add
python -m mcp_server.run run lng_javascript_add '{\"function_name\": \"greet\", \"function_code\": \"function greet(params) { console.log(\\\"Greeting:\\\", params); return \\\"Hello, \\\" + params; }\"}'

# Save a mathematical calculation function with console logging
python -m mcp_server.run run lng_javascript_add '{\"function_name\": \"calculateSum\", \"function_code\": \"function calculateSum(params) { console.log(\\\"Calculating sum:\\\", params); const result = params.a + params.b; console.log(\\\"Result:\\\", result); return result; }\"}'

# Save a complex calculation function with destructuring, array methods, and detailed logging
python -m mcp_server.run run lng_javascript_add '{\"function_name\": \"complexCalc\", \"function_code\": \"function complexCalc(params) { console.log(\\\"Starting complex calculation\\\", params); const { numbers, operation } = params; if (operation === \\\"sum\\\") { const result = numbers.reduce((a, b) => a + b, 0); console.log(\\\"Sum operation completed:\\\", result); return result; } if (operation === \\\"product\\\") { const result = numbers.reduce((a, b) => a * b, 1); console.log(\\\"Product operation completed:\\\", result); return result; } console.warn(\\\"Invalid operation:\\\", operation); return \\\"Invalid operation\\\"; }\"}'

# Save a function with comprehensive console logging examples
python -m mcp_server.run run lng_javascript_add '{\"function_name\": \"debugExample\", \"function_code\": \"function debugExample(params) { console.log(\\\"Function called with:\\\", JSON.stringify(params)); console.warn(\\\"This is a warning message\\\"); if (params.debug) { console.error(\\\"Debug mode enabled - showing detailed info\\\"); } const result = { input: params, timestamp: new Date().toISOString(), processed: true }; console.log(\\\"Returning result:\\\", JSON.stringify(result)); return result; }\"}'

# List all saved functions after adding them
python -m mcp_server.run run lng_javascript_list '{}'

# Execute greeting function with string parameter using lng_javascript_execute
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"greet\", \"parameters\": \"World\"}'

# Execute sum function with object parameters (recommended approach)
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"calculateSum\", \"parameters\": {\"a\": 5, \"b\": 3}}'

# Execute complex function with array sum operation
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"complexCalc\", \"parameters\": {\"numbers\": [1, 2, 3, 4], \"operation\": \"sum\"}}'

# Execute complex function with array product operation
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"complexCalc\", \"parameters\": {\"numbers\": [2, 3, 4], \"operation\": \"product\"}}'

# Execute debug function to see comprehensive console logging
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"debugExample\", \"parameters\": {\"data\": \"test\", \"debug\": true, \"options\": {\"verbose\": true}}}'

# Test complex object parameters
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"debugExample\", \"parameters\": {\"user\": {\"name\": \"John\", \"age\": 30}, \"settings\": {\"theme\": \"dark\", \"notifications\": true}, \"items\": [\"item1\", \"item2\", \"item3\"]}}'

# Test error handling - trying to execute non-existent function
python -m mcp_server.run run lng_javascript_execute '{\"function_name\": \"nonexistent\", \"parameters\": \"test\"}'

# Test error handling - trying to add arrow function (should fail)
python -m mcp_server.run run lng_javascript_add '{\"function_name\": \"arrowTest\", \"function_code\": \"const arrowTest = () => { return 1; }\"}'

# Test batch execution with pipeline - create and execute function in one pipeline
python -m mcp_server.run run lng_batch_run '{\"pipeline\": [{\"tool\": \"lng_javascript_add\", \"params\": {\"function_name\": \"quickTest\", \"function_code\": \"function quickTest(params) { console.log(\\\"Quick test:\\\", params); return \\\"OK: \\\" + JSON.stringify(params); }\"}, \"output\": \"save_result\"}, {\"tool\": \"lng_javascript_execute\", \"params\": {\"function_name\": \"quickTest\", \"parameters\": {\"message\": \"batch execution test\"}}, \"output\": \"exec_result\"}], \"final_result\": \"${exec_result}\"}'

#######################
### lng_json_to_csv ###
#######################
# JSON to CSV/Markdown converter with pandas support

### TEXT MODE TESTS ###

# Simple JSON object to CSV (new simplified format)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"field\":\"value1\"}]}'

# Simple JSON object to Markdown (new simplified format)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"field\":\"value1\"}],\"format\":\"markdown\"}'

# Multiple objects with different fields (no escaping needed!)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"name\":\"John\",\"age\":30},{\"name\":\"Jane\",\"city\":\"NYC\"}]}'

# Array handling example (clean syntax)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"field\":\"value1\",\"array\":[\"item1\",\"item2\"]},{\"field\":\"value2\",\"array\":[\"item3\",\"item4\"]}]}'

# Nested object example (much cleaner!)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"user\":{\"name\":\"John\",\"age\":30},\"settings\":{\"theme\":\"dark\"}}]}'

# Character escaping example
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"field\":\"value,with,commas\"}]}'

# Custom delimiter example (clean syntax)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"field1\":\"value1\",\"field2\":\"value2\"}],\"column_delimiter\":\"|\"}'

# Complex real-world example (GitHub Copilot analytics style - much more readable!)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":[{\"date\":\"2025-01-01\",\"users\":5,\"metrics\":{\"active\":3,\"engaged\":2},\"languages\":[{\"name\":\"java\",\"count\":10},{\"name\":\"python\",\"count\":5}]}]}'

# Single object (not array)
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":{\"name\":\"SingleUser\",\"role\":\"admin\"}}'

### FILE MODE TESTS ###

# Create test JSON file for file mode tests
echo '[{"name":"Alice","age":30,"city":"New York","hobbies":["reading","painting"]},{"name":"Bob","age":25,"city":"Los Angeles","hobbies":["gaming","cooking","hiking"]},{"name":"Charlie","age":35,"city":"Chicago","hobbies":["music"]}]' > test_input.json

# File mode: JSON to CSV conversion
python -m mcp_server.run run lng_json_to_csv '{\"input_file_path\":\"test_input.json\", \"output_file_path\":\"test_output.csv\"}'

# File mode: JSON to Markdown conversion
python -m mcp_server.run run lng_json_to_csv '{\"input_file_path\":\"test_input.json\", \"output_file_path\":\"test_output.md\", \"format\":\"markdown\"}'

# File mode: Complex data with nested directory creation
echo '[{"product":"Widget","price":15.99,"categories":{"main":"electronics","sub":"gadgets"}},{"product":"Gadget","price":25.50,"categories":{"main":"tools","sub":"automation"}}]' > test_products.json
python -m mcp_server.run run lng_json_to_csv '{\"input_file_path\":\"test_products.json\", \"output_file_path\":\"output/reports/products.csv\"}'

# File mode: Custom delimiter in file output
python -m mcp_server.run run lng_json_to_csv '{\"input_file_path\":\"test_input.json\", \"output_file_path\":\"test_custom.csv\", \"column_delimiter\":\"|\"}'

# File mode: Test error handling - nonexistent input file
python -m mcp_server.run run lng_json_to_csv '{\"input_file_path\":\"nonexistent.json\", \"output_file_path\":\"test.csv\"}'

# File mode: Test mode conflict detection
python -m mcp_server.run run lng_json_to_csv '{\"json_data\":\"[{}]\", \"input_file_path\":\"test.json\", \"output_file_path\":\"test.csv\"}'

# Display created files to verify results
echo "=== Created CSV file content ==="
cat test_output.csv
echo "=== Created Markdown file content ==="
cat test_output.md

# Clean up test files
rm -f test_input.json test_products.json test_output.csv test_output.md test_custom.csv
rm -rf output/

# Test tool functionality
cd mcp_server/tools/lng_json_to_csv/stuff && python test_runner.py && cd ../../../../

#####################
### lng_file_read ###
### lng_file_write ###
#####################
# Cross-platform file operations with encoding support and improved output formats

# Create test file for reading
echo -e "Line 1\nLine 2\nLine 3\nLine 4\nLine 5" > test_read.txt

# Read entire file (default plain text format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\"}'

# Read entire file (JSON format with metadata)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"output_format\":\"json\"}'

# Read with UTF-8 encoding (explicit, plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"encoding\":\"utf-8\"}'

# Read with UTF-8 encoding (JSON format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"encoding\":\"utf-8\",\"output_format\":\"json\"}'

# Read with offset (skip first 2 lines, plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"offset\":2}'

# Read with offset (skip first 2 lines, JSON format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"offset\":2,\"output_format\":\"json\"}'

# Read with offset and limit (lines 2-4, plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"offset\":1,\"limit\":3}'

# Read with offset and limit (lines 2-4, JSON format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"offset\":1,\"limit\":3,\"output_format\":\"json\"}'

# Test relative path (plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"./test_read.txt\"}'

# Test absolute path with JSON format (Windows compatible)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"output_format\":\"json\"}'

# Test non-existent file (returns JSON error regardless of format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"nonexistent.txt\"}'

# Test non-existent file with JSON format specified
python -m mcp_server.run run lng_file_read '{\"file_path\":\"nonexistent_json.txt\",\"output_format\":\"json\"}'

# Create new file (default create mode, returns JSON metadata)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"test_create.txt\",\"content\":\"Hello World!\\nThis is a new file.\"}'

# Try to create existing file (should fail, returns JSON error)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"test_create.txt\",\"content\":\"This should fail\",\"mode\":\"create\"}'

# Append to existing file (returns JSON metadata)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"test_create.txt\",\"content\":\"\\nAppended line 1\\nAppended line 2\",\"mode\":\"append\"}'

# Read appended file to verify (plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_create.txt\"}'

# Read appended file to verify (JSON format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_create.txt\",\"output_format\":\"json\"}'

# Overwrite existing file (returns JSON metadata with size changes)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"test_create.txt\",\"content\":\"Completely new content!\\nFile was overwritten.\",\"mode\":\"overwrite\"}'

# Read overwritten file to verify (plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_create.txt\"}'

# Create file in subdirectory (auto-create directories, JSON metadata)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"subdir/nested/deep_file.txt\",\"content\":\"File in nested directory\\nCreated automatically\"}'

# Read from nested directory (JSON format with full metadata)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"subdir/nested/deep_file.txt\",\"output_format\":\"json\"}'

# Test different encodings (Unicode characters, JSON metadata)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"utf8_test.txt\",\"content\":\"UTF-8: Hello 🌍! Русский текст. 中文字符. Émojis 🎉\",\"encoding\":\"utf-8\"}'

# Read UTF-8 file (plain text to see Unicode)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"utf8_test.txt\",\"encoding\":\"utf-8\"}'

# Read UTF-8 file (JSON format with metadata)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"utf8_test.txt\",\"encoding\":\"utf-8\",\"output_format\":\"json\"}'

# Test empty content (JSON metadata)
python -m mcp_server.run run lng_file_write '{\"file_path\":\"empty_file.txt\",\"content\":\"\"}'

# Read empty file (plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"empty_file.txt\"}'

# Read empty file (JSON format)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"empty_file.txt\",\"output_format\":\"json\"}'

# Test error handling - missing content parameter
python -m mcp_server.run run lng_file_write '{\"file_path\":\"missing_content.txt\"}'

# Test error handling - missing file_path parameter
python -m mcp_server.run run lng_file_read '{\"encoding\":\"utf-8\"}'

# Combined operations in batch mode (write + read JSON + append)
python -m mcp_server.run batch lng_file_write '{\"file_path\":\"batch_test.txt\",\"content\":\"First line\\nSecond line\\nThird line\"}' lng_file_read '{\"file_path\":\"batch_test.txt\",\"output_format\":\"json\"}' lng_file_write '{\"file_path\":\"batch_test.txt\",\"content\":\"\\nAppended in batch\",\"mode\":\"append\"}'

# Final read to see all changes (plain text)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"batch_test.txt\"}'

# Final read to see all changes (JSON format with metadata)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"batch_test.txt\",\"output_format\":\"json\"}'

# Advanced test: offset beyond file length (should return empty content)
python -m mcp_server.run run lng_file_read '{\"file_path\":\"test_read.txt\",\"offset\":100,\"output_format\":\"json\"}'

# Clean up test files
rm -f test_read.txt test_create.txt utf8_test.txt empty_file.txt batch_test.txt
rm -rf subdir/

# Test tool functionality with test script
cd mcp_server/tools/lng_file/stuff && python test.py && cd ../../../../

#####################
### lng_file_list ###
#####################
# Lists files and directories with flexible filtering and output options

# Create test directory structure for listing examples
mkdir -p test_list_dir/subdir1 test_list_dir/subdir2 test_list_dir/.hidden
echo "Content 1" > test_list_dir/file1.txt
echo "Content 2" > test_list_dir/file2.py
echo "print('hello')" > test_list_dir/script.py
echo "Hidden content" > test_list_dir/.hidden_file
echo "Nested content 1" > test_list_dir/subdir1/nested.txt
echo "Nested content 2" > test_list_dir/subdir2/another.py
echo "Hidden nested" > test_list_dir/.hidden/hidden_nested.txt

# Basic directory listing (simple format, relative paths)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\"}'

# Directory listing with absolute paths
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"path_type\":\"absolute\"}'

# List only files (exclude directories)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"include_directories\":false}'

# List only directories (exclude files)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"include_files\":false}'

# Recursive listing (all files and directories)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"recursive\":true}'

# Pattern filtering - only .py files
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"pattern\":\"*.py\",\"recursive\":true}'

# Pattern filtering - only .txt files with absolute paths
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"pattern\":\"*.txt\",\"path_type\":\"absolute\",\"recursive\":true}'

# Include hidden files and directories
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"show_hidden\":true}'

# Detailed output format (with file sizes, timestamps, permissions)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"output_format\":\"detailed\"}'

# JSON output format (full metadata)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"output_format\":\"json\"}'

# Complex example: recursive .py files with hidden files in detailed format
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"pattern\":\"*.py\",\"recursive\":true,\"show_hidden\":true,\"output_format\":\"detailed\"}'

# Complex example: all files recursively with absolute paths in JSON format
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir\",\"recursive\":true,\"show_hidden\":true,\"path_type\":\"absolute\",\"output_format\":\"json\"}'

# List current directory (using relative path)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\".\"}'

# List specific subdirectory
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir/subdir1\"}'

# Test error handling - non-existent directory
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"nonexistent_directory\"}'

# Test error handling - path is file, not directory (using one of our test files)
python -m mcp_server.run run lng_file_list '{\"directory_path\":\"test_list_dir/file1.txt\"}'

# Test error handling - missing directory_path parameter
python -m mcp_server.run run lng_file_list '{\"pattern\":\"*.txt\"}'

# Clean up test directory
rm -rf test_list_dir

##########################
### lng_pdf_extract_images ###
##########################
# PDF image extraction tool with PyMuPDF - extracts all images from PDF files

# Create a test PDF with embedded images for demonstration
echo "Creating test PDF with embedded images..."
mkdir -p /tmp/pdf_test_demo
python3 << 'EOF'
import fitz  # PyMuPDF
from PIL import Image, ImageDraw
import os

# Create test images
img1 = Image.new('RGB', (200, 150), color='lightblue')
draw1 = ImageDraw.Draw(img1)
draw1.rectangle([10, 10, 50, 50], fill='red', outline='black')
draw1.text((10, 100), "Test Image 1", fill='black')
img1.save('/tmp/pdf_test_demo/test_img1.png')

img2 = Image.new('RGB', (150, 100), color='lightgreen')
draw2 = ImageDraw.Draw(img2)
draw2.ellipse([20, 20, 130, 80], fill='purple', outline='white')
draw2.text((30, 40), "Image 2", fill='white')
img2.save('/tmp/pdf_test_demo/test_img2.png')

# Create PDF with embedded images
doc = fitz.open()
page1 = doc.new_page(width=595, height=842)
page1.insert_text((50, 50), "Test PDF - Page 1", fontsize=16)
page1.insert_image(fitz.Rect(50, 100, 250, 250), filename='/tmp/pdf_test_demo/test_img1.png')

page2 = doc.new_page(width=595, height=842)
page2.insert_text((50, 50), "Test PDF - Page 2", fontsize=16)
page2.insert_image(fitz.Rect(100, 100, 250, 200), filename='/tmp/pdf_test_demo/test_img2.png')

doc.save('/tmp/pdf_test_demo/sample_document.pdf')
doc.close()
print("Test PDF created: /tmp/pdf_test_demo/sample_document.pdf")
EOF

echo "Testing PDF image extraction..."

# Basic extraction - extracts to same directory as PDF
python -m mcp_server.run run lng_pdf_extract_images '{"pdf_path":"/tmp/pdf_test_demo/sample_document.pdf"}'

# Custom output directory and prefix
mkdir -p /tmp/pdf_extracted
python -m mcp_server.run run lng_pdf_extract_images '{"pdf_path":"/tmp/pdf_test_demo/sample_document.pdf","output_directory":"/tmp/pdf_extracted","image_prefix":"extracted_img"}'

# Test error handling - non-existent PDF file
python -m mcp_server.run run lng_pdf_extract_images '{"pdf_path":"/tmp/nonexistent.pdf"}'

# Test error handling - missing pdf_path parameter
python -m mcp_server.run run lng_pdf_extract_images '{}'

# Test error handling - directory instead of file
python -m mcp_server.run run lng_pdf_extract_images '{"pdf_path":"/tmp/pdf_test_demo"}'

# Display extracted images
echo "=== Extracted images in default location ==="
ls -la /tmp/pdf_test_demo/*.png

echo "=== Extracted images in custom location ==="
ls -la /tmp/pdf_extracted/

# Clean up test files
rm -rf /tmp/pdf_test_demo /tmp/pdf_extracted

########################
### clean all caches ###
########################
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force