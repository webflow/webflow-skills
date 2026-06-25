---
name: webflow-mcp:figma-to-webflow
description: >-
  Build a Webflow page, section, component, or full site from a Figma design
  using the Figma MCP and the Webflow MCP (Designer Bridge + Data API). Use
  whenever translating a Figma file/frame into Webflow, building directly in a
  Webflow project, or implementing a design as live Webflow elements/styles
  (not a copy-paste fragment). Triggers: "build this Figma in Webflow",
  "Figma to Webflow", "implement this design in Webflow", a figma.com URL +
  a Webflow site, "recreate this in my Webflow project".
---

# Figma → Webflow

Translate a Figma design into a live Webflow project: real elements, styles,
assets, fonts, and (optionally) custom code + interactions.

## Instructions

Follow this order exactly. When a step says to read a reference file, read it
before doing that work; those files contain the failure modes for that step.

## Non-Negotiable Gates

Treat these as build gates, not suggestions. If you cannot satisfy one, stop
and explain the tradeoff instead of silently substituting.

- **Bridge gate:** Designer Bridge is the default build mode. If selected, provide or request the Designer launch link and wait for the user to open the project with the Designer tab foregrounded before bridge-dependent steps. If the bridge disconnects, keep structural work headless and reconnect before snapshots/canvas inspection.
- **Native style gate:** apply styles with `data_style_tool`, never with the `data_whtml_builder` `css` param or raw `var()` strings. Otherwise styles land in Custom properties instead of native controls. Bind Webflow variables with `variable_as_value`.
- **Variables gate:** decide the Webflow variable/design-system strategy before creating styles. Do not hard-code repeated colors/type/spacing/radii unless the user explicitly chooses hard-coded output.
- **Vector gate:** logos, icons, and marks must be inline SVG embeds, not PNG/JPG uploads, unless the user explicitly approves raster fallback.
- **Raster quality gate:** hero/product/mockup images must use a confirmed 2x source where crispness matters.
- **Dashed accent gate:** dashed lines, dividers, grids, accents, and underlines must use `repeating-linear-gradient`, not `border-style:dashed`, unless the user explicitly accepts browser-default dash rhythm.
- **Publish gate:** do not publish by default. Offer `.webflow.io` publish only after build/review, and only proceed on explicit user confirmation.

## Tool Surfaces

| Surface | Examples | Needs Designer open? |
|---|---|---|
| **Data API** (headless) | `data_whtml_builder`, `data_element_builder`, `data_element_tool`, `data_style_tool`, `data_fonts_tool`, `data_pages_tool`, `data_scripts_tool`, `data_assets_tool`, publish | No |
| **Designer Bridge** | `element_snapshot_tool`, `designer_tool` canvas/selection/navigation, `asset_tool upload_image_by_url` | **Yes — Designer tab open AND foregrounded** |

- Call `webflow_guide_tool` once before other Webflow tools. Confirm auth/site with `whoami` + `get_site`.
- Prefer bridge-assisted builds by default for better visual feedback, while still using `data_*` tools for DOM, classes/styles, text, semantic tags, responsive overrides, fonts, scripts, pages, and asset records.
- If Designer is disconnected, continue structural work headlessly with `query_styles`, `get_all_elements`, and `query_elements`; reconnect the bridge for snapshots, canvas inspection, and any still-required bridge-gated image processing fallback.
- If a bridge tool returns `status:false` or "Unable to connect to Webflow Designer," share the launch link and ask the user to open the Designer **and keep that browser tab in the foreground** — it idles/disconnects when backgrounded. Retry before assuming anything broke.

## Workflow

### 1. Gather And Decide

1. Use Figma MCP:
   - `get_metadata` for structure.
   - `get_design_context` for major frames/sections.
   - `get_variable_defs` for colors, type, spacing, radii.
   - Read page/canvas background; do not assume white.
2. Use Webflow MCP:
   - `webflow_guide_tool` first.
   - Confirm target site/page and inspect existing variables/styles.
3. Ask the required setup prompts below.
4. Confirm ambiguous design intent before building. If Figma component instances contain repeated placeholder labels, ask for intended copy instead of copying placeholders.

### Required Prompts

Before creating Webflow variables, classes, or CSS, ask about build mode, design-system strategy, naming, and units.

**Build-mode prompt:**

> Do you want me to build headless, or use the Webflow Designer Bridge app during the build?

Offer these choices, with Designer Bridge selected as the default:

1. **Use the Designer Bridge during the build (default)** — better feedback loop and visual confidence. The agent can take snapshots, inspect the canvas/page state, confirm layering/composition earlier, and catch visual issues while building. Requires the Webflow Designer tab to be open, connected, and kept in the foreground; if the tab is backgrounded or idle, bridge tools can disconnect or return `status:false`.
2. **Build headless first** — fastest and least interruptive. Use `data_*` tools for DOM, styles, variables, fonts, assets, pages, scripts, responsive overrides, and structural verification; ask for the bridge only if visual QA or image processing needs it.

If the user does not choose, default to **use the Designer Bridge during the build**. Share or request the Designer launch link and remind them to keep the tab foregrounded while bridge tools run.

**Design-system prompt:**

> How should I handle Webflow variables for this build?

Offer these choices, with "read existing variables and create missing ones" selected as the recommended default for existing sites:

1. **Read existing variables and create missing ones (recommended)** — inspect current Webflow variables first, map Figma tokens to existing variables when possible, and create only the missing colors, typography, spacing, and radius variables needed for the design.
2. **Create a new design system from scratch** — create a fresh variable set from the Figma design's colors, typography, spacing, and radii before building sections. Best for blank/new sites or isolated experiments.
3. **Use existing variables only** — inspect and use only variables that already exist in Webflow. If a Figma token has no match, ask before hard-coding or changing the design.
4. **Do not use Webflow variables** — hard-code values in the generated styles. Use only when the user explicitly chooses speed or one-off output over maintainability.

If the user does not choose, default to **read existing variables and create missing ones**. For a brand-new/blank site, recommend **create a new design system from scratch** and explain why before proceeding.

**Naming prompt:**

> Do you want to use FlowKit naming conventions for new styles?

Offer these choices, with FlowKit selected as the recommended default:

1. **Yes, use FlowKit naming (recommended)** — follow the `webflow-mcp:flowkit-naming` skill when creating new styles. Use FlowKit patterns such as `fk-[component]`, `fk-[component]-[element]`, utility classes like `fk-section` / `fk-container`, and combo-state classes like `is-active`.
2. **Use the existing Webflow design system if one exists** — inspect existing classes/styles first, reuse the site's established tokens and naming patterns, and only introduce new names that fit that system.
3. **Use clear semantic names for this build** — create layout/structure-based kebab-case names that are easy to maintain, without forcing FlowKit if the site does not use it.

If the user does not choose, default to **FlowKit naming**. Never mix naming strategies casually within the same build; if an established site system conflicts with FlowKit, call out the tradeoff and ask before proceeding.

**Unit prompt:**

> Do you want this build to use px, rem, or em units?

Offer these choices, with px selected as the default:

1. **px (default)** — match Figma/Webflow values directly and avoid conversion drift.
2. **rem** — use scalable root-relative units for typography and spacing where practical.
3. **em** — use component-relative units where the design intentionally scales with local font size.

If the user does not choose, default to **px**. Keep units consistent within a build; only mix units when there is a clear reason, such as `%` for fluid widths or `em` for icon/text relationships.

### 2. Build Foundations And Sections

Before creating variables/classes/styles, read [CSS rules](references/css-rules.md).

1. Create or map Webflow variables according to the selected strategy.
2. Create reusable primitives first: page wrapper, containers, typography, spacing, buttons, image-fill, cards, nav.
3. Use `data_whtml_builder` for DOM/structure only: one root section per action, semantic tags, nesting, text, and class names.
4. Create styles with `data_style_tool create_style` / `update_style`. Repeat: do **not** use the WHTML `css` param for styling.
5. Capture returned element ids. Re-find later with `query_elements`, then filter by exact class/type before acting.
6. Build in section-sized batches. Prefer structural verification with `query_elements` / `query_styles` between visual checks.

### 3. Attach Assets

Before handling images or vectors, read [Assets and SVG](references/assets-and-svg.md).

1. Use `data_assets_tool create_asset` for raster assets. Download source bytes locally, compute MD5, POST to presigned S3, then verify nonzero size/variants before placement.
2. For hero/product/mockup images, confirm 2x source before placement.
3. Bind images by asset ID with `set_image_asset`; never rely on raw `<img src="...">`.
4. Inline vector marks as `HtmlEmbed` SVGs and set embed code with `data_element_tool set_settings`.
5. Upload fonts with `data_fonts_tool`; never add Google Fonts `<link>` tags to head.

### 4. Navbar And Custom Behavior

If the build includes a navbar, read [Navbar](references/navbar.md) before building it.

- Ask which breakpoint should collapse to hamburger.
- Webflow native Navbar cannot be created via API/WHTML. Build a semantic custom nav or ask the user to add the native element in Designer.
- Put component behavior `<style>`/`<script>` in an HtmlEmbed inside the component root. Use site/page head code only for truly global behavior.

### 5. Responsive And QA

Before responsive/final verification, read [Verification](references/verification.md).

1. Use `data_style_tool update_style` with breakpoint ids (`main`, `medium`, `small`, `tiny`). Desktop-first: set base, override downward.
2. If Designer Bridge is selected, snapshot groups/wrappers rather than every element. Keep the Designer tab foregrounded.
3. Verify overlays/layering with a full-page composite, not isolated-section snapshots.
4. Do not trust first snapshots for fonts; warm cache and re-snapshot before changing font implementation.
5. Do not claim embed behavior, custom code, blur, WebGL, animation, or mobile widths are verified from your side. Ask the user to confirm in preview/published site.
6. Offer publish/review next steps. Default remains **no publish**.

## Examples

### Example 1: Build a Figma frame into a Webflow page

**User:** "Build this Figma frame in my Webflow site: [figma.com URL]"

1. Use Figma MCP to gather metadata, design context, variables, screenshots, and export URLs for the requested frame.
2. Use Webflow MCP to call `webflow_guide_tool`, confirm the user/site/page, and inspect existing styles.
3. Ask whether to use Designer Bridge during the build or build headless first; explain the bridge is recommended for visual feedback but requires the Designer tab open and foregrounded.
4. Ask how to handle Webflow variables, whether to use FlowKit naming / existing class patterns / semantic names, and whether to use `px`, `rem`, or `em` units.
5. Ask about ambiguous design intent and navbar collapse breakpoint if relevant.
6. Confirm the build gates: Designer link/foreground tab if using bridge, SVG embeds for vector marks, 2× raster sources where needed, and gradient-based dashed accents.
7. Read the referenced files at their point of use, set up or map variables, build DOM with `data_whtml_builder`, style with `data_style_tool`, attach assets by Webflow asset ID, verify, then ask whether they want to publish to `.webflow.io`. Default to no.

### Example 2: Recreate a Figma section in an existing Webflow page

**User:** "Recreate this pricing section from Figma on my homepage."

1. Extract the section's Figma tokens, assets, and reference code.
2. Confirm the target Webflow site/page and ask whether to use the default Designer Bridge flow or build headless first.
3. Confirm build mode plus variable, naming, and unit strategy before generating new Webflow classes/CSS; default to Designer Bridge, existing variables plus missing variables, FlowKit, and `px` if the user has no preference.
4. Present a concise preview plan that calls out the non-negotiable build gates, then require explicit confirmation before creating elements.
5. Insert one section, constrain confirmed 2× images to display size, verify structurally headless or visually with bridge snapshots if selected, and ask the user to confirm any embed or responsive behavior that cannot be self-verified.

## Guidelines

- Always use Figma MCP for design extraction and Webflow MCP for Webflow operations; never use direct Webflow API calls.
- Call `webflow_guide_tool` before other Webflow tools in the workflow.
- Ask for build mode, Webflow variable, style naming, and CSS unit strategy before creating classes. Default to Designer Bridge, existing variables plus missing variables, FlowKit naming, and `px`; reference `webflow-mcp:flowkit-naming` when FlowKit is selected.
- Treat mutating Webflow operations as confirmation-gated. Require explicit user approval before creating, updating, publishing, or deleting.
- Prefer `data_whtml_builder` for DOM/section construction, then `data_style_tool` for all styling and element tools for precise asset binding, embeds, and refinements.
- Keep CSS Webflow-compatible. Only non-native CSS belongs in Custom properties.
- Do not publish by default. If the user wants a live review link, publish to the `.webflow.io` subdomain before any custom domains.

## Checklist before declaring done

- [ ] Required reference files were read at their point of use.
- [ ] All CSS longhand; correct breakpoints; flexbox-first.
- [ ] Styles applied via `data_style_tool` (native controls), variables bound with `variable_as_value`, and only truly non-native CSS (`backdrop-filter`, `aspect-ratio`, `repeating-linear-gradient`, etc.) left as custom properties.
- [ ] Build mode followed: bridge-assisted by default with Designer tab open and foregrounded, or headless-first if the user chose it.
- [ ] Webflow variables handled according to the selected strategy; repeated colors/type/spacing/radii are mapped or created unless hard-coding was explicitly selected.
- [ ] Images attached by asset ID (not orphan `<img src>`); 2× source confirmed where crispness matters.
- [ ] Vector marks are clean inline-SVG embeds (backgrounds stripped), or user explicitly approved raster fallback.
- [ ] Dashed accents/dividers/grids use `repeating-linear-gradient`, not `border-style:dashed`, unless user explicitly approved browser-default dashes.
- [ ] Fonts uploaded + referenced by exact family name; temp `<head>` link removed.
- [ ] Runtime-toggled classes have guaranteed CSS (not stripped).
- [ ] Responsive overrides at medium/small/tiny.
- [ ] If published to subdomain, user asked to confirm anything you can't self-verify (embeds, WebGL, blur, mobile).
