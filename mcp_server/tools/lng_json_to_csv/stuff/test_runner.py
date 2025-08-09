"""
Test runner for the JSON to CSV conversion tests without MCP dependencies.
"""
import unittest
import sys
import os
import json

# Add the parent directory to the path to import the tool functions
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the standalone test functions
from simple_test import json_to_csv, json_to_markdown

class JsonToCsvTest(unittest.TestCase):
    """Test cases matching the Java JsonToCsvTest.java implementation."""
    
    def assert_conversion(self, input_json: str, expected_csv: str, expected_markdown: str):
        """Helper method to assert both CSV and Markdown conversion."""
        actual_csv = json_to_csv(input_json)
        actual_markdown = json_to_markdown(input_json)
        
        # Compare CSV output
        self.assertEqual(expected_csv, actual_csv, 
                        f"CSV conversion failed.\nExpected:\n{repr(expected_csv)}\nActual:\n{repr(actual_csv)}")
        
        # Compare Markdown output  
        self.assertEqual(expected_markdown, actual_markdown,
                        f"Markdown conversion failed.\nExpected:\n{repr(expected_markdown)}\nActual:\n{repr(actual_markdown)}")
    
    def test_json_to_csv_simple_one_object_one_field(self):
        """Test conversion of simple JSON object with one field to CSV."""
        input_json = """[
    {
        "field": "value1"
    }
]"""
        
        expected_csv = """field
value1
"""
        
        expected_markdown = """field 
------
value1
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_comma(self):
        """Test conversion with comma escaping."""
        input_json = """[
    {
        "field": "val,ue1"
    }
]"""
        
        expected_csv = """field
"val,ue1"
"""
        
        expected_markdown = """field  
-------
val,ue1
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_quote(self):
        """Test conversion with quote escaping."""
        input_json = """[
    {
        "field": "val\\"ue1"
    }
]"""
        
        expected_csv = """field
"val""ue1"
"""
        
        expected_markdown = """field  
-------
val"ue1
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_new_line(self):
        """Test conversion with newline escaping."""
        input_json = """[
    {
        "field": "val\\nue1"
    }
]"""
        
        expected_csv = """field
"val
ue1"
"""
        
        expected_markdown = """field  
-------
val
ue1
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
    
    def test_json_to_csv_simple_two_objects_one_field(self):
        """Test conversion of two objects with one field."""
        input_json = """[
    {
        "field": "value1"
    },
    {
        "field": "value2"
    }
]"""
        
        expected_csv = """field
value1
value2
"""
        
        expected_markdown = """field 
------
value1
value2
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_simple_one_object_two_fields(self):
        """Test conversion of one object with two fields."""
        input_json = """[
    {
        "field1": "value1",
        "field2": "value2"
    }
]"""
        
        expected_csv = """field1,field2
value1,value2
"""
        
        expected_markdown = """field1|field2
-------------
value1|value2
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_simple_two_objects_two_fields(self):
        """Test conversion of two objects with two fields."""
        input_json = """[
    {
        "field1": "value1",
        "field2": "value2"
    },
    {
        "field1": "value3",
        "field2": "value4"
    }
]"""
        
        expected_csv = """field1,field2
value1,value2
value3,value4
"""
        
        expected_markdown = """field1|field2
-------------
value1|value2
value3|value4
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_simple(self):
        """Test conversion with different fields per object."""
        input_json = """[
    {
        "zField": "value3",
        "aField": "value1"
    },
    {
        "zField": "test",
        "name": "example"
    }
]"""
        
        expected_csv = """zField,aField,name
value3,value1,
test,,example
"""
        
        expected_markdown = """zField|aField|name   
---------------------
value3|value1|       
test  |      |example
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_sub_array_case_simple(self):
        """Test conversion with simple sub-arrays."""
        input_json = """[
    {
        "field": "value1",
        "array": ["value2", "value3"]
    },
    {
        "field": "value4",
        "array": ["value5", "value6"]
    }
]"""
        
        expected_csv = """field,array
value1,value2
,value3
value4,value5
,value6
"""
        
        expected_markdown = """field |array 
-------------
value1|value2
      |value3
value4|value5
      |value6
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_sub_array_of_objects_case_same_arrays_length(self):
        """Test conversion with arrays of objects."""
        input_json = """[
    {
        "name": "test1",
        "items": [
            {"id": 1, "value": "a"},
            {"id": 2, "value": "b"}
        ]
    },
    {
        "name": "test2", 
        "items": [
            {"id": 3, "value": "c"},
            {"id": 4, "value": "d"}
        ]
    }
]"""
        
        expected_csv = """name,items,
,id,value
test1,1,a
,2,b
test2,3,c
,4,d
"""
        
        expected_markdown = """name |items|     
     |id   |value
-----------------
test1|1    |a    
     |2    |b    
test2|3    |c    
     |4    |d    
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)
        
    def test_json_to_csv_object_with_object(self):
        """Test conversion with nested objects."""
        input_json = """[
    {
        "user": {
            "name": "John",
            "age": 30
        },
        "settings": {
            "theme": "dark",
            "lang": "en"
        }
    }
]"""
        
        expected_csv = """user,,settings,
name,age,theme,lang
John,30,dark,en
"""
        
        expected_markdown = """user|   |settings|    
name|age|theme   |lang
----------------------
John|30 |dark    |en  
"""
        
        self.assert_conversion(input_json, expected_csv, expected_markdown)

if __name__ == '__main__':
    unittest.main()