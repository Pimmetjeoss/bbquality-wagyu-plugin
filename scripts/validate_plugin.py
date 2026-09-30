#!/usr/bin/env python3
"""Validate the BBQuality Wagyu marketplace and Agent Plugin package."""
from __future__ import annotations

import json
import pathlib
import urllib.request

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "bbquality-wagyu"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SCHEMAS = {
    "plugin.json": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "mcp.json": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
}


def load_json(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "bbquality-wagyu-plugin-validator/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    for filename, schema_url in SCHEMAS.items():
        jsonschema.validate(load_json(PLUGIN / filename), fetch_json(schema_url))

    marketplace = load_json(MARKETPLACE)
    if marketplace.get("name") != "bbquality-plugins":
        raise SystemExit("Unexpected marketplace name")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise SystemExit("Marketplace must contain exactly one plugin")
    entry = entries[0]
    if entry.get("name") != "bbquality-wagyu":
        raise SystemExit("Marketplace plugin name mismatch")
    source_path = entry.get("source", {}).get("path")
    if source_path != "./plugins/bbquality-wagyu":
        raise SystemExit("Marketplace source.path must target ./plugins/bbquality-wagyu")
    target = (ROOT / source_path[2:]).resolve()
    if not target.is_relative_to(ROOT.resolve()) or target != PLUGIN.resolve():
        raise SystemExit("Marketplace source.path escapes or misses the plugin root")
    policy = entry.get("policy", {})
    if policy.get("installation") != "AVAILABLE" or "authentication" not in policy:
        raise SystemExit("Marketplace installation/authentication policy is incomplete")

    manifest = load_json(PLUGIN / "plugin.json")
    interface = manifest["extensions"]["com.openai"]["interface"]
    for key in ("logo", "composerIcon"):
        reference = interface[key]
        if not reference.startswith("./"):
            raise SystemExit(f"{key} must be relative to plugin root: {reference}")
        asset = (PLUGIN / reference[2:]).resolve()
        if not asset.is_relative_to(PLUGIN.resolve()) or not asset.is_file():
            raise SystemExit(f"Missing or unsafe {key}: {reference}")

    required = [
        PLUGIN / "README.md",
        PLUGIN / "skills" / "bbquality-wagyu-assistant" / "SKILL.md",
        PLUGIN / "assets" / "wagyu-icon.svg",
        PLUGIN / "assets" / "wagyu-logo.svg",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing package files: " + ", ".join(missing))

    mcp = load_json(PLUGIN / "mcp.json")
    server = mcp["mcpServers"]["bbquality-wagyu"]
    if server.get("type") != "streamable-http" or not str(server.get("url", "")).endswith("/mcp"):
        raise SystemExit("mcp.json must use streamable-http and an /mcp URL")

    health_url = str(server["url"]).removesuffix("/mcp") + "/"
    health = fetch_json(health_url)
    if health.get("service") != "bbquality-wagyu-mcp" or health.get("mcp") != "/mcp":
        raise SystemExit("Live MCP health response is not the expected BBQuality Wagyu service")

    print("marketplace and plugin validation: PASS")


if __name__ == "__main__":
    main()
