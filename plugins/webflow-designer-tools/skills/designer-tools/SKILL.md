---
name: designer-tools
description: Build and manage pages, elements, components, and styles in Webflow Designer. Use when adding sections, creating layouts, building elements, inspecting or updating components, viewing what's inside a component, restructuring pages, creating new pages, previewing page structure, styling elements, or managing component properties. Requires Webflow Designer connection.
---

# Page Structure

Build, inspect, and manage page elements and components in the Webflow Designer.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**
- Use Webflow MCP's `webflow_guide_tool` to get best practices **before any other tool call**
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify the target site
- Use Webflow MCP's `de_page_tool` to get current page, switch pages, or create pages/folders
- Use Webflow MCP's `element_tool` with action `get_all_elements` to retrieve page elements
- Use Webflow MCP's `element_tool` with action `select_element` to select a specific element
- Use Webflow MCP's `element_tool` with action `add_or_update_attribute` to update element attributes
- Use Webflow MCP's `element_builder` to create new elements (max 3 levels deep)
- Use Webflow MCP's `element_snapshot_tool` to get visual previews of elements before and after changes
- Use Webflow MCP's `style_tool` to create and update styles on elements
- Use Webflow MCP's `de_learn_more_about_styles` to check supported style properties
- Use Webflow MCP's `data_components_tool` with action `list_components` to list all site components
- Use Webflow MCP's `data_components_tool` with action `get_component_content` to inspect a component
- Use Webflow MCP's `data_components_tool` with action `update_component_content` to update component content
- Use Webflow MCP's `data_components_tool` with action `get_component_properties` to get component properties
- Use Webflow MCP's `data_components_tool` with action `update_component_properties` to update component properties
- Use Webflow MCP's `de_component_tool` to manage component instances in the Designer
- DO NOT use any other tools or methods for Webflow operations
- All tool calls must include the required `context` parameter (15-25 words, third-person perspective)
- **Designer connection required** — user must have Webflow Designer open and connected

## Instructions

### Phase 1: Discovery
1. **Call `webflow_guide_tool` first** — always the first MCP tool call in any workflow
2. **Get the site**: Use `data_sites_tool` with action `list_sites` to identify the target site. If only one site exists, use it automatically.
3. **Get current page**: Use `de_page_tool` to identify which page is active in the Designer
4. **If user specifies a different page**: Use `de_page_tool` to switch to it before proceeding
4. **Identify the task type**:
   - **Inspect**: List elements, view structure, preview → go to Phase 2
   - **Build/Modify/Delete**: Add, update, restructure, remove → go to Phase 3
   - **Components**: List, inspect, update → go to Phase 2 or Phase 3 depending on read vs write

### Phase 2: Inspection (read-only operations)
5. **List page elements**: Use `de_page_tool` then `element_tool` with `get_all_elements` to retrieve page structure. Present a summary of sections, elements, and nesting.
6. **Preview elements**: Use `element_snapshot_tool` to get visual previews of specific sections
7. **List components**: Use `data_components_tool` with action `list_components` to list all site components
8. **Inspect a component**: Use `data_components_tool` with action `get_component_content` or `de_component_tool` for Designer instances

### Phase 3: Planning (before any mutation)
Before creating, updating, or deleting anything:
9. **Snapshot current state**: Use `element_snapshot_tool` to capture the area being changed
10. **Present the plan**: Describe exactly what will be created, modified, or deleted
11. **Request explicit confirmation**: Ask the user before proceeding:
    - "Would you like me to proceed with these changes?"
    - "Shall I go ahead and create this?"
    - "Do you want me to apply these changes?"
    - "Before I make changes, here's what I'll do: [plan]. Confirm to proceed."
12. **For destructive operations** (delete, restructure): Require "confirm" or "delete", warn about child elements that will also be affected

### Phase 4: Execution (after confirmation only)
13. **Build elements**: Use `element_builder` to create new elements (max 3 levels deep). For deeper structures, build in multiple passes.
14. **Style elements**: Use `style_tool` to apply or update styles on created or existing elements
15. **Modify elements**: Use `element_tool` with `add_or_update_attribute` to update attributes, text, or links
16. **Update components**: Use `data_components_tool` with `update_component_content` or `update_component_properties`. Use `de_component_tool` for Designer-level instance changes.
17. **Create pages**: Use `de_page_tool` to create new pages or folders

### Phase 5: Verification
18. **Snapshot the result**: Use `element_snapshot_tool` to capture the new state
19. **Report what changed**: Summarize the changes made

## Examples

### Example 1: List page elements

**User:** "Show me all elements on the homepage"

1. Call `webflow_guide_tool` for best practices
2. Call `data_sites_tool` with `list_sites` to identify the site
3. Call `de_page_tool` to confirm current page is homepage (switch if needed)
4. Call `element_tool` with `get_all_elements` to retrieve page structure
5. Present organized summary of sections, elements, and nesting

### Example 2: Build a hero section

**User:** "Add a hero section with a heading and CTA button"

1. Call `webflow_guide_tool` for best practices
2. Call `data_sites_tool` with `list_sites` to identify the site
3. Call `de_page_tool` to get current page
4. Call `element_snapshot_tool` to capture current state
4. Present plan: "I'll create a Section with a Heading and Button. Would you like me to proceed?"
5. After confirmation: call `element_builder` with nested structure
6. Call `style_tool` to apply styles (padding, background, typography)
7. Call `element_snapshot_tool` to show the result

### Example 3: Update a component

**User:** "Update the footer copyright text to 2026"

1. Call `webflow_guide_tool` for best practices
2. Call `data_sites_tool` with `list_sites` to identify the site
3. Call `data_components_tool` with `list_components` to find the footer
3. Call `data_components_tool` with `get_component_content` to inspect it
4. Present: "I'll update the copyright text from '2025' to '2026'. Would you like me to proceed?"
5. After confirmation: call `data_components_tool` with `update_component_content`
6. Report the change

### Example 4: Restructure a section

**User:** "Restructure the hero section layout"

1. Call `webflow_guide_tool` for best practices
2. Call `data_sites_tool` with `list_sites` to identify the site
3. Call `de_page_tool` to get current page
3. Call `element_snapshot_tool` to capture current hero section
4. Call `element_tool` to inspect current structure
5. Present restructuring plan with before/after description
6. After confirmation: apply changes using `element_tool` and/or `element_builder`
7. Call `element_snapshot_tool` to show the result

### Example 5: Create a two-column layout

**User:** "Create a two-column layout with text on left and image on right"

1. Call `webflow_guide_tool` for best practices
2. Call `data_sites_tool` with `list_sites` to identify the site
3. Call `de_page_tool` to get current page
3. Call `element_snapshot_tool` to capture current state
4. Present plan: "I'll create a Grid with two columns — text block on left, image on right. Would you like me to proceed?"
5. After confirmation: call `element_builder` with grid structure
6. Call `style_tool` to set grid layout properties
7. Call `element_snapshot_tool` to show the result

## Guidelines

- **`webflow_guide_tool` always first** — before any other MCP tool in every workflow
- **Snapshot before and after** — use `element_snapshot_tool` before mutations and after to show results
- **Never silently mutate** — every write operation requires explicit user confirmation
- **`de_page_tool` before `element_tool`** — always confirm/switch page before inspecting elements
- **Batch changes need itemized preview** — if modifying multiple elements, list each change
- Prefer Webflow's native layout tools (Grid, Flexbox) over manual positioning
- Components shared across pages should be updated via `data_components_tool` (changes propagate)
- Component instances on a specific page use `de_component_tool`
- `element_builder` supports max 3 levels per call — build deeper structures in stages
- Check `de_learn_more_about_styles` for supported style properties when unsure
