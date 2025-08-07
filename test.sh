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
. ./.virtualenv/Scripts/activate

############################################################
### to check connection to the OpenAI/Azure LLM provider ###
############################################################
python simple_openai.py 
python simple_azure.py 
python simple_both.py 

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

#####################
### lng_llm_run_chain ###
#####################
# it runs a simple chain with the input text
# sample of how to run several python functions with langchain
python -m mcp_server.run run lng_llm_run_chain '{\"input_text\":\"Hello pirate!\"}'

######################
### lng_llm_agent_demo ###
######################
# it runs a simple agent demo with the input text
# sample of how to run several python functions with langchain in Agent mode
python -m mcp_server.run run lng_llm_agent_demo '{\"input_text\":\"Hello pirate!\",\"task\":\"Reverse this text and then capitalize it\"}'

#############################
### lng_llm_structured_output ###
#############################
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

############################
### lng_llm_chain_of_thought ###
############################
# it runs a chain of thought with memory
# it allows to ask several questions in a row and remember the context
# demonstration of technique

# Run both questions in sequence within the same Python process to maintain memory
python -m mcp_server.run batch lng_llm_chain_of_thought '{\"question\":\"If John has 5 apples and he gives 2 to Mary, how many apples does John have left?\",\"session_id\":\"apple_problem\",\"new_session\":true}' lng_llm_chain_of_thought '{\"question\":\"If John then buys 3 more apples, how many does he have now?\",\"session_id\":\"apple_problem\",\"new_session\":false}'

############################################################
### lng_llm_prompt_template ###
###############################
# demonstration of unified prompt template management with file storage
# it allows to save prompt templates to files and then use them with different parameters
# lng_llm_prompt_template - unified tool with commands: save, use, list

# Save and use a template
python -m mcp_server.run run lng_llm_prompt_template '{\"command\":\"save\",\"template_name\":\"pirate_style\",\"template\":\"Tell me about {topic} in the style of {style}.\"}'
python -m mcp_server.run run lng_llm_prompt_template '{\"command\":\"use\",\"template_name\":\"pirate_style\",\"topic\":\"artificial intelligence\",\"style\":\"a pirate\"}'

###########################################
### lng_rag_add_data ### lng_rag_search ###
###########################################
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

##################################
### lng_winapi_clipboard_set   ###
### lng_winapi_clipboard_get   ###
##################################
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

#############################
### lng_javascript_add    ###
### lng_javascript_exec   ###
#############################
# JavaScript execution tools for storing and running JavaScript functions

# Store a simple function
python -m mcp_server.run run lng_javascript_add '{\"function_name\":\"add_numbers\",\"function_code\":\"function add_numbers(a, b) { console.log(\\\"Adding:\\\", a, b); return a + b; }\"}'

# Execute the function with simple parameters
python -m mcp_server.run run lng_javascript_exec '{\"function_name\":\"add_numbers\",\"parameters\":\"{\\\"a\\\":5,\\\"b\\\":3}\"}'

# Store a complex function that works with objects
python -m mcp_server.run run lng_javascript_add '{\"function_name\":\"process_objects\",\"function_code\":\"function process_objects(config, data) { console.log(\\\"Processing data:\\\", JSON.stringify(data)); console.log(\\\"Config:\\\", JSON.stringify(config)); return { items: data.items, sorted: config.sort, count: data.items.length }; }\"}'

# Execute with complex parameters (note alphabetical key order: config, data)
python -m mcp_server.run run lng_javascript_exec '{\"function_name\":\"process_objects\",\"parameters\":\"{\\\"data\\\":{\\\"items\\\":[1,2,3]},\\\"config\\\":{\\\"sort\\\":true}}\"}'

# Test parameter ordering with different JSON key order
python -m mcp_server.run run lng_javascript_exec '{\"function_name\":\"add_numbers\",\"parameters\":\"{\\\"b\\\":10,\\\"a\\\":5}\"}'

########################
### clean all caches ###
########################
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force