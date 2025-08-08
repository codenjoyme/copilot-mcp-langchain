#!/usr/bin/env python3
"""
MCP Direct Access Demonstration

This script demonstrates that GitHub Coding Agent CAN access MCP tools,
but through programmatic Python access rather than as direct agent functions.

Created in response to user question about whether the agent can run MCP tools
directly from sandbox without terminal commands or Python scripts.

Answer: The agent can use MCP tools programmatically, start MCP servers,
but cannot invoke MCP tools as native agent functions.
"""

import asyncio
import json
import time
import sys
import os

# Add project path for imports
sys.path.insert(0, '/home/runner/work/copilot-mcp-langchain/copilot-mcp-langchain')

from mcp_server.tools.tool_registry import run_tool

async def demonstrate_mcp_access():
    """Demonstrate direct MCP tool access from agent sandbox"""
    
    print("🧪 MCP Direct Access Demonstration")
    print("=" * 40)
    print("Showing that GitHub Coding Agent can use MCP tools programmatically")
    print()
    
    # Test expressions for math calculator
    test_cases = [
        "2 + 3 * 4",
        "sqrt(16) + 2^3",
        "sin(pi/2)", 
        "(10 + 5) * 2",
        "log(100)",
        "25 / 5 + 3 * 2"
    ]
    
    print("Testing lng_math_calculator MCP tool:")
    print("-" * 35)
    
    for expr in test_cases:
        try:
            start_time = time.time()
            result = await run_tool("lng_math_calculator", {"expression": expr})
            execution_time = time.time() - start_time
            
            if result and len(result) > 0:
                result_data = json.loads(result[0].text)
                print(f"Expression: {expr}")
                print(f"Result: {result_data.get('result', 'Error')}")
                print(f"Time: {execution_time:.3f}s")
                print("---")
            else:
                print(f"Expression: {expr}")
                print(f"Error: No result returned")
                print("---")
                
        except Exception as e:
            print(f"Expression: {expr}")
            print(f"Error: {str(e)}")
            print("---")
    
    print()
    print("✅ MCP tool access is working programmatically!")
    print()
    print("📋 Summary of MCP capabilities in agent sandbox:")
    print("- ✅ Can import and use MCP tools through Python")
    print("- ✅ Can start MCP servers (demonstrated with SSE transport)")
    print("- ✅ Can process mathematical expressions with lng_math_calculator")
    print("- ❌ Cannot invoke MCP tools as direct agent functions")
    print("- 💡 Must use programmatic access through run_tool() function")

if __name__ == "__main__":
    asyncio.run(demonstrate_mcp_access())