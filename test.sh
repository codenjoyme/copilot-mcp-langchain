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
. ./.virtualenv/bin/activate

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
### lng_prompt_template_save ### lng_prompt_template_use ###
############################################################
# demonstration of prompting with templates technique
# it allows to save a prompt template and then use it with different parameters
# lng_llm_prompt_template_save - saves a template
# lng_llm_prompt_template_use - uses a saved template with parameters

# Run both save and use in sequence within the same Python process to maintain template in memory
python -m mcp_server.run batch lng_llm_prompt_template_save '{\"template\":\"Tell me about {topic} in the style of {style}.\"}' lng_llm_prompt_template_use '{\"topic\":\"artificial intelligence\",\"style\":\"a pirate\"}'

###########################################
### lng_rag_add_data ### lng_rag_search ###
###########################################
# it adds data to the RAG system and then searches for it
# demonstration of RAG tools

# Run both add data and search in sequence within the same Python process
python -m mcp_server.run batch lng_llm_rag_add_data '{\"input_text\":\"Hello pirate!\"}' lng_llm_rag_search '{\"query\":\"Pirate\"}'

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

########################
### clean all caches ###
########################
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force