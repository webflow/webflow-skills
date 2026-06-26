# CSS And Build Rules

Read this before creating Webflow variables, classes, styles, or responsive overrides.

## Native Styling Gate

- Apply styles with `data_style_tool`, never with the `data_whtml_builder` `css` param. WHTML CSS lands in Designer **Custom properties**, so the result is hard to edit and does not map to native Style-panel controls.
- Bind Webflow variables with `variable_as_value: "<variable-id>"` from `data_variable_tool`. Do not use raw `var(--collection---token)` strings; they do not render the native variable pill.
- Only truly non-native CSS belongs in Custom properties: `backdrop-filter`, `aspect-ratio`, `repeating-linear-gradient` backgrounds, parent-state selectors, custom mobile-toggle selectors, and similar CSS Webflow cannot model.
- Do not use embed `<style>` blocks for normal layout, typography, spacing, backgrounds, dividers, grids, cards, or section styling. That hides styling from the Designer style panel.
- Do not use `::before` or `::after`. Pseudo-elements are invisible in the Navigator and unselectable in Designer. Build decorative lines, grids, badges, and backgrounds as real elements with native classes.

## Webflow-Compatible CSS

- Use longhand properties. Expand `padding`, `margin`, `border`, `border-radius`, `font`, `background`, `transition`, and `flex`.
- Use class selectors only. No tag, ID, descendant, or attribute selectors. `:hover` is the only safe pseudo-class in native styles.
- Emit `grid-row-gap` and `grid-column-gap` even on flex; Webflow stores gaps under those keys.
- Build desktop-first: base styles apply to all devices, then override downward.
  - `main`: base desktop
  - `medium`: 991px and below
  - `small`: 767px and below
  - `tiny`: 479px and below
- Prefer flexbox. Use grid only for true two-dimensional layouts.
- Avoid unsupported/dropped values: `calc()`, `clamp()`, `min()`, `max()`, `@keyframes`, `@font-face`, multi-layer `box-shadow`, logical props, vendor prefixes.
- Put inheritable typography once on `.page-wrapper`: font family, color, base size, line height. Use single font names, no fallback stacks.

## Design System And Units

- Follow the selected variable strategy before building sections.
- Prefer Webflow variables for repeated colors, typography, spacing, and radii unless the user explicitly selected hard-coded output.
- Follow the selected naming strategy. If using FlowKit, read/reference `webflow-mcp:flowkit-naming`; otherwise use layout/structure-based kebab-case names and never page-prefixed names.
- Follow the selected unit preference. Default to `px`; convert to `rem` or `em` only when the user chooses that strategy.

## Element Construction

- Use `data_whtml_builder` for DOM/structure only: one root element per action, markup, semantic tags, text, nesting, and class names.
- To insert multiple sibling sections, use multiple WHTML actions.
- If a class does not exist, create it with `data_style_tool create_style`; do not define it through WHTML CSS.
- Create classes before referencing them in WHTML or element class lists. If a custom class exists only as a string in WHTML and no Webflow style exists yet, Webflow can silently drop it, leaving unstyled full-width text or broken layout.
- `set_style` replaces all classes on an element. Include all intended classes when applying it.
- `query_elements` style filters are case-insensitive substring matches. Filter results by exact class/type before acting.
- Capture returned element ids from every insert. Re-find later by exact style/type when possible.
- Element ids are `{component, element}`, where `component` is the page id. Use the matching top-level `pageId`.
- Combo classes can be ambiguous. When in doubt, prefer one standalone class with full styling.

## Layout Patterns

- Use `repeating-linear-gradient`, not `border-style:dashed`, for dashed accents/dividers/underlines so dash length, gap, opacity, and direction match the design.
- Decorative overlays must sit behind content. Make `.page-wrapper` a stacking context (`position:relative; z-index:0`) and place overlays at `z-index:-1`.
- Never use a fixed overlay width wider than the viewport. Prefer `left:0; right:0; width:auto; max-width:<design-width>; margin-left:auto; margin-right:auto`.
- Replicate interior grid lines too, not just outer edges; check Figma for distributed columns.
- A fixed nav lets the first section sit under the bar; add top-padding to clear it. Sticky nav reserves space.
- Suppress Designer-only `.wf-empty` affordances on decorative empty normal DivBlocks with a dimension-giving style in the active breakpoint. For custom-tag empty elements, add a child or use a normal DivBlock.
