"""Exercise helper failures without requiring Blender or an MCP installation."""

import argparse
import asyncio
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

if sys.version_info < (3, 11):
    raise unittest.SkipTest("The optional Blender client requires Python 3.11+")

ROOT = Path(__file__).resolve().parents[1] / "skills/gda-blender-mcp/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


client = load("mcp_stdio_client")
inspector = load("inspect_blender_asset")


class ClientTests(unittest.TestCase):
    def test_config_home_and_literal_arguments(self):
        with tempfile.TemporaryDirectory(prefix="mcp with spaces ") as directory:
            config = Path(directory) / "config.toml"
            config.write_text(
                '[mcp_servers.custom]\ncommand="uv"\nargs=["$HOME/server", "a b"]\n[mcp_servers.custom.env]\nASSET_FLAG="yes"\n'
            )
            with patch.dict(os.environ, {"CODEX_HOME": directory}):
                self.assertEqual(client.default_config(), config)
                server = client.load_server(config, "custom")
            self.assertEqual(server["args"], ["$HOME/server", "a b"])
            self.assertEqual(server["env"]["ASSET_FLAG"], "yes")

    def test_refuses_wrong_server_definition(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.toml"
            for definition in (
                'command="uv"\nenabled=false',
                'url="https://example.test"',
                'command="uv"\nargs="bad"',
                'command="uv"\ncwd="relative"',
            ):
                with self.subTest(definition=definition):
                    config.write_text("[mcp_servers.blender]\n" + definition)
                    with self.assertRaises(ValueError):
                        client.load_server(config, "blender")
            with self.assertRaises(ValueError):
                client.load_server(config, "missing")

    def test_parameters_are_data_and_imports_are_self_contained(self):
        with tempfile.TemporaryDirectory(prefix="asset files ") as directory:
            code = Path(directory) / "read inputs.py"
            data = Path(directory) / "params.json"
            code.write_text(
                'from __future__ import annotations\nresult = {"path": params["path"]}\n'
            )
            value = "a'b\"c\n$HOME/`command`/$(command)"
            data.write_text(json.dumps({"path": value}))
            namespace = {}
            exec(client.build_code(code, data), namespace)
            self.assertEqual(namespace["result"], {"path": value})
            data.write_text("[]")
            with self.assertRaises(ValueError):
                client.build_code(code, data)

    def test_interactive_and_cli_have_different_envelopes(self):
        raw = {"structuredContent": {"status": "ok", "result": {"meshes": 3}}}
        self.assertEqual(client.decode_result(raw, "interactive"), {"meshes": 3})
        raw = {"content": [{"type": "text", "text": '{"meshes": 3}'}]}
        self.assertEqual(client.decode_result(raw, "cli"), {"meshes": 3})
        custom = {"structuredContent": {"status": "error", "domain_data": True}}
        self.assertEqual(
            client.decode_result(custom, "cli"), custom["structuredContent"]
        )

    def test_errors_and_unknown_shapes_are_not_success(self):
        for raw in (
            {"isError": True},
            {"structuredContent": {"status": "error", "message": "bad code"}},
            {"structuredContent": {"status": "ok", "result": []}},
            {"content": []},
            {"content": [{"type": "image"}]},
            {"content": [{"type": "text", "text": "not json"}]},
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                client.decode_result(raw, "interactive")

    def test_paginated_discovery_and_cycle(self):
        class Session:
            def __init__(self, cycle=False):
                self.cursors = []
                self.cycle = cycle

            async def list_tools(self, cursor=None):
                self.cursors.append(cursor)
                return SimpleNamespace(
                    tools=[cursor],
                    nextCursor="next" if cursor is None or self.cycle else None,
                )

        session = Session()
        self.assertEqual(asyncio.run(client.discover(session)), [None, "next"])
        self.assertEqual(session.cursors, [None, "next"])
        with self.assertRaises(ValueError):
            asyncio.run(client.discover(Session(cycle=True)))

    def test_failure_receipt_and_no_retry(self):
        calls = []

        async def fail(args, receipt, errlog):
            calls.append(1)
            receipt["stage"] = "execute"
            raise RuntimeError("expected node missing")

        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "failure.json"
            with patch.object(client, "call", fail), redirect_stdout(io.StringIO()):
                self.assertEqual(client.main(["probe", "--receipt", str(receipt)]), 1)
                original = receipt.read_text()
                self.assertEqual(client.main(["probe", "--receipt", str(receipt)]), 1)
            self.assertEqual(calls, [1])
            self.assertEqual(receipt.read_text(), original)
            self.assertIn("expected node missing", json.loads(original)["error"])
            self.assertEqual(json.loads(original)["stage"], "execute")

    def test_invalid_timeouts(self):
        for value in ("0", "-1", "nan", "inf"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                client.positive_seconds(value)


class InspectorTests(unittest.TestCase):
    def test_bad_parameters_fail_before_blender_access(self):
        for params in (None, {}, {"scene": "a", "root": "b", "expected_nodes": "a"}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                inspector.inspect_asset(params)

    def test_missing_scene_root_and_expected_node_raise(self):
        objects = {}
        scene = SimpleNamespace(objects=objects)
        bpy = SimpleNamespace(data=SimpleNamespace(scenes={"scene": scene}))
        with patch.dict(sys.modules, {"bpy": bpy}):
            with self.assertRaisesRegex(ValueError, "Scene not found"):
                inspector.inspect_asset({"scene": "missing", "root": "root"})
            with self.assertRaisesRegex(ValueError, "Root not found"):
                inspector.inspect_asset({"scene": "scene", "root": "root"})
            objects["root"] = SimpleNamespace(name="root", children_recursive=[])
            with self.assertRaisesRegex(ValueError, "Expected nodes missing"):
                inspector.inspect_asset(
                    {"scene": "scene", "root": "root", "expected_nodes": ["missing"]}
                )
