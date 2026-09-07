#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp==1.29.1"]
# ///
"""Probe or call Blender Lab MCP through a Codex stdio server definition."""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import sys
import tomllib
from datetime import timedelta
from importlib.metadata import version
from pathlib import Path


def positive_seconds(value: str) -> float:
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("timeout must be finite and positive")
    return seconds


def default_config() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "config.toml"


def load_server(path: Path, name: str) -> dict:
    with path.open("rb") as source:
        config = tomllib.load(source)
    server = config.get("mcp_servers", {}).get(name)
    if not isinstance(server, dict):
        raise ValueError(f"No MCP server definition named {name!r}")
    if server.get("enabled") is False:
        raise ValueError("The selected server is disabled")
    if (
        "url" in server
        or not isinstance(server.get("command"), str)
        or not server["command"]
    ):
        raise ValueError("Select a stdio server with a non-empty command")
    arguments = server.get("args", [])
    environment = server.get("env", {})
    if not isinstance(arguments, list) or not all(
        isinstance(v, str) for v in arguments
    ):
        raise ValueError("Server args must be a list of strings")
    if not isinstance(environment, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in environment.items()
    ):
        raise ValueError("Server env must map strings to strings")
    cwd = server.get("cwd")
    if cwd is not None and (not isinstance(cwd, str) or not Path(cwd).is_absolute()):
        raise ValueError("Server cwd, when set, must be an absolute path")
    return {
        "command": server["command"],
        "args": arguments,
        "env": {**os.environ, **environment},
        "cwd": cwd,
    }


def build_code(code_file: Path, params_file: Path | None) -> str:
    parameters = json.loads(params_file.read_text()) if params_file else {}
    if not isinstance(parameters, dict):
        raise ValueError("The parameters file must contain a JSON object")
    encoded = json.dumps(parameters, allow_nan=False)
    # repr quotes JSON as Python data; neither parameters nor paths enter a shell.
    # Compile separately so the code file can keep its own future imports.
    return (
        "import json as _gda_json\nparams = _gda_json.loads("
        + repr(encoded)
        + ")\n"
        + "exec(compile("
        + repr(code_file.read_text())
        + ", "
        + repr(str(code_file.resolve()))
        + ", 'exec'), globals())\n"
    )


def decode_result(raw: dict, mode: str) -> dict:
    if raw.get("isError"):
        raise ValueError("MCP tool reported an error; see raw_result in the receipt")
    payload = raw.get("structuredContent")
    if payload is None:
        blocks = raw.get("content", [])
        if len(blocks) != 1 or blocks[0].get("type") != "text":
            raise ValueError("Expected one JSON text block or structuredContent")
        payload = json.loads(blocks[0]["text"])
    if not isinstance(payload, dict):
        raise ValueError("Expected a dictionary tool result")
    if mode == "interactive":
        if payload.get("status") != "ok":
            raise ValueError(
                str(payload.get("message", "Unrecognized interactive result status"))
            )
        if not isinstance(payload.get("result"), dict):
            raise ValueError("Interactive result has no dictionary result field")
        return payload["result"]
    if mode != "cli":
        raise ValueError("Unknown execution mode")
    # CLI returns the user's dictionary. Its keys have no generic success meaning.
    return payload


async def discover(session) -> list:
    found = []
    cursor = None
    seen = set()
    while True:
        page = await session.list_tools(cursor=cursor)
        found.extend(page.tools)
        cursor = page.nextCursor
        if cursor is None:
            return found
        if cursor in seen:
            raise ValueError("Server repeated its tools/list cursor")
        seen.add(cursor)


async def run_mcp_operation(args, receipt: dict, errlog) -> None:
    sdk = version("mcp")
    receipt["mcp_sdk"] = sdk
    if sdk != "1.29.1":
        raise ValueError(
            f"Unsupported MCP SDK {sdk}; this helper requires mcp==1.29.1. "
            "Use uv run --script to prepare the pinned dependency."
        )
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    server = load_server(args.config, args.server)
    code = (
        build_code(args.code_file, args.params_file)
        if args.operation == "execute"
        else None
    )
    blend_file = (
        args.blend_file.resolve()
        if args.operation == "execute" and args.blend_file
        else None
    )
    if blend_file and not blend_file.is_file():
        raise ValueError("The selected .blend file does not exist")
    receipt["stage"] = "initialize"
    async with stdio_client(StdioServerParameters(**server), errlog=errlog) as (
        read,
        write,
    ):
        async with ClientSession(
            read, write, read_timeout_seconds=timedelta(seconds=args.timeout)
        ) as session:
            initialized = await session.initialize()
            receipt["server_info"] = initialized.serverInfo.model_dump(mode="json")
            receipt["stage"] = "discover"
            available = await discover(session)
            receipt["tools"] = [t.model_dump(mode="json") for t in available]
            if args.operation == "probe":
                receipt["stage"] = "completed"
                return
            tool = (
                "execute_blender_code_for_cli" if blend_file else "execute_blender_code"
            )
            receipt["tool"] = tool
            definition = next((t for t in available if t.name == tool), None)
            if definition is None:
                raise ValueError(f"Server does not expose {tool}; inspect its tools")
            arguments = {"code": code}
            if blend_file:
                arguments["blend_file"] = str(blend_file)
            properties = definition.inputSchema.get("properties", {})
            if any(key not in properties for key in arguments):
                raise ValueError(
                    "Discovered tool schema does not match Blender Lab parameters"
                )
            receipt["stage"] = "execute"
            response = await session.call_tool(tool, arguments)
            receipt["raw_result"] = response.model_dump(mode="json")
            receipt["stage"] = "decode"
            receipt["result"] = decode_result(
                receipt["raw_result"], "cli" if blend_file else "interactive"
            )
            receipt["stage"] = "completed"


def error_text(error: BaseException) -> str:
    if isinstance(error, BaseExceptionGroup):
        return "; ".join(error_text(child) for child in error.exceptions)
    return f"{type(error).__name__}: {error}"


def parse_args(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", type=Path, default=default_config())
    common.add_argument("--server", default="blender")
    common.add_argument(
        "--receipt",
        type=Path,
        required=True,
        help="New JSON file; existing files are preserved",
    )
    common.add_argument(
        "--timeout",
        type=positive_seconds,
        default=300.0,
        help="Per-request client timeout in seconds",
    )
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="operation", required=True)
    modes.add_parser(
        "probe",
        parents=[common],
        help="Initialize MCP and list tools; no Blender code is run",
    )
    execute = modes.add_parser(
        "execute", parents=[common], help="Execute Python through Blender Lab MCP"
    )
    execute.add_argument("--code-file", type=Path, required=True)
    execute.add_argument("--params-file", type=Path)
    execute.add_argument(
        "--blend-file", type=Path, help="Select the MCP CLI tool for this file"
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    receipt = {
        "operation": args.operation,
        "server": args.server,
        "stage": "prepare",
        "ok": False,
    }
    args.receipt = args.receipt.expanduser().resolve()
    args.config = args.config.expanduser().resolve()
    stderr_file = args.receipt.with_name(args.receipt.name + ".stderr.log")
    try:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        # New receipts retain each attempt, including partial failures.
        with args.receipt.open("x") as output:
            try:
                with stderr_file.open("x") as errlog:
                    asyncio.run(run_mcp_operation(args, receipt, errlog))
                receipt["ok"] = True
            except (Exception, KeyboardInterrupt) as error:
                receipt["error"] = error_text(error)
            json.dump(receipt, output, indent=2, allow_nan=False)
            output.write("\n")
    except OSError as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    print(
        json.dumps(
            {
                "ok": receipt["ok"],
                "stage": receipt["stage"],
                "receipt": str(args.receipt),
                "stderr": str(stderr_file),
                "error": receipt.get("error"),
            }
        )
    )
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
