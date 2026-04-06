"""Shared fixtures for skill evals.

Spawns claude CLI in --print mode with stream-json output,
parses events, and provides helpers to extract tool calls and skill invocations.
"""
import json
import subprocess
from typing import Any

from constants import (
    EVAL_MODEL,
    MAX_TURNS_DIRECT,
    MCP_CONFIG,
    PLUGIN_DIRS,
    REPO_ROOT,
)


def run_claude(
    prompt: str,
    max_turns: int = MAX_TURNS_DIRECT,
    model: str = EVAL_MODEL,
    plugin_dirs: list[str] | None = None,
    mcp_config: str | None = None,
    skip_permissions: bool = True,
) -> list[dict[str, Any]]:
    """Spawn claude CLI and return parsed stream-json events."""
    if plugin_dirs is None:
        plugin_dirs = PLUGIN_DIRS
    if mcp_config is None:
        mcp_config = MCP_CONFIG

    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "stream-json",
        "--verbose",
        "--model", model,
        "--max-turns", str(max_turns),
        "--mcp-config", mcp_config,
    ]

    for d in plugin_dirs:
        cmd.extend(["--plugin-dir", d])

    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=300,
    )

    events = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return events


def extract_tool_calls(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract tool_use content blocks from assistant messages.

    Returns list of dicts with keys: name, input, index.
    """
    tool_calls = []
    index = 0
    for event in events:
        if event.get("type") != "assistant":
            continue
        message = event.get("message", {})
        for block in message.get("content", []):
            if block.get("type") == "tool_use":
                tool_calls.append({
                    "name": block["name"],
                    "input": block.get("input", {}),
                    "index": index,
                })
                index += 1
    return tool_calls


def extract_skill_invocations(events: list[dict[str, Any]]) -> list[str]:
    """Extract skill names from Skill tool_use calls.

    When Claude triggers a skill via natural language, it calls the Skill tool
    with input like {"skill": "webflow-skills:safe-publish"}.
    """
    skills = []
    for event in events:
        if event.get("type") != "assistant":
            continue
        message = event.get("message", {})
        for block in message.get("content", []):
            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                skill_name = block.get("input", {}).get("skill", "")
                if skill_name:
                    skills.append(skill_name)
    return skills


def get_result(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Extract the final result event."""
    for event in events:
        if event.get("type") == "result":
            return {
                "stop_reason": event.get("stop_reason"),
                "num_turns": event.get("num_turns"),
                "total_cost_usd": event.get("total_cost_usd"),
                "is_error": event.get("is_error", False),
                "duration_ms": event.get("duration_ms"),
                "session_id": event.get("session_id"),
            }
    return None
