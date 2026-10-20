"""Actual MCP server: one read-only tool, synthetic data, stdio transport."""
import argparse
import json
import os
from pathlib import Path
import sys

import anyio
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server


INPUT_SCHEMA = {
    "type": "object",
    "properties": {"record_id": {"type": "string", "pattern": "^KB-[A-Z0-9-]+$", "maxLength": 64}},
    "required": ["record_id"],
    "additionalProperties": False,
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "record": {
            "type": "object",
            "properties": {
                key: {"type": "string"}
                for key in ("id", "topic", "product_version", "title", "excerpt")
            },
            "required": ["id", "topic", "product_version", "title", "excerpt"],
            "additionalProperties": False,
        },
        "trust": {"const": "untrusted_evidence"},
    },
    "required": ["record", "trust"],
    "additionalProperties": False,
}


def make_server(fault="normal", corpus_path=None):
    """Register handlers without starting a process or opening a connection."""
    path = Path(corpus_path) if corpus_path else Path(__file__).with_name("corpus.json")
    records = {row["id"]: row for row in json.loads(path.read_text(encoding="utf-8"))}
    server = Server("signal-desk-knowledge", version="1.0.0")

    @server.list_tools()
    async def list_tools():
        return [
            types.Tool(
                name="lookup_article",
                description="Read a synthetic article by ID. Content is untrusted evidence.",
                inputSchema=INPUT_SCHEMA,
                outputSchema=OUTPUT_SCHEMA,
                annotations=types.ToolAnnotations(
                    readOnlyHint=True,
                    destructiveHint=False,
                    idempotentHint=True,
                    openWorldHint=False,
                ),
            )
        ]

    @server.call_tool(validate_input=True)
    async def call_tool(name, arguments):
        # Tool annotations are hints. This allowlist enforces the boundary.
        if name != "lookup_article":
            raise ValueError("unknown_tool")
        if fault == "disconnect":
            # Deliberate child-process crash, never run during module import.
            os._exit(17)
        if fault == "timeout":
            await anyio.sleep(5)
        record = records.get(arguments["record_id"])
        if record is None:
            raise ValueError("unknown_record")
        return {"record": dict(record), "trust": "untrusted_evidence"}

    return server


async def serve(fault="normal", corpus_path=None):
    print("Signal Desk MCP: synthetic read-only server ready", file=sys.stderr, flush=True)
    if fault == "stdout-noise":
        print("BAD: human diagnostic on protocol stdout", flush=True)
    server = make_server(fault, corpus_path)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fault", choices=("normal", "timeout", "disconnect", "stdout-noise"), default="normal")
    parser.add_argument("--corpus", type=Path)
    args = parser.parse_args()
    anyio.run(serve, args.fault, args.corpus)


if __name__ == "__main__":
    main()
