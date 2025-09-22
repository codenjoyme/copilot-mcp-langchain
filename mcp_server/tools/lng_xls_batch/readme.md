# lng_xls_batch - Advanced Excel/CSV Batch Operations Tool

## Overview

The `lng_xls_batch` tool provides powerful batch operations for Excel and CSV files with expression support, allowing you to copy data, formulas, and formatting between files with flexible configurations.

## Features

- **Multi-format Support**: Works with Excel (.xlsx, .xls) and CSV files
- **Expression System**: Dynamic ranges and values using `{! expression !}` syntax
- **Flexible Copy Types**: Values, formulas, formatting, and combinations
- **Smart Insert Modes**: Replace or insert with row/column expansion  
- **CSV Integration**: CSV files treated as single-sheet Excel internally
- **Batch Processing**: Multiple operations with workspace file management

## Usage Examples

### Basic Copy Operation

```json
{
  "workspace": {
    "source": "input.xlsx",
    "target": "output.xlsx"
  },
  "operations": [
    {
      "from": "[source]Sheet1!A1:C10",
      "to": "[target]Summary!A1:C10",
      "copy": ["values", "formulas"],
      "insert": "replace"
    }
  ]
}
```

### Batch Operations with Expressions

```json
{
  "workspace": {
    "data": "raw_data.csv",
    "report": "monthly_report.xlsx"
  },
  "defaults": {
    "copy": ["values"],
    "insert": "replace"
  },
  "operations": [
    {
      "from": "{! env.REPORT_TITLE !}",
      "to": "[report]Report!A1"
    },
    {
      "from": "=SUM(B:B)",
      "to": "[report]Report!B{! row_count + 2 !}",
      "copy": ["formulas"]
    }
  ]
}
```

## Configuration Options

### Copy Types

- `"values"` - Copy cell values only
- `"formulas"` - Copy formulas only  
- `"formatting"` - Copy cell formatting only
- Combinations: `["values", "formulas"]`, `["values", "formatting"]`, etc.

### Insert Modes

- `"replace"` - Replace existing cells
- `["rows"]` - Insert new rows, shifting existing down
- `["columns"]` - Insert new columns, shifting existing right
- `["rows", "columns"]` - Insert both rows and columns

### Range Notation

- Excel files: `[fileId]SheetName!A1:C10`
- CSV files: `[fileId]A1:C10` (sheet name optional)
- Dynamic ranges: `[source]Sheet1!A1:A{! row_count !}`

## File Structure

```
lng_xls_batch/
├── settings.yaml      # Tool configuration
├── tool.py           # Main tool implementation
├── readme.md         # This documentation
└── stuff/
    └── test_basic.py # Basic test script
```

## Dependencies

- `openpyxl` - Excel file manipulation
- `pandas` - CSV file handling and data processing

## Error Handling

The tool stops execution on the first error and provides detailed error messages including:

- Operation number that failed
- Specific error description
- List of completed operations before failure

This allows LLM agents to analyze failures and take corrective action.

## Testing

Run the test script to verify functionality:

```bash
python mcp_server/tools/lng_xls_batch/stuff/test_basic.py
```

Or use the system test suite:

```bash
# See test.sh for lng_xls_batch test examples
./mcp_server/build/test.sh
```
