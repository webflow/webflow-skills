import os

# Path to the webflow-skills repo root (one level up from evals/)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MCP config path
MCP_CONFIG = os.path.join(REPO_ROOT, ".mcp.json")

# Plugin directories — all plugins loaded so trigger tests can verify correct skill selection
PLUGIN_DIRS = [
    os.path.join(REPO_ROOT, "plugins", "webflow-designer-tools"),
    os.path.join(REPO_ROOT, "plugins", "webflow-skills"),
    os.path.join(REPO_ROOT, "plugins", "webflow-code-component-skills"),
    os.path.join(REPO_ROOT, "plugins", "webflow-cli-skills"),
]

# MCP tool name prefix
MCP_PREFIX = "mcp__webflow__"

# All known Webflow MCP tools (without prefix)
KNOWN_WEBFLOW_TOOLS = {
    "webflow_guide_tool",
    "data_sites_tool",
    "data_cms_tool",
    "data_pages_tool",
    "data_components_tool",
    "data_scripts_tool",
    "element_tool",
    "element_builder",
    "element_snapshot_tool",
    "de_component_tool",
    "de_page_tool",
    "style_tool",
    "variable_tool",
    "asset_tool",
    "de_learn_more_about_styles",
    "ask_webflow_ai",
    "get_image_preview",
}

# All known tools = MCP tools (with prefix) + built-in Claude tools
KNOWN_MCP_TOOLS = {f"{MCP_PREFIX}{t}" for t in KNOWN_WEBFLOW_TOOLS}
KNOWN_BUILTIN_TOOLS = {
    "Read", "Edit", "Write", "Bash", "Glob", "Grep",
    "Skill", "ToolSearch", "Agent",
    "TaskCreate", "TaskUpdate", "TaskGet", "TaskList", "TaskOutput", "TaskStop",
    "WebFetch", "WebSearch",
    "AskUserQuestion", "NotebookEdit",
    "EnterPlanMode", "ExitPlanMode",
    "EnterWorktree", "ExitWorktree",
    "CronCreate", "CronDelete", "CronList",
    "mcp__webflow__authenticate",
}
KNOWN_TOOLS = KNOWN_MCP_TOOLS | KNOWN_BUILTIN_TOOLS

# Default max turns
MAX_TURNS_DIRECT = 15
MAX_TURNS_TRIGGER = 5

# Default model for eval runs (cheaper)
EVAL_MODEL = "sonnet"
