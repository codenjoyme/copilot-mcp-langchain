- When you create a new tool, pay attention to the `settings.yaml` file.
- Always pay attention to how `settings.yaml` is used in other tools. Don't create unnecessary constructs.  
  + One field `enabled: true|false`.
  + One field `description: With short summary of this tool`.
  + And `dependencies: list of pip install libraries`
  + Only `pip install` libraries should be added to dependencies.
- Dependencies in these files are inherited from the parent files.
- When creating a new tool, use only English. Respond to me in the language I used.
- When creating a tool group, look for the most appropriate location - the group may already exist.
- If you are creating a paired tool for an existing tool, it makes sense to regroup them both with a new category.
- Pay attention to dependencies - they may indicate group membership.
- If it is a new group, then specify a category folder, e.g. `lng_llm` then a subcategory `rag` and then the tools `add_data` and `search`.
- If the tool (or group) is complex - you can create a `readme.md` file.
- When creating `readme.md` don't overuse details, only useful things in essence, like how `stuff` scripts are used.
- If useful scripts were created to test the tool and their usefulness is justified, create a `stuff` folder next to `tool.py` or a level higher in the category if the tools group is linked through this `stuff`.
- Also add examples of how to use the new tool in `./mcp_server/build/test.sh`.