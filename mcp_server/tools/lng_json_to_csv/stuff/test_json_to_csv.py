import unittest
import sys
import os
import json

# Add the parent directory to the path to import the tool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tool import json_to_csv, json_to_markdown

class JsonToCsvTest(unittest.TestCase):
    """Test cases exactly matching the Java JsonToCsvTest.java implementation."""
    
    def assert_r(self, expected: str):
        """Helper method to assert conversion like Java assertR method."""
        input_json = expected.split("\n\n")[0]
        actual_csv = json_to_csv(input_json)
        actual_markdown = json_to_markdown(input_json)
        actual = input_json + "\n\n\n" + actual_csv + "\n\n" + actual_markdown
        
        self.assertEqual(expected, actual, 
                        f"Conversion failed.\nExpected:\n{repr(expected)}\nActual:\n{repr(actual)}")
    
    def test_json_to_csv_simple_one_object_one_field(self):
        """Test conversion of simple JSON object with one field."""
        self.assert_r("""[
    {
        "field": "value1"
    }
]


field
value1


field 
------
value1
""")
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_comma(self):
        """Test conversion with comma escaping."""
        self.assert_r("""[
    {
        "field": "val,ue1"
    }
]


field
"val,ue1"


field  
-------
val,ue1
""")
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_quote(self):
        """Test conversion with quote escaping."""
        self.assert_r("""[
    {
        "field": "val\\"ue1"
    }
]


field
"val""ue1"


field  
-------
val"ue1
""")
    
    def test_json_to_csv_simple_one_object_one_field_case_escape_case_new_line(self):
        """Test conversion with newline escaping."""
        self.assert_r("""[
    {
        "field": "val\\nue1"
    }
]


field
"val
ue1"


field  
-------
val
ue1
""")
    
    def test_json_to_csv_simple_two_objects_one_field(self):
        """Test conversion of two objects with one field."""
        self.assert_r("""[
    {
        "field": "value1"
    },
    {
        "field": "value2"
    }
]


field
value1
value2


field 
------
value1
value2
""")
        
    def test_json_to_csv_simple_one_object_two_fields(self):
        """Test conversion of one object with two fields."""
        self.assert_r("""[
    {
        "field1": "value1",
        "field2": "value2"
    }
]


field1,field2
value1,value2


field1|field2
-------------
value1|value2
""")
        
    def test_json_to_csv_simple_two_objects_two_fields(self):
        """Test conversion of two objects with two fields."""
        self.assert_r("""[
    {
        "field1": "value1",
        "field2": "value2"
    },
    {
        "field1": "value3",
        "field2": "value4"
    }
]


field1,field2
value1,value2
value3,value4


field1|field2
-------------
value1|value2
value3|value4
""")
        
    def test_json_to_csv_simple(self):
        """Test conversion with different fields per object."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1"
    },
    {
        "zField": "test",
        "name": "example"
    }
]


zField,aField,name
value3,value1,
test,,example


zField|aField|name   
---------------------
value3|value1|       
test  |      |example
""")
        
    def test_json_to_csv_sub_array_case_simple(self):
        """Test conversion with simple sub-arrays."""
        self.assert_r("""[
    {
        "field": "value1",
        "array": ["value2", "value3"]
    },
    {
        "field": "value4",
        "array": ["value5", "value6"]
    }
]


field,array
value1,value2
,value3
value4,value5
,value6


field |array 
-------------
value1|value2
      |value3
value4|value5
      |value6
""")
        
    def test_json_to_csv_sub_array(self):
        """Test conversion with number arrays."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,numberArray,name
value3,value1,3,
,,1,
,,2,
test,,10,example
,,2,
,,30,


zField|aField|numberArray|name   
---------------------------------
value3|value1|3          |       
      |      |1          |       
      |      |2          |       
test  |      |10         |example
      |      |2          |       
      |      |30         |       
""")
        
    def test_json_to_csv_sub_array_not_same_length(self):
        """Test conversion with arrays of different lengths."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    },
    {
        "id": "12345",
        "aField": "value6",
        "numberArray": [1, 10, 100, 1000]
    }
]


zField,aField,numberArray,name,id
value3,value1,3,,
,,1,,
,,2,,
test,,10,example,
,,2,,
,,30,,
,value6,1,,12345
,,10,,
,,100,,
,,1000,,


zField|aField|numberArray|name   |id   
---------------------------------------
value3|value1|3          |       |     
      |      |1          |       |     
      |      |2          |       |     
test  |      |10         |example|     
      |      |2          |       |     
      |      |30         |       |     
      |value6|1          |       |12345
      |      |10         |       |     
      |      |100        |       |     
      |      |1000       |       |     
""")
        
    def test_json_to_csv_two_different_arrays(self):
        """Test conversion with two different arrays."""
        self.assert_r("""[
    {
        "filed": "name",
        "array1": [1, 2, 3],
        "array2": [4, 5, 6]
    }
]


filed,array1,array2
name,1,4
,2,5
,3,6


filed|array1|array2
-------------------
name |1     |4     
     |2     |5     
     |3     |6     
""")

    def test_json_to_csv_sub_array_of_objects_case_same_arrays_length(self):
        """Test conversion with arrays of objects with same lengths."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "arrayField": [
            {"name": "banana", "color": "yellow"},
            {"name": "apple", "color": "red"},
            {"name": "cherry", "color": "red"}
        ],
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,arrayField,,numberArray,name
,,name,color,,
value3,value1,banana,yellow,3,
,,apple,red,1,
,,cherry,red,2,
test,,,,10,example
,,,,2,
,,,,30,


zField|aField|arrayField|      |numberArray|name   
---------------------------------------------------
      |      |name      |color |           |       
value3|value1|banana    |yellow|3          |       
      |      |apple     |red   |1          |       
      |      |cherry    |red   |2          |       
test  |      |          |      |10         |example
      |      |          |      |2          |       
      |      |          |      |30         |       
""")

    def test_json_to_csv_sub_array_of_objects_case_one_is_less(self):
        """Test conversion with arrays of objects where one is shorter."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "arrayField": [
            {"name": "banana", "color": "yellow"},
            {"name": "apple", "color": "red"}
        ],
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,arrayField,,numberArray,name
,,name,color,,
value3,value1,banana,yellow,3,
,,apple,red,1,
,,,,2,
test,,,,10,example
,,,,2,
,,,,30,


zField|aField|arrayField|      |numberArray|name   
---------------------------------------------------
      |      |name      |color |           |       
value3|value1|banana    |yellow|3          |       
      |      |apple     |red   |1          |       
      |      |          |      |2          |       
test  |      |          |      |10         |example
      |      |          |      |2          |       
      |      |          |      |30         |       
""")

    def test_json_to_csv_sub_array_of_objects_case_another_is_less(self):
        """Test conversion with arrays where another one is shorter."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "arrayField": [
            {"name": "banana", "color": "yellow"},
            {"name": "apple", "color": "red"},
            {"name": "cherry", "color": "red"}
        ],
        "numberArray": [3, 1]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,arrayField,,numberArray,name
,,name,color,,
value3,value1,banana,yellow,3,
,,apple,red,1,
,,cherry,red,,
test,,,,10,example
,,,,2,
,,,,30,


zField|aField|arrayField|      |numberArray|name   
---------------------------------------------------
      |      |name      |color |           |       
value3|value1|banana    |yellow|3          |       
      |      |apple     |red   |1          |       
      |      |cherry    |red   |           |       
test  |      |          |      |10         |example
      |      |          |      |2          |       
      |      |          |      |30         |       
""")

    def test_json_to_csv_sub_array_of_objects_that_contains_of_objects(self):
        """Test conversion with nested objects within array objects."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "arrayField": [
            {"name": "banana", "color":
                {"id": "y", "value": "yellow"}
            },
            {"name": "apple", "color":
                {"id": "r", "value": "red"}
            },
            {"name": "cherry", "color":
                {"id": "r", "value": "red"}
            }
        ],
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,arrayField,,,numberArray,name
,,name,color,,,
,,,id,value,,
value3,value1,banana,y,yellow,3,
,,apple,r,red,1,
,,cherry,r,red,2,
test,,,,,10,example
,,,,,2,
,,,,,30,


zField|aField|arrayField|     |      |numberArray|name   
---------------------------------------------------------
      |      |name      |color|      |           |       
      |      |          |id   |value |           |       
value3|value1|banana    |y    |yellow|3          |       
      |      |apple     |r    |red   |1          |       
      |      |cherry    |r    |red   |2          |       
test  |      |          |     |      |10         |example
      |      |          |     |      |2          |       
      |      |          |     |      |30         |       
""")

    def test_json_to_csv_sub_array_of_objects_that_contains_of_array_of_objects(self):
        """Test conversion with arrays of objects containing arrays of objects."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "arrayField": [
            {"name": "banana", "colors": [
                {"id": "y", "value": "yellow"},
                {"id": "g", "value": "green"}
            ]},
            {"name": "apple", "colors": [
                {"id": "m", "value": "magenta"}
            ]},
            {"name": "cherry", "colors": [
                {"id": "bl", "value": "black"},
                {"id": "w", "value": "white"},
                {"id": "br", "value": "brown"}
            ]}
        ],
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,arrayField,,,numberArray,name
,,name,colors,,,
,,,id,value,,
value3,value1,banana,y,yellow,3,
,,,g,green,1,
,,apple,m,magenta,2,
,,cherry,bl,black,,
,,,w,white,,
,,,br,brown,,
test,,,,,10,example
,,,,,2,
,,,,,30,


zField|aField|arrayField|      |       |numberArray|name   
-----------------------------------------------------------
      |      |name      |colors|       |           |       
      |      |          |id    |value  |           |       
value3|value1|banana    |y     |yellow |3          |       
      |      |          |g     |green  |1          |       
      |      |apple     |m     |magenta|2          |       
      |      |cherry    |bl    |black  |           |       
      |      |          |w     |white  |           |       
      |      |          |br    |brown  |           |       
test  |      |          |      |       |10         |example
      |      |          |      |       |2          |       
      |      |          |      |       |30         |       
""")

    def test_json_to_csv_object_with_object(self):
        """Test conversion with nested objects (not arrays)."""
        self.assert_r("""[
    {
        "zField": "value3",
        "aField": "value1",
        "objectField": {
            "name": "banana",             "color": "yellow"
        },
        "numberArray": [3, 1, 2]
    },
    {
        "zField": "test",
        "name": "example",
        "numberArray": [10, 2, 30]
    }
]


zField,aField,objectField,,numberArray,name
,,name,color,,
value3,value1,banana,yellow,3,
,,,,1,
,,,,2,
test,,,,10,example
,,,,2,
,,,,30,


zField|aField|objectField|      |numberArray|name   
----------------------------------------------------
      |      |name       |color |           |       
value3|value1|banana     |yellow|3          |       
      |      |           |      |1          |       
      |      |           |      |2          |       
test  |      |           |      |10         |example
      |      |           |      |2          |       
      |      |           |      |30         |       
""")

    def test_json_to_csv_partially_from_different_lines(self):
        """Test complex partially mixed structure."""
        self.assert_r("""[
  {
    "date": "2025-03-17",
    "one": {
      "data1": 0
    },
    "data2": 1,
    "two": {
      "data3": 0
    },
    "data4": 1,
    "three": {
      "data5": 0
    }
  },
  {
    "date": "2025-03-18",
    "one": {
      "data6": [
        {
          "name": "JetBrains"
        },
        {
          "name": "vscode"
        }
      ]
    },
    "data2": 5,
    "two": {
      "data3": 0
    },
    "data4": 3,
    "three": {
      "data5": 0
    }
  }
]


date,one,,data2,two,data4,three
,data1,data6,,data3,,data5
,,name,,,,
2025-03-17,0,,1,0,1,0
2025-03-18,,JetBrains,5,0,3,0
,,vscode,,,,


date      |one  |         |data2|two  |data4|three
--------------------------------------------------
          |data1|data6    |     |data3|     |data5
          |     |name     |     |     |     |     
2025-03-17|0    |         |1    |0    |1    |0    
2025-03-18|     |JetBrains|5    |0    |3    |0    
          |     |vscode   |     |     |     |     
""")

    def test_json_to_csv_complex(self):
        """Test conversion with complex nested structure."""
        self.assert_r("""[
  {
    "date": "2025-03-17",
    "copilot_ide_chat": {
      "total_engaged_users": 0
    },
    "total_active_users": 1,
    "copilot_dotcom_chat": {
      "total_engaged_users": 0
    },
    "total_engaged_users": 1,
    "copilot_dotcom_pull_requests": {
      "total_engaged_users": 0
    },
    "copilot_ide_code_completions": {
      "editors": [
        {
          "name": "JetBrains",
          "models": [
            {
              "name": "default",
              "languages": [
                {
                  "name": "json",
                  "total_engaged_users": 1,
                  "total_code_acceptances": 1,
                  "total_code_suggestions": 1,
                  "total_code_lines_accepted": 1,
                  "total_code_lines_suggested": 1
                }
              ],
              "is_custom_model": false,
              "total_engaged_users": 1
            }
          ],
          "total_engaged_users": 1
        }
      ],
      "languages": [
        {
          "name": "json",
          "total_engaged_users": 1
        }
      ],
      "total_engaged_users": 1
    }
  },
  {
    "date": "2025-03-18",
    "copilot_ide_chat": {
      "editors": [
        {
          "name": "JetBrains",
          "models": [
            {
              "name": "default",
              "total_chats": 4,
              "is_custom_model": false,
              "total_engaged_users": 1,
              "total_chat_copy_events": 1,
              "total_chat_insertion_events": 0
            }
          ],
          "total_engaged_users": 1
        },
        {
          "name": "vscode",
          "models": [
            {
              "name": "default",
              "total_chats": 4,
              "is_custom_model": false,
              "total_engaged_users": 1,
              "total_chat_copy_events": 0,
              "total_chat_insertion_events": 0
            }
          ],
          "total_engaged_users": 1
        }
      ],
      "total_engaged_users": 2
    },
    "total_active_users": 5,
    "copilot_dotcom_chat": {
      "total_engaged_users": 0
    },
    "total_engaged_users": 3,
    "copilot_dotcom_pull_requests": {
      "total_engaged_users": 0
    },
    "copilot_ide_code_completions": {
      "editors": [
        {
          "name": "JetBrains",
          "models": [
            {
              "name": "default",
              "languages": [
                {
                  "name": "java",
                  "total_engaged_users": 2,
                  "total_code_acceptances": 12,
                  "total_code_suggestions": 67,
                  "total_code_lines_accepted": 18,
                  "total_code_lines_suggested": 214
                },
                {
                  "name": "unknown",
                  "total_engaged_users": 0,
                  "total_code_acceptances": 0,
                  "total_code_suggestions": 11,
                  "total_code_lines_accepted": 0,
                  "total_code_lines_suggested": 21
                },
                {
                  "name": "json",
                  "total_engaged_users": 0,
                  "total_code_acceptances": 0,
                  "total_code_suggestions": 1,
                  "total_code_lines_accepted": 0,
                  "total_code_lines_suggested": 13
                }
              ],
              "is_custom_model": false,
              "total_engaged_users": 2
            }
          ],
          "total_engaged_users": 2
        }
      ],
      "languages": [
        {
          "name": "java",
          "total_engaged_users": 2
        },
        {
          "name": "unknown",
          "total_engaged_users": 0
        },
        {
          "name": "json",
          "total_engaged_users": 0
        }
      ],
      "total_engaged_users": 2
    }
  }
]


date,copilot_ide_chat,,,,,,,,,total_active_users,copilot_dotcom_chat,total_engaged_users,copilot_dotcom_pull_requests,copilot_ide_code_completions,,,,,,,,,,,,,
,total_engaged_users,editors,,,,,,,,,total_engaged_users,,total_engaged_users,editors,,,,,,,,,,,languages,,total_engaged_users
,,name,models,,,,,,total_engaged_users,,,,,name,models,,,,,,,,,total_engaged_users,name,total_engaged_users,
,,,name,total_chats,is_custom_model,total_engaged_users,total_chat_copy_events,total_chat_insertion_events,,,,,,,name,languages,,,,,,is_custom_model,total_engaged_users,,,,
,,,,,,,,,,,,,,,,name,total_engaged_users,total_code_acceptances,total_code_suggestions,total_code_lines_accepted,total_code_lines_suggested,,,,,,
2025-03-17,0,,,,,,,,,1,0,1,0,JetBrains,default,json,1,1,1,1,1,false,1,1,json,1,1
2025-03-18,2,JetBrains,default,4,false,1,1,0,1,5,0,3,0,JetBrains,default,java,2,12,67,18,214,false,2,2,java,2,2
,,vscode,default,4,false,1,0,0,1,,,,,,,unknown,0,0,11,0,21,,,,unknown,0,
,,,,,,,,,,,,,,,,json,0,0,1,0,13,,,,json,0,


date      |copilot_ide_chat   |         |       |           |               |                   |                      |                           |                   |total_active_users|copilot_dotcom_chat|total_engaged_users|copilot_dotcom_pull_requests|copilot_ide_code_completions|       |         |                   |                      |                      |                         |                          |               |                   |                   |         |                   |                   
          |total_engaged_users|editors  |       |           |               |                   |                      |                           |                   |                  |total_engaged_users|                   |total_engaged_users         |editors                     |       |         |                   |                      |                      |                         |                          |               |                   |                   |languages|                   |total_engaged_users
          |                   |name     |models |           |               |                   |                      |                           |total_engaged_users|                  |                   |                   |                            |name                        |models |         |                   |                      |                      |                         |                          |               |                   |total_engaged_users|name     |total_engaged_users|                   
          |                   |         |name   |total_chats|is_custom_model|total_engaged_users|total_chat_copy_events|total_chat_insertion_events|                   |                  |                   |                   |                            |                            |name   |languages|                   |                      |                      |                         |                          |is_custom_model|total_engaged_users|                   |         |                   |                   
          |                   |         |       |           |               |                   |                      |                           |                   |                  |                   |                   |                            |                            |       |name     |total_engaged_users|total_code_acceptances|total_code_suggestions|total_code_lines_accepted|total_code_lines_suggested|               |                   |                   |         |                   |                   
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2025-03-17|0                  |         |       |           |               |                   |                      |                           |                   |1                 |0                  |1                  |0                           |JetBrains                   |default|json     |1                  |1                     |1                     |1                        |1                         |false          |1                  |1                  |json     |1                  |1                  
2025-03-18|2                  |JetBrains|default|4          |false          |1                  |1                     |0                          |1                  |5                 |0                  |3                  |0                           |JetBrains                   |default|java     |2                  |12                    |67                    |18                       |214                       |false          |2                  |2                  |java     |2                  |2                  
          |                   |vscode   |default|4          |false          |1                  |0                     |0                          |1                  |                  |                   |                   |                            |                            |       |unknown  |0                  |0                     |11                    |0                        |21                        |               |                   |                   |unknown  |0                  |                   
          |                   |         |       |           |               |                   |                      |                           |                   |                  |                   |                   |                            |                            |       |json     |0                  |0                     |1                     |0                        |13                        |               |                   |                   |json     |0                  |                   
""")

    def test_json_to_csv_corner_case(self):
        """Test complex nested corner case."""
        self.assert_r("""[
  {
    "date": "2025-03-17",
    "object": {
      "field1": [
        {
          "name": "field1_name",
          "array1": [
            {
              "name": "array1_name",
              "array2": [
                {
                  "name": "array2_name",
                  "data3": 3
                }
              ],
              "data4": 4
            }
          ],
          "data5": 5
        }
      ],
      "field2": [
        {
          "name": "field2_name",
          "data6": 6
        }
      ],
      "data7": 7
    }
  }
]


date,object,,,,,,,,
,field1,,,,,,field2,,data7
,name,array1,,,,data5,name,data6,
,,name,array2,,data4,,,,
,,,name,data3,,,,,
2025-03-17,field1_name,array1_name,array2_name,3,4,5,field2_name,6,7


date      |object     |           |           |     |     |     |           |     |     
          |field1     |           |           |     |     |     |field2     |     |data7
          |name       |array1     |           |     |     |data5|name       |data6|     
          |           |name       |array2     |     |data4|     |           |     |     
          |           |           |name       |data3|     |     |           |     |     
----------------------------------------------------------------------------------------
2025-03-17|field1_name|array1_name|array2_name|3    |4    |5    |field2_name|6    |7    
""")

    def test_json_to_csv_super_complex(self):
        """Test super complex conversion with large dataset (minified JSON)."""
        json_data = '[{"date":"2025-03-17","copilot_ide_chat":{"total_engaged_users":0},"total_active_users":1,"copilot_dotcom_chat":{"total_engaged_users":0},"total_engaged_users":1,"copilot_dotcom_pull_requests":{"total_engaged_users":0},"copilot_ide_code_completions":{"editors":[{"name":"JetBrains","models":[{"name":"default","languages":[{"name":"json","total_engaged_users":1,"total_code_acceptances":1,"total_code_suggestions":1,"total_code_lines_accepted":1,"total_code_lines_suggested":1}],"is_custom_model":false,"total_engaged_users":1}],"total_engaged_users":1}],"languages":[{"name":"json","total_engaged_users":1}],"total_engaged_users":1}},{"date":"2025-03-18","copilot_ide_chat":{"editors":[{"name":"JetBrains","models":[{"name":"default","total_chats":4,"is_custom_model":false,"total_engaged_users":1,"total_chat_copy_events":1,"total_chat_insertion_events":0}],"total_engaged_users":1},{"name":"vscode","models":[{"name":"default","total_chats":4,"is_custom_model":false,"total_engaged_users":1,"total_chat_copy_events":0,"total_chat_insertion_events":0}],"total_engaged_users":1}],"total_engaged_users":2},"total_active_users":5,"copilot_dotcom_chat":{"total_engaged_users":0},"total_engaged_users":3,"copilot_dotcom_pull_requests":{"total_engaged_users":0},"copilot_ide_code_completions":{"editors":[{"name":"JetBrains","models":[{"name":"default","languages":[{"name":"java","total_engaged_users":2,"total_code_acceptances":12,"total_code_suggestions":67,"total_code_lines_accepted":18,"total_code_lines_suggested":214},{"name":"unknown","total_engaged_users":0,"total_code_acceptances":0,"total_code_suggestions":11,"total_code_lines_accepted":0,"total_code_lines_suggested":21},{"name":"json","total_engaged_users":0,"total_code_acceptances":0,"total_code_suggestions":1,"total_code_lines_accepted":0,"total_code_lines_suggested":13}],"is_custom_model":false,"total_engaged_users":2}],"total_engaged_users":2}],"languages":[{"name":"java","total_engaged_users":2},{"name":"unknown","total_engaged_users":0},{"name":"json","total_engaged_users":0}],"total_engaged_users":2}}]'
        expected_csv = "date,copilot_ide_chat,,,,,,,,,total_active_users,copilot_dotcom_chat,total_engaged_users,copilot_dotcom_pull_requests,copilot_ide_code_completions,,,,,,,,,,,,,\n,total_engaged_users,editors,,,,,,,,,total_engaged_users,,total_engaged_users,editors,,,,,,,,,,,languages,,total_engaged_users\n,,name,models,,,,,,total_engaged_users,,,,,name,models,,,,,,,,,total_engaged_users,name,total_engaged_users,\n,,,name,total_chats,is_custom_model,total_engaged_users,total_chat_copy_events,total_chat_insertion_events,,,,,,,name,languages,,,,,,is_custom_model,total_engaged_users,,,,\n,,,,,,,,,,,,,,,,name,total_engaged_users,total_code_acceptances,total_code_suggestions,total_code_lines_accepted,total_code_lines_suggested,,,,,,\n2025-03-17,0,,,,,,,,,1,0,1,0,JetBrains,default,json,1,1,1,1,1,false,1,1,json,1,1\n2025-03-18,2,JetBrains,default,4,false,1,1,0,1,5,0,3,0,JetBrains,default,java,2,12,67,18,214,false,2,2,java,2,2\n,,vscode,default,4,false,1,0,0,1,,,,,,,unknown,0,0,11,0,21,,,,unknown,0,\n,,,,,,,,,,,,,,,,json,0,0,1,0,13,,,,json,0,"
        expected_markdown = "date      |copilot_ide_chat   |         |       |           |               |                   |                      |                           |                   |total_active_users|copilot_dotcom_chat|total_engaged_users|copilot_dotcom_pull_requests|copilot_ide_code_completions|       |               |                   |                      |                      |                         |                          |               |                   |                   |               |                   |                   \n          |total_engaged_users|editors  |       |           |               |                   |                      |                           |                   |                  |total_engaged_users|                   |total_engaged_users         |editors                     |       |               |                   |                      |                      |                         |                          |               |                   |                   |languages      |                   |total_engaged_users\n          |                   |name     |models |           |               |                   |                      |                           |total_engaged_users|                  |                   |                   |                            |name                        |models |               |                   |                      |                      |                         |                          |               |                   |total_engaged_users|name           |total_engaged_users|                   \n          |                   |         |name   |total_chats|is_custom_model|total_engaged_users|total_chat_copy_events|total_chat_insertion_events|                   |                  |                   |                   |                            |                            |name   |languages      |                   |                      |                      |                         |                          |is_custom_model|total_engaged_users|                   |               |                   |                   \n          |                   |         |       |           |               |                   |                      |                           |                   |                  |                   |                   |                            |                            |       |name           |total_engaged_users|total_code_acceptances|total_code_suggestions|total_code_lines_accepted|total_code_lines_suggested|               |                   |                   |               |                   |                   \n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n2025-03-17|0                  |         |       |           |               |                   |                      |                           |                   |1                 |0                  |1                  |0                           |JetBrains                   |default|json           |1                  |1                     |1                     |1                        |1                         |false          |1                  |1                  |json           |1                  |1                  \n2025-03-18|2                  |JetBrains|default|4          |false          |1                  |1                     |0                          |1                  |5                 |0                  |3                  |0                           |JetBrains                   |default|java           |2                  |12                    |67                    |18                       |214                       |false          |2                  |2                  |java           |2                  |2                  \n          |                   |vscode   |default|4          |false          |1                  |0                     |0                          |1                  |                  |                   |                   |                            |                            |       |unknown        |0                  |0                     |11                    |0                        |21                        |               |                   |                   |unknown        |0                  |                   \n          |                   |         |       |           |               |                   |                      |                           |                   |                  |                   |                   |                            |                            |       |json           |0                  |0                     |1                     |0                        |13                        |               |                   |                   |json           |0                  |                   "
        expected = json_data + "\n\n\n" + expected_csv + "\n\n" + expected_markdown
        self.assert_r(expected)

    def test_json_to_csv_super_complex2(self):
        """Test another super complex conversion with reformatted JSON."""
        self.assert_r("""[
  {
    "date" : "2025-03-17",
    "total_active_users" : 1,
    "total_engaged_users" : 1,
    "copilot_ide_chat" : {
      "total_engaged_users" : 0
    },
    "copilot_dotcom_chat" : {
      "total_engaged_users" : 0
    },
    "copilot_dotcom_pull_requests" : {
      "total_engaged_users" : 0
    },
    "copilot_ide_code_completions" : {
      "editors" : [
        {
          "models" : [
            {
              "is_custom_model" : false,
              "languages" : [
                {
                  "name" : "json",
                  "total_code_acceptances" : 1,
                  "total_code_lines_accepted" : 1,
                  "total_code_lines_suggested" : 1,
                  "total_code_suggestions" : 1,
                  "total_engaged_users" : 1
                }
              ],
              "name" : "default",
              "total_engaged_users" : 1
            }
          ],
          "name" : "JetBrains",
          "total_engaged_users" : 1
        }
      ],
      "languages" : [
        {
          "name" : "json",
          "total_engaged_users" : 1
        }
      ],
      "total_engaged_users" : 1
    }
  },
  {
    "date" : "2025-03-18",
    "total_active_users" : 5,
    "total_engaged_users" : 3,
    "copilot_ide_chat" : {
      "editors" : [
        {
          "models" : [
            {
              "is_custom_model" : false,
              "name" : "default",
              "total_chat_copy_events" : 1,
              "total_chat_insertion_events" : 0,
              "total_chats" : 4,
              "total_engaged_users" : 1
            }
          ],
          "name" : "JetBrains",
          "total_engaged_users" : 1
        },
        {
          "models" : [
            {
              "is_custom_model" : false,
              "name" : "default",
              "total_chat_copy_events" : 0,
              "total_chat_insertion_events" : 0,
              "total_chats" : 4,
              "total_engaged_users" : 1
            }
          ],
          "name" : "vscode",
          "total_engaged_users" : 1
        }
      ],
      "total_engaged_users" : 2
    },
    "copilot_dotcom_chat" : {
      "total_engaged_users" : 0
    },
    "copilot_dotcom_pull_requests" : {
      "total_engaged_users" : 0
    },
    "copilot_ide_code_completions" : {
      "editors" : [
        {
          "models" : [
            {
              "is_custom_model" : false,
              "languages" : [
                {
                  "name" : "java",
                  "total_code_acceptances" : 12,
                  "total_code_lines_accepted" : 18,
                  "total_code_lines_suggested" : 214,
                  "total_code_suggestions" : 67,
                  "total_engaged_users" : 2
                },
                {
                  "name" : "json",
                  "total_code_acceptances" : 0,
                  "total_code_lines_accepted" : 0,
                  "total_code_lines_suggested" : 13,
                  "total_code_suggestions" : 1,
                  "total_engaged_users" : 0
                },
                {
                  "name" : "unknown",
                  "total_code_acceptances" : 0,
                  "total_code_lines_accepted" : 0,
                  "total_code_lines_suggested" : 21,
                  "total_code_suggestions" : 11,
                  "total_engaged_users" : 0
                }
              ],
              "name" : "default",
              "total_engaged_users" : 2
            }
          ],
          "name" : "JetBrains",
          "total_engaged_users" : 2
        }
      ],
      "languages" : [
        {
          "name" : "java",
          "total_engaged_users" : 2
        },
        {
          "name" : "json",
          "total_engaged_users" : 0
        },
        {
          "name" : "unknown",
          "total_engaged_users" : 0
        }
      ],
      "total_engaged_users" : 2
    }
  }
]


date,total_active_users,total_engaged_users,copilot_ide_chat,,,,,,,,,copilot_dotcom_chat,copilot_dotcom_pull_requests,copilot_ide_code_completions,,,,,,,,,,,,,
,,,total_engaged_users,editors,,,,,,,,total_engaged_users,total_engaged_users,editors,,,,,,,,,,,languages,,total_engaged_users
,,,,models,,,,,,name,total_engaged_users,,,models,,,,,,,,,name,total_engaged_users,name,total_engaged_users,
,,,,is_custom_model,name,total_chat_copy_events,total_chat_insertion_events,total_chats,total_engaged_users,,,,,is_custom_model,languages,,,,,,name,total_engaged_users,,,,,
,,,,,,,,,,,,,,,name,total_code_acceptances,total_code_lines_accepted,total_code_lines_suggested,total_code_suggestions,total_engaged_users,,,,,,,
2025-03-17,1,1,0,,,,,,,,,0,0,false,json,1,1,1,1,1,default,1,JetBrains,1,json,1,1
2025-03-18,5,3,2,false,default,0,0,4,1,vscode,1,0,0,false,java,12,18,214,67,2,default,2,JetBrains,2,java,2,2
,,,,,,,,,,,,,,,json,0,0,13,1,0,,,,,json,0,
,,,,,,,,,,,,,,,unknown,0,0,21,11,0,,,,,unknown,0,


date      |total_active_users|total_engaged_users|copilot_ide_chat   |               |       |                      |                           |           |                   |      |                   |copilot_dotcom_chat|copilot_dotcom_pull_requests|copilot_ide_code_completions|         |                      |                         |                          |                      |                   |       |                   |         |                   |         |                   |                   
          |                  |                   |total_engaged_users|editors        |       |                      |                           |           |                   |      |                   |total_engaged_users|total_engaged_users         |editors                     |         |                      |                         |                          |                      |                   |       |                   |         |                   |languages|                   |total_engaged_users
          |                  |                   |                   |models         |       |                      |                           |           |                   |name  |total_engaged_users|                   |                            |models                      |         |                      |                         |                          |                      |                   |       |                   |name     |total_engaged_users|name     |total_engaged_users|                   
          |                  |                   |                   |is_custom_model|name   |total_chat_copy_events|total_chat_insertion_events|total_chats|total_engaged_users|      |                   |                   |                            |is_custom_model             |languages|                      |                         |                          |                      |                   |name   |total_engaged_users|         |                   |         |                   |                   
          |                  |                   |                   |               |       |                      |                           |           |                   |      |                   |                   |                            |                            |name     |total_code_acceptances|total_code_lines_accepted|total_code_lines_suggested|total_code_suggestions|total_engaged_users|       |                   |         |                   |         |                   |                   
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2025-03-17|1                 |1                  |0                  |               |       |                      |                           |           |                   |      |                   |0                  |0                           |false                       |json     |1                     |1                        |1                         |1                     |1                  |default|1                  |JetBrains|1                  |json     |1                  |1                  
2025-03-18|5                 |3                  |2                  |false          |default|0                     |0                          |4          |1                  |vscode|1                  |0                  |0                           |false                       |java     |12                    |18                       |214                       |67                    |2                  |default|2                  |JetBrains|2                  |java     |2                  |2                  
          |                  |                   |                   |               |       |                      |                           |           |                   |      |                   |                   |                            |                            |json     |0                     |0                        |13                        |1                     |0                  |       |                   |         |                   |json     |0                  |                   
          |                  |                   |                   |               |       |                      |                           |           |                   |      |                   |                   |                            |                            |unknown  |0                     |0                        |21                        |11                    |0                  |       |                   |         |                   |unknown  |0                  |                   
""")

    def performance(self):
        """Performance test calling test_json_to_csv_super_complex2 multiple times."""
        import time
        start = time.time()
        for i in range(100):  # Reduced iterations for faster testing
            self.test_json_to_csv_super_complex2()
        end = time.time()
        print(f"Performance test took: {(end - start) * 1000:.0f} ms")

if __name__ == '__main__':
    unittest.main()