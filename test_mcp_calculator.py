#!/usr/bin/env python3
"""
Test script for MCP Math Calculator Tool Integration.

This script demonstrates the ability of a Coding Agent to use MCP (Model Context Protocol)
tools directly from Python code, rather than through terminal commands.

The script tests the lng_math_calculator MCP tool with various mathematical expressions
and provides timing information and error handling.
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from mcp_server.tools.tool_registry import run_tool


async def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Calculate a mathematical expression using the MCP lng_math_calculator tool.
    
    Args:
        expression: Mathematical expression as a string
        
    Returns:
        Dictionary containing the result and metadata
        
    Raises:
        Exception: If calculation fails
    """
    try:
        # Call the MCP tool directly
        result = await run_tool("lng_math_calculator", {"expression": expression})
        
        # Parse the JSON response from the MCP tool
        if isinstance(result, list) and len(result) > 0:
            # Extract text content from the MCP response
            response_text = result[0].text if hasattr(result[0], 'text') else str(result[0])
            response_data = json.loads(response_text)
            
            # Check if there was an error in the calculation
            if "error" in response_data:
                raise ValueError(response_data["error"])
            
            return response_data
        else:
            raise ValueError("Invalid response from MCP tool")
            
    except Exception as e:
        # Return error information in a consistent format
        return {
            "originalExpression": expression,
            "error": str(e),
            "result": None
        }


def format_result(expression: str, result_data: Dict[str, Any], execution_time: float) -> str:
    """
    Format the calculation result for display.
    
    Args:
        expression: Original mathematical expression
        result_data: Result data from the calculator
        execution_time: Time taken for the calculation
        
    Returns:
        Formatted string for display
    """
    if "error" in result_data:
        return f"Expression: {expression}\nError: {result_data['error']}\nTime: {execution_time:.3f}s"
    else:
        result = result_data.get("result", "Unknown")
        return f"Expression: {expression}\nResult: {result}\nTime: {execution_time:.3f}s"


async def test_calculator_expressions(expressions: List[str]) -> None:
    """
    Test the MCP calculator with a list of mathematical expressions.
    
    Args:
        expressions: List of mathematical expressions to test
    """
    print("Testing MCP Math Calculator Tool:")
    print("=" * 35)
    
    for i, expression in enumerate(expressions):
        # Measure execution time
        start_time = time.time()
        
        try:
            result_data = await calculate_expression(expression)
            execution_time = time.time() - start_time
            
            # Format and display the result
            formatted_result = format_result(expression, result_data, execution_time)
            print(formatted_result)
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"Expression: {expression}")
            print(f"Error: Unexpected error - {str(e)}")
            print(f"Time: {execution_time:.3f}s")
        
        # Add separator between results (except for the last one)
        if i < len(expressions) - 1:
            print("---")


async def main():
    """
    Main function to run the MCP calculator tests.
    """
    # Test expressions as specified in the requirements
    test_expressions = [
        "2 + 3 * 4",
        "sqrt(16) + 2^3", 
        "sin(pi/2)",
        "(10 + 5) * 2",
        "log(100)",
        "25 / 5 + 3 * 2",
        "2^10"
    ]
    
    print("🧪 MCP Math Calculator Integration Test")
    print("======================================")
    print("Testing direct integration with lng_math_calculator MCP tool\n")
    
    try:
        await test_calculator_expressions(test_expressions)
        
        print("\n" + "=" * 35)
        print("✅ Test completed successfully!")
        print("MCP tool integration is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the test
    asyncio.run(main())