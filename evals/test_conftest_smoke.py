"""Smoke test to verify conftest fixtures work."""
from conftest import run_claude, extract_tool_calls, extract_skill_invocations, get_result


def test_run_claude_returns_events():
    """run_claude should return a list of parsed events."""
    events = run_claude(prompt="say hello", max_turns=1)
    assert isinstance(events, list)
    assert len(events) > 0


def test_run_claude_has_init_event():
    """First event should be system init."""
    events = run_claude(prompt="say hello", max_turns=1)
    init_events = [e for e in events if e.get("type") == "system" and e.get("subtype") == "init"]
    assert len(init_events) == 1


def test_run_claude_has_result_event():
    """Should have a result event."""
    events = run_claude(prompt="say hello", max_turns=1)
    result = get_result(events)
    assert result is not None
    assert result["stop_reason"] == "end_turn"


def test_extract_tool_calls_with_read():
    """When Claude reads a file, extract_tool_calls should capture it."""
    events = run_claude(
        prompt="read the file evals/pytest.ini",
        max_turns=3,
    )
    tools = extract_tool_calls(events)
    read_calls = [t for t in tools if t["name"] == "Read"]
    assert len(read_calls) >= 1


def test_extract_skill_invocations_empty():
    """A non-skill prompt should produce no skill invocations."""
    events = run_claude(prompt="say hello", max_turns=1)
    skills = extract_skill_invocations(events)
    assert skills == []
