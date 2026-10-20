# MCP lab solution guidance

Try the extension before reading this page. Do not replace the reference server. Work in the copied server and preserve evidence from the failing baseline.

The `list_tools()` handler returns a list. Append another `types.Tool` to that list:

```python
types.Tool(
    name="list_topics",
    description="List unique topics in the synthetic corpus.",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    outputSchema={
        "type": "object",
        "properties": {
            "topics": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True,
            }
        },
        "required": ["topics"],
        "additionalProperties": False,
    },
    annotations=types.ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
```

In `call_tool()`, before the existing unknown-tool guard, add:

```python
if name == "list_topics":
    return {"topics": sorted({record["topic"] for record in records.values()})}
```

The official server decorator validates the declared argument schema before entering this handler. The official client validates successful structured content against the advertised output schema. The handler still has to refuse tool names outside its explicit branches.

Run the extended gate and preserve its report. Then replace the implementation temporarily with a hardcoded list and add a new corpus topic: observe why the existing gate alone cannot distinguish a derived list from a memorized answer. Add an assertion covering the new topic, restore the derived implementation, and document the limitation of a fixed fixture. Your extra check is part of the submitted evidence, beyond the bundled 16 assertions.

An empty output list can be a valid answer for an empty corpus. A malformed input object is an error. Do not conflate these cases by returning an empty list for all failures.
