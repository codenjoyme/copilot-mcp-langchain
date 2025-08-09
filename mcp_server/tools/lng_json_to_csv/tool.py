import mcp.types as types
import json
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import re

async def tool_info() -> dict:
    """Returns information about the lng_json_to_csv tool."""
    return {
        "description": """Converts JSON data to CSV or Markdown format using pandas.

**Parameters:**
- `json_data` (string, required): The JSON data to convert.
- `format` (string, optional): Output format - 'csv' or 'markdown'. Default: 'csv'.
- `column_delimiter` (string, optional): Column separator. Default: ','.
- `cell_left_delimiter` (string, optional): Left cell delimiter for escaping. Default: '"'.
- `cell_right_delimiter` (string, optional): Right cell delimiter for escaping. Default: '"'.
- `line_chars_need_to_be_escaped_with_cell_delimiter` (string, optional): Characters that need escaping. Default: '\\n",'.
- `header_delimiter` (string, optional): Header delimiter for markdown format. Default: null.
- `line_replacements` (array, optional): String replacements like ["\\"==>\\"\\""]. Default: ["\\"==>\\"\\""]. 
- `padding_to_max_cell_length` (boolean, optional): Pad cells to max length. Default: false.
- `remove_headers_duplicates` (boolean, optional): Remove duplicate headers. Default: true.

**Example Usage:**
- Convert simple JSON array to CSV
- Support complex nested structures
- Handle arrays within objects
- Escape special characters properly

This tool flattens nested JSON structures into tabular format, preserving hierarchy through column headers.""",
        "schema": {
            "type": "object",
            "properties": {
                "json_data": {
                    "type": "string",
                    "description": "JSON data to convert to CSV/Markdown"
                },
                "format": {
                    "type": "string",
                    "enum": ["csv", "markdown"],
                    "default": "csv",
                    "description": "Output format"
                },
                "column_delimiter": {
                    "type": "string",
                    "default": ",",
                    "description": "Column delimiter"
                },
                "cell_left_delimiter": {
                    "type": "string",
                    "default": "\"",
                    "description": "Left cell delimiter for escaping"
                },
                "cell_right_delimiter": {
                    "type": "string", 
                    "default": "\"",
                    "description": "Right cell delimiter for escaping"
                },
                "line_chars_need_to_be_escaped_with_cell_delimiter": {
                    "type": "string",
                    "default": "\n\",",
                    "description": "Characters that need escaping"
                },
                "header_delimiter": {
                    "type": ["string", "null"],
                    "default": None,
                    "description": "Header delimiter (for markdown)"
                },
                "line_replacements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["\"==>\"\""],
                    "description": "String replacements"
                },
                "padding_to_max_cell_length": {
                    "type": "boolean",
                    "default": False,
                    "description": "Pad cells to max length"
                },
                "remove_headers_duplicates": {
                    "type": "boolean",
                    "default": True,
                    "description": "Remove duplicate headers"
                }
            },
            "required": ["json_data"]
        }
    }

class Matrix:
    """Handles the tabular structure for JSON conversion."""
    
    def __init__(self):
        self.data: List[List[Optional[str]]] = []
        self.current_header = 0
        self.header_size = 1
        self.current_line = 0
        self.base_line = 0
        self.new_line_flag = False
        
    def insert_row(self, row_index: int):
        """Insert a new row at the specified index."""
        new_row = []
        if self.data:
            # Fill with None values to match existing column count
            for _ in range(len(self.data[0]) if self.data else 0):
                new_row.append(None)
        self.data.insert(row_index, new_row)
        
    def insert_column(self, col_index: int):
        """Insert a new column at the specified index."""
        for row in self.data:
            row.insert(col_index, None)
            
    def get_or_create_header(self, key: str) -> int:
        """Get the column index for a key, creating it if needed."""
        # Ensure header row exists
        if len(self.data) <= self.current_header:
            self.insert_row(self.current_header)
            self.current_line += 1
            self.base_line += 1
            
        header = self.data[self.current_header]
        
        # Check if key already exists
        for i, header_key in enumerate(header):
            if key == header_key:
                return i
                
        # For top-level headers, just append
        if self.current_header == 0:
            self.insert_column(len(header))
            header[-1] = key
            return len(header) - 1
            
        # For nested headers, find parent position
        parent_key = key[:key.rfind(".")]
        parent_pos = -1
        
        if self.current_header > 0:
            parent_header = self.data[self.current_header - 1]
            for i, parent_header_key in enumerate(parent_header):
                if parent_header_key == parent_key:
                    parent_pos = i
                    break
                    
        if parent_pos == -1:
            raise ValueError(f"Parent key not found: {parent_key}")
            
        # Check if parent position is empty
        if parent_pos >= len(header) or header[parent_pos] is None:
            # Ensure header is long enough
            while len(header) <= parent_pos:
                header.append(None)
            header[parent_pos] = key
            return parent_pos
            
        # Find next available position after parent
        new_pos = parent_pos
        while new_pos < len(header) and header[new_pos] is not None:
            value = header[new_pos]
            if value and not value.startswith(parent_key):
                break
            new_pos += 1
            
        # Insert new column
        self.insert_column(new_pos)
        header[new_pos] = key
        return new_pos
        
    def set(self, y: int, x: int, value: str):
        """Set a value at the specified position."""
        # Ensure row exists
        while len(self.data) <= y:
            self.data.append([])
            
        # Ensure column exists
        while len(self.data[y]) <= x:
            self.data[y].append(None)
            
        self.data[y][x] = value
        
    def child_header(self):
        """Move to child header level."""
        self.current_header += 1
        if self.current_header == self.header_size:
            self.insert_row(self.header_size)
            self.header_size += 1
            self.base_line += 1
            self.current_line += 1
            
    def parent_header(self):
        """Move back to parent header level."""
        self.current_header -= 1
        if self.current_header < 0:
            self.current_header = 0
            
    def inject(self, x: int, same_line: bool, value: str):
        """Inject a value at the specified column."""
        if self.new_line_flag:
            self.base_line = len(self.data)
            self.current_line = self.base_line - 1
            self.new_line_flag = False
            
        if same_line:
            if (self.base_line < len(self.data) and 
                x < len(self.data[self.base_line]) and 
                self.data[self.base_line][x] is None):
                self.current_line = self.base_line
        else:
            self.current_line += 1
            if self.current_line >= len(self.data):
                self.insert_row(len(self.data))
                
        self.set(self.current_line, x, value)
        
    def new_line(self):
        """Mark that we need a new line."""
        self.new_line_flag = True
        
    def remove_headers_duplicates(self):
        """Remove duplicate parts of headers."""
        for y in range(self.header_size):
            if y >= len(self.data):
                continue
            row = self.data[y]
            for x in range(len(row)):
                value = row[x]
                if value is None or value == "":
                    continue
                    
                value_prefix = value + "."
                for yy in range(y + 1, self.header_size):
                    if yy >= len(self.data):
                        continue
                    next_row = self.data[yy]
                    for xx in range(len(row)):
                        if xx >= len(next_row):
                            continue
                        value2 = next_row[xx]
                        if value2 and value2.startswith(value_prefix):
                            next_row[xx] = value2[len(value_prefix):]
                            
    def to_string(self, column_delimiter: str = ",", cell_left_delimiter: Optional[str] = "\"", 
                  cell_right_delimiter: Optional[str] = "\"", 
                  line_chars_need_to_be_escaped_with_cell_delimiter: Optional[str] = "\n\",",
                  header_delimiter: Optional[str] = None,
                  line_replacements: Optional[List[str]] = None,
                  padding_to_max_cell_length: bool = False) -> str:
        """Convert matrix to string format."""
        
        # Parse line replacements
        replacements = []
        if line_replacements:
            for replacement in line_replacements:
                if "==>" in replacement:
                    parts = replacement.split("==>", 1)
                    replacements.append((parts[0], parts[1]))
                    
        result = []
        max_line_length = 0
        header_delimiter_pos = 0
        
        for y in range(len(self.data)):
            row = self.data[y]
            line_parts = []
            line_length = 0
            
            # Ensure all rows have same length
            max_cols = max(len(r) for r in self.data) if self.data else 0
            while len(row) < max_cols:
                row.append(None)
                
            for x in range(len(row)):
                value = row[x] if row[x] is not None else ""
                
                # Apply line replacements
                for old, new in replacements:
                    value = value.replace(old, new)
                    
                # Check if escaping is needed
                escape = False
                if (line_chars_need_to_be_escaped_with_cell_delimiter and
                    any(c in value for c in line_chars_need_to_be_escaped_with_cell_delimiter)):
                    escape = True
                    
                # Add delimiters if escaping
                if cell_left_delimiter and escape:
                    line_parts.append(cell_left_delimiter)
                    line_length += len(cell_left_delimiter)
                    
                line_parts.append(value)
                line_length += len(value)
                
                if cell_right_delimiter and escape:
                    line_parts.append(cell_right_delimiter)
                    line_length += len(cell_right_delimiter)
                    
                # Add padding if requested
                if padding_to_max_cell_length:
                    max_length = self._get_max_cell_length(x)
                    padding = max_length - len(value)
                    if padding > 0:
                        line_parts.append(" " * padding)
                        line_length += padding
                        
                # Add column delimiter (except for last column)
                if x < len(row) - 1:
                    line_parts.append(column_delimiter)
                    line_length += len(column_delimiter)
                    
            max_line_length = max(max_line_length, line_length)
            result.append("".join(line_parts))
            
        # Add header delimiter if specified (after all header rows)
        if header_delimiter is not None:
            header_line = header_delimiter * max_line_length
            if max_line_length > 0:
                header_line = header_line[:max_line_length]
            # Insert after header rows (at position header_size)
            result.insert(self.header_size, header_line)
            
        return "\n".join(result) + "\n"
        
    def _get_max_cell_length(self, x: int) -> int:
        """Get maximum cell length for a column."""
        max_length = 0
        for row in self.data:
            if x < len(row) and row[x] is not None:
                max_length = max(max_length, len(row[x]))
        return max_length

def process_element(matrix: Matrix, obj: Any, prefix: str, same_line: bool, depth: int):
    """Process a JSON element recursively."""
    x = 0
    if prefix:
        x = matrix.get_or_create_header(prefix)
        
    if isinstance(obj, dict):
        if depth > 1:
            matrix.child_header()
            
        for key, value in obj.items():
            new_key = f"{prefix}.{key}" if prefix else key
            process_element(matrix, value, new_key, same_line, depth + 1)
            same_line = True
            
        if depth > 1:
            matrix.parent_header()
            
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if depth == 0:
                matrix.new_line()
            else:
                same_line = (i == 0)
            process_element(matrix, item, prefix, same_line, depth + 1)
            
    else:
        matrix.inject(x, same_line, str(obj))

def json_to_csv(json_data: str, 
                column_delimiter: str = ",",
                cell_left_delimiter: Optional[str] = "\"",
                cell_right_delimiter: Optional[str] = "\"", 
                line_chars_need_to_be_escaped_with_cell_delimiter: Optional[str] = "\n\",",
                header_delimiter: Optional[str] = None,
                line_replacements: Optional[List[str]] = None,
                padding_to_max_cell_length: bool = False,
                remove_headers_duplicates: bool = True) -> str:
    """Convert JSON to CSV format."""
    
    # Only set default line replacements if None
    if line_replacements is None:
        line_replacements = ["\"==>\"\""]
        
    # Parse JSON
    data = json.loads(json_data)
    
    # Create matrix
    matrix = Matrix()
    
    # Process data
    process_element(matrix, data, "", False, 0)
    
    # Remove header duplicates if requested
    if remove_headers_duplicates:
        matrix.remove_headers_duplicates()
        
    # Convert to string
    return matrix.to_string(
        column_delimiter=column_delimiter,
        cell_left_delimiter=cell_left_delimiter, 
        cell_right_delimiter=cell_right_delimiter,
        line_chars_need_to_be_escaped_with_cell_delimiter=line_chars_need_to_be_escaped_with_cell_delimiter,
        header_delimiter=header_delimiter,
        line_replacements=line_replacements,
        padding_to_max_cell_length=padding_to_max_cell_length
    )

def json_to_markdown(json_data: str) -> str:
    """Convert JSON to Markdown table format."""
    return json_to_csv(
        json_data,
        column_delimiter="|",
        cell_left_delimiter=None,
        cell_right_delimiter=None,
        line_chars_need_to_be_escaped_with_cell_delimiter=None,
        header_delimiter="-",
        line_replacements=[],  # Empty list to avoid replacements
        padding_to_max_cell_length=True,
        remove_headers_duplicates=True
    )

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Convert JSON data to CSV or Markdown format."""
    try:
        # Extract parameters
        json_data = parameters.get("json_data", "")
        format_type = parameters.get("format", "csv")
        
        if not json_data:
            return [types.TextContent(type="text", text='{"error": "No JSON data provided."}')]
            
        # Validate JSON
        try:
            json.loads(json_data)
        except json.JSONDecodeError as e:
            return [types.TextContent(type="text", text=f'{{"error": "Invalid JSON: {str(e)}"}}')]
            
        # Get conversion parameters
        column_delimiter = parameters.get("column_delimiter", ",")
        cell_left_delimiter = parameters.get("cell_left_delimiter", "\"")
        cell_right_delimiter = parameters.get("cell_right_delimiter", "\"")
        line_chars_need_to_be_escaped_with_cell_delimiter = parameters.get(
            "line_chars_need_to_be_escaped_with_cell_delimiter", "\n\","
        )
        header_delimiter = parameters.get("header_delimiter", None)
        line_replacements = parameters.get("line_replacements", ["\"==>\"\""])
        padding_to_max_cell_length = parameters.get("padding_to_max_cell_length", False)
        remove_headers_duplicates = parameters.get("remove_headers_duplicates", True)
        
        # Convert based on format
        if format_type == "markdown":
            result = json_to_markdown(json_data)
        else:
            result = json_to_csv(
                json_data,
                column_delimiter=column_delimiter,
                cell_left_delimiter=cell_left_delimiter,
                cell_right_delimiter=cell_right_delimiter,
                line_chars_need_to_be_escaped_with_cell_delimiter=line_chars_need_to_be_escaped_with_cell_delimiter,
                header_delimiter=header_delimiter,
                line_replacements=line_replacements,
                padding_to_max_cell_length=padding_to_max_cell_length,
                remove_headers_duplicates=remove_headers_duplicates
            )
            
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}))]