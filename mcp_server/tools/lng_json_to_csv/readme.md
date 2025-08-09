# JSON to CSV/Markdown Converter

A comprehensive MCP tool for converting JSON data to CSV or Markdown table formats using pandas. This tool handles complex nested JSON structures and provides flexible formatting options.

## Features

- **Pure Python Implementation**: Uses pandas for efficient data processing
- **Complex JSON Support**: Handles deeply nested objects, arrays, and mixed structures
- **Dual Output Formats**: Converts to both CSV and Markdown table formats
- **Flexible Configuration**: Supports all formatting parameters from the reference implementation
- **Proper Escaping**: Handles special characters (commas, quotes, newlines) correctly
- **Header Management**: Intelligent column header generation for nested structures

## Usage

### Basic Conversion

```python
# Simple JSON array to CSV
json_data = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
result = convert_json_to_csv(json_data, format="csv")
```

### Advanced Configuration

```python
# Custom formatting options
result = convert_json_to_csv(
    json_data='[{"field": "value,with,commas"}]',
    format="csv",
    column_delimiter=",",
    cell_left_delimiter='"',
    cell_right_delimiter='"',
    remove_headers_duplicates=True
)
```

### Markdown Output

```python
# Generate Markdown table
result = convert_json_to_csv(json_data, format="markdown")
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json_data` | string | required | JSON data to convert |
| `format` | string | "csv" | Output format: "csv" or "markdown" |
| `column_delimiter` | string | "," | Column separator |
| `cell_left_delimiter` | string | "\"" | Left cell delimiter for escaping |
| `cell_right_delimiter` | string | "\"" | Right cell delimiter for escaping |
| `line_chars_need_to_be_escaped_with_cell_delimiter` | string | "\n\"," | Characters requiring escaping |
| `header_delimiter` | string/null | null | Header delimiter ("-" for markdown) |
| `line_replacements` | array | ["\"==>\"\""] | String replacements for escaping |
| `padding_to_max_cell_length` | boolean | false | Pad cells to maximum length |
| `remove_headers_duplicates` | boolean | true | Remove duplicate header parts |

## Examples

### Simple Object

**Input:**
```json
[{"field": "value1"}]
```

**CSV Output:**
```
field
value1
```

**Markdown Output:**
```
field 
------
value1
```

### Array Handling

**Input:**
```json
[
  {"field": "value1", "array": ["item1", "item2"]},
  {"field": "value2", "array": ["item3", "item4"]}
]
```

**CSV Output:**
```
field,array
value1,item1
,item2
value2,item3
,item4
```

### Nested Objects

**Input:**
```json
[
  {
    "user": {"name": "John", "age": 30},
    "settings": {"theme": "dark"}
  }
]
```

**CSV Output:**
```
user.name,user.age,settings.theme
John,30,dark
```

### Character Escaping

**Input:**
```json
[{"field": "value,with,commas"}]
```

**CSV Output:**
```
field
"value,with,commas"
```

## Testing

The tool includes comprehensive tests covering:

- Simple objects and arrays
- Character escaping (commas, quotes, newlines)
- Nested structures
- Arrays of different lengths
- Complex real-world data scenarios

Run tests from the `stuff/` directory:

```bash
cd mcp_server/tools/lng_json_to_csv/stuff
python test_runner.py -v
```

## Technical Implementation

The tool uses a Matrix-based approach to build tabular data:

1. **JSON Parsing**: Recursively processes JSON elements
2. **Matrix Building**: Constructs a dynamic table structure
3. **Header Management**: Creates hierarchical column headers for nested data
4. **Formatting**: Applies escaping, padding, and delimiter rules
5. **Output Generation**: Produces CSV or Markdown formatted strings

This implementation matches the reference Java logic exactly while leveraging Python's strengths for data manipulation.