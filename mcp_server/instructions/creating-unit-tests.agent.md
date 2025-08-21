- Please store all unit tests in the `stuff` folder inside the folder with `tool.py` with name `test.py`.
- When creating tests, use the `approvals testing` approach `https://approvaltests.com/`. 
  + Unit testing asserts can be difficult to use. Approval tests simplify this by taking a snapshot of the results, and confirming that they have not changed. 
  + In normal unit testing, you say assertEquals(5, person.getAge()). Approvals allow you to do this when the thing that you want to assert is no longer a primitive but a complex object. For example, you can say, Approvals.verify(person).
- Each test must contain at least one assert block that tests some part of the component under test in a text representation. 
  + This content can be prepared by a function in the test framework. 
  + Thanks to this approach, we will see a well-readable test—the “test as documentation” principle.
- Tests should contain `// given`, ``// when`, and `// then` blocks to make it clear what the test does.
- Tests names should use `should_<what-to-expect>_when_<context>`. You can add `_and|case_<some_additional>` to the test name.
- Use the xUnit framework.
- An example of such a test in Java (all logic is hidden in the `given`, `createQuestionChain`, `logger.assertLog` methods so you can see the test the main idea of what we are testing):
```java
@Test
public void shouldBuildTable_whenTwoLists_caseReplaceQuotes() {
    // given
    given("""
            [TRANSFORMER]
            name: CSV_TABLE
            type: CSV_FORMAT_TRANSFORMER
            input_keys: list1,list2
            output_key: csv_result
            template: |-
              Column1,Column2
            """);

    ChainContext context = new ChainContext() {{
        documents.put("list1", List.of("\"1\"a\"", "\"2\"a\"", "\"3\"a\"", "\"4\"a\""));
        documents.put("list2", List.of("\"1\"b\"", "\"2\"b\"", "\"3\"b\"", "\"4\"b\""));
    }};

    createQuestionChain(context);

    // when
    transformer.transform(context);

    // then
    logger.assertLog("""
            CSV_TABLE: Transformer [CSV_FORMAT_TRANSFORMER] is processing.
            CSV_TABLE: Count(null) is not integer. Got defaults(1)
            CSV_TABLE: How many times to recursively replace place-holders in prompt before getting result: 1
            CSV_TABLE: Trying to build SCV table with:
            header: Column1,Column2
            row: ["1"a", "2"a", "3"a", "4"a"]
            row: ["1"b", "2"b", "3"b", "4"b"]
            CSV_TABLE: CSV table:
            "Column1","Column2"
            "`1`a`","`1`b`"
            "`2`a`","`2`b`"
            "`3`a`","`3`b`"
            "`4`a`","`4`b`"
            
            CSV_TABLE: Transformer processed.
            """);

    assertEquals("""
                    "Column1","Column2"
                    "`1`a`","`1`b`"
                    "`2`a`","`2`b`"
                    "`3`a`","`3`b`"
                    "`4`a`","`4`b`"
                    """,
            context.getValue("csv_result"));
}
```
- Run all tests to make sure everything works correctly: 
  + `python -m pytest mcp_server/tools/{TOOL_NAME}/ --tb=no -q`
  + `python -m unittest mcp_server.tools.{TOOL_NAME}.stuff.test -v`
  + `python mcp_server/tools/{TOOL_NAME}/stuff/test.py`
  + `python -m unittest mcp_server.tools.{TOOL_NAME}.stuff.test.{TestClass}.{test_method} -v` (single test)