- If you need to test the tool after creation or modification do the following:
```bash
python -m mcp_server.run run lng_winapi_window_tree '{\"pid\":18672}'
```
- If you need to run two or more tools together, you can run them in parallel with bathch command:
```bash
python -m mcp_server.run batch lng_llm_rag_add_data '{\"input_text\":\"Hello pirate!\"}' lng_llm_rag_search '{\"query\":\"Pirate\"}'
```
- Log file in this case will be `mcp_server/logs/mcp_runner.log`.
- Always use single quotes for the json parameter string, and escape double quotes within that string with a slash.
Not:
```bash
python -m mcp_server.run run lng_count_words '{"input_text":"Hello world! This is a test."}'
```
Not:
```bash
python -m mcp_server.run run lng_count_words "{`"input_text`":`"Hello world! This is a test.`"}"
```
But:
```bash
python -m mcp_server.run run lng_count_words '{\"input_text\":\"Hello world! This is a test.\"}'
```
- But if you were asked to test a new tool via MCP explicitly, then always ask after the changes if the server was restarted, as this is done manually.
- If an error occurred during testing through MCP, report it as `FAIL` even if testing through `python -m mcp_server.run run` gave a positive result. 
