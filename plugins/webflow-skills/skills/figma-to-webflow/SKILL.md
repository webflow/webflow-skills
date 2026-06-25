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
assets, fonts, and (optionally) custom code + interactions. This skill is the
hard-won playbook — follow the order, and heed the gotchas (each is something
that silently fails or wastes a publish cycle if you don't know it).

## Instructions

### 0. The single most important thing: two tool surfaces

Webflow MCP has **two kinds of tools with different requirements**:

| Surface | Examples | Needs Designer open? |
|---|---|---|
| **Data API** (headless) | `data_whtml_builder`, `data_element_builder`, `data_element_tool`, `data_style_tool`, `data_fonts_tool`, `data_pages_tool`, `data_scripts_tool`, `data_assets_tool`, publish | No |
| **Designer Bridge** | `element_snapshot_tool`, `designer_tool` canvas/selection/navigation, `asset_tool upload_image_by_url` | **Yes — Designer tab open AND foregrounded** |

- Call `webflow_guide_tool` once before other Webflow tools. Confirm auth/site with `whoami` + `get_site`.
- Prefer bridge-assisted builds by default for better visual feedback, while still using `data_*` tools for DOM, classes/styles, text, semantic tags, responsive overrides, fonts, scripts, pages, and asset records.
- If Designer is disconnected, continue structural work headlessly with `query_styles`, `get_all_elements`, and `query_elements`; reconnect the bridge for snapshots, canvas inspection, and any still-required bridge-gated image processing fallback.
- If a bridge tool returns `status:false` or "Unable to connect to Webflow Designer," share the launch link and ask the user to open the Designer **and keep that browser tab in the foreground** — it idles/disconnects when backgrounded. Retry before assuming anything broke.

### 1. Workflow order

1. **Gather** — Figma structure, tokens, per-section code/colors/assets; Webflow site, pages, existing styles.
2. **Choose build mode and style preferences** — ask whether to build headless or bridge-assisted, then ask how Webflow variables, new styles, and CSS units should be handled before creating any classes/CSS (see §3).
3. **Set up foundations** — Webflow variables/design tokens, page wrapper w/ base typography, and fonts.
4. **Build section by section** via `data_whtml_builder` (capture each returned element id to nest the next piece). Verify structurally after each, and visually if the user chose bridge-assisted mode.
5. **Attach assets** (images by ID; inline SVGs via embeds).
6. **Responsive pass** (desktop-first overrides).
7. **Custom code / interactions** last (mobile menu, animated backgrounds, blur).
8. **Offer review/publish next steps** — default to **no publish**. Only publish to the `.webflow.io` subdomain if the user explicitly asks or confirms after reviewing the build.

### Non-negotiable build gates

Treat these as gates, not suggestions. Before building, explicitly confirm the planned choice for each item; if you cannot satisfy one, stop and explain the tradeoff instead of silently substituting.

- **Bridge gate:** if the user chooses Designer Bridge (the default), provide/request the Designer launch link and wait for the user to open the project with the Designer tab foregrounded before running bridge-dependent steps. Do not skip this setup and start building as if headless were selected.
- **Vector gate:** logos, icons, and marks must be inline SVG embeds, not PNG/JPG uploads, unless the user explicitly approves raster fallback. If SVG export cleanup is slow, say so and ask before substituting.
- **Raster quality gate:** hero/product/mockup images must use a 2× source when crispness matters. Verify the asset source/export is 2× or tell the user it is not confirmed.
- **Dashed accent gate:** dashed lines, dividers, grids, accents, and underlines must use `repeating-linear-gradient`, not `border-style:dashed`, unless the user explicitly accepts browser-default dash rhythm.

### Speed defaults

- Build in section-sized batches with `data_whtml_builder`; avoid element-by-element construction unless precision requires it.
- Create variables/classes for common primitives once (containers, typography, spacing, buttons, image-fill, cards, nav) and reuse them aggressively.
- Snapshot groups/wrappers, not every element. Prefer structural verification with `query_elements` / `query_styles` between visual checks.
- Export complex layered visuals as 2× composed images instead of rebuilding every layer in Webflow.
- Gather Figma metadata, variables, and major-section design context up front; avoid repeated per-node Figma calls for small children.
- If using Designer Bridge, keep the tab foregrounded and batch several headless `data_*` operations between bridge snapshots.

Confirm ambiguous design intent up front (e.g., a button whose label is a repeated component placeholder) rather than guessing. **If the build includes a navbar, ask which breakpoint the mobile menu should collapse at before building it (see §10).**

### 2. Extracting from Figma

- `get_metadata` → node/structure map. `get_design_context` per node → reference code + exact colors + asset download URLs + a screenshot. `get_variable_defs` → design tokens (colors, type scale, spacing, radii). Pull tokens early and treat them as law.
- Read the page/canvas background color from Figma; do not assume white. Set the real page background on `.page-wrapper`, or white cards/sections can disappear against the wrong background.
- **Asset URLs from design-context live ~7 days; `get_screenshot` URLs are short-lived** — upload promptly.
- **Vector assets (logos, icons, marks): use `download_assets` with `defaultFormat: "svg"`** — NOT `get_screenshot`. Screenshot only rasterizes and **never upscales past the node's native size** (so it can't give you 2×, and it bakes in surrounding background).
  - **Gotcha:** the SVG export wraps the node in its ancestor chain and **bakes in background fills** clipped to the node box (page background rect, card background, a node "backing" rect). Strip the full-bleed background `<rect>`/`<path>` elements that aren't part of the target → clean transparent vector. (Remaining `fill="white"` inside `<defs><clipPath>` are just clip masks — leave them.)
- **Raster (photos, complex product mockups): can't get 2× from `get_screenshot`.** Use the design-context layer export URLs (often already 2×) or `download_assets` at 2× for a composed parent node; treat layered product mockups as one image instead of reconstructing every layer (see §5, §6).

### 3. Build mode and style preferences

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

### 4. Webflow CSS rules (these bite)

- **Longhand only.** Expand `padding`, `margin`, `border`, `border-radius` (4 corners), `font`, `background`, `transition`, `flex`.
- **Class selectors only.** No tag/ID/descendant/attribute selectors. `:hover` is the only safe pseudo-class; no `::before`/`::after` (use real elements).
- **Gaps:** emit `grid-row-gap` / `grid-column-gap` even on flex (Webflow's stored keys) — not `row-gap`/`column-gap`.
- **Desktop-first breakpoints (Webflow).** Override downward only; WHTML media queries need the `screen and` prefix (e.g., `@media screen and (max-width: 767px)`).
  - **Desktop (base)** — applies to all devices unless overridden at another breakpoint.
  - **Tablet** — screens **991px** and below.
  - **Mobile landscape** — screens **767px** and below.
  - **Mobile portrait** — screens **479px** and below.
- **Flexbox-first**; grid only for true 2D.
- **Forbidden / dropped:** `calc()`, `clamp()`, `min()/max()`, `@keyframes`, `@font-face`, multi-layer `box-shadow`, logical props, vendor prefixes. For animation use IX2 or a custom-code embed.
- Put inheritable typography (font-family, color, base size/line-height) once on `.page-wrapper`; single font names, no fallback stacks.
- Variables: follow the selected design-system strategy before building sections. Prefer Webflow variables for repeated colors, typography, spacing, and radii unless the user explicitly chooses hard-coded styles.
- Naming: follow the selected naming strategy. If using FlowKit, reference `webflow-mcp:flowkit-naming`; otherwise use layout/structure-based, kebab-case names and never page-prefixed names.
- Units: follow the selected unit preference. Default to `px`; convert to `rem`/`em` only when the user chooses that strategy.

### 5. Building elements

- **`data_whtml_builder` is the workhorse** — pass HTML + raw CSS; class selectors become real Webflow styles automatically. Build one section per call, set `return_element_info:true`, and use the returned id as the parent for the next insert.
- **Element identity & page context:** an element id is `{component, element}` where **`component` IS the page id**. `data_element_tool` actions must run with the **matching top-level `pageId`** — a mismatch returns "Element not found." This is exactly how you target a *duplicated* page's elements (pass that page's id).
- `data_element_builder` (typed elements, supports `set_style`/`set_image_asset`/children at creation) is the fallback when you need precise control; component instances need `component_builder`.
- Keep nesting ≤4–5 levels.

### 6. Images & assets

Use the headless Data API asset path first. Do **not** rely on `asset_tool upload_image_by_url` as the primary path; it is Designer Bridge-gated and may be removed.

- **Download Figma asset bytes locally first.** Use the Figma design-context/export URL promptly, write the file to `/tmp/`, and compute the MD5 hash of the actual bytes.
- **Create the asset via `data_assets_tool create_asset`.** Pass `site_id`, `file_name`, and `file_hash`, then POST the local file bytes to the returned presigned S3 form.
  - The presigned **policy is base64 — validate it is pure ASCII** before POSTing (`grep '[^A-Za-z0-9+/=]'`); transcription homoglyphs cause a 403.
  - Append the file field last in the multipart POST.
- **Verify processing before placing the image.** Fetch/check the created asset after upload. If it remains `size:0` or has no variants, tell the user the upload succeeded but Webflow has not processed a renderable asset yet.
- **Bridge-gated fallback:** if processed variants are required and `create_asset` does not process them, raise the issue rather than reverting silently. If a fallback is still available, ask the user to open and foreground Webflow Designer. Do not assume `upload_image_by_url` will remain available.
- **`whtml <img src="...">` does NOT link to the asset library by URL** ("inserted without a managed asset"). After inserting, `query_elements` for the `Image` and `set_image_asset` by asset ID.
- Bind images by asset ID with `set_image_asset`, or create the Image with `data_element_builder` and `set_image_asset` in the same step when possible. Apply an image-fill class (`width:100%; height:100%; object-fit:cover; display:block`) inside the image's container/placeholder.
- **hiDPI/retina:** Webflow's HiDPI checkbox is Designer-UI-only. Equivalent via API: ship a **2× source and let CSS constrain it to its display width** → crisp automatically.
- Delete orphaned `size:0` assets to keep the library clean.

### 7. SVG, logos, icons → use embeds

- **An SVG uploaded as an asset and placed via `<img>` can render as a filled blob** when it has gradients/complex fills. **Inline the SVG inside an `HtmlEmbed`** for crisp, transparent, recolorable vectors.
- **Setting embed code:** create the `HtmlEmbed` (code can't be set at creation), then `data_element_tool set_settings` with key `"code"` and the raw markup as `static_text`.
- To avoid malformed tool-call JSON, single-quote SVG attributes, optimize before transcribing, collapse whitespace, round path coordinates to ~1 decimal, and do one SVG per call. Around 13 KB is usually reliable; 16–20 KB is risky.
- Strip Figma SVG export noise: full-page/canvas backing rects, dashed component-boundary rects, off-target paths, and unused `id` attributes. Keep ids referenced by `url(#...)` gradients/clips and leave `fill="white"` inside `<defs><clipPath>` alone.
- Crop the SVG `viewBox` to the artwork bounds and put `style="height:Npx; width:auto; display:block"` on the root `<svg>` when sizing by height. If the export is too messy, ask the user to paste Figma's cleaner "Copy as SVG" output.
- Regex gotcha when parsing SVG: `id="X"` contains `d="X"` as a substring. Match `\sd="` with a leading boundary, not bare `d="`.
- Dark-background variant: duplicate the SVG and swap wordmark `fill` hex to white (leave `fill="url(#…)"` gradient fills alone).
- **`set_text("")` on a Link wipes its child embeds.** Never clear a link's text after inserting an icon embed (or re-add the embed after).
- For multiple logos of different proportions, **crop each SVG `viewBox` to its content bounds** so you can size them uniformly in a flex row.

### 8. Fonts (`data_fonts_tool`)

- Upload fonts with `data_fonts_tool`: `create_font` (`file_hash` = MD5 of the woff2) → presigned upload → POST the bytes. Source woff2 from the Google Fonts `css2` endpoint (latin subset) with a desktop User-Agent when needed.
- Never add Google Fonts `<link>` tags to page/site `<head>` after uploading fonts; they create duplicate `@font-face` declarations. Reference fonts by **exact family name** in CSS.
- First snapshots can show fallback fonts during the cold-cache `font-display: swap` window. Warm the cache with a throwaway/full-page snapshot and re-snapshot before "fixing" fonts. Do not add head links to solve snapshot-only fallback fonts.
- Variable-font woff2 files can serve multiple weights; registering each weight against the same source file is acceptable.

### 9. Custom code & interactions

- **Prefer component-scoped HtmlEmbeds for component behavior** (e.g., navbar mobile-toggle CSS/JS) so the behavior travels if the element becomes a Webflow component. Create the embed inside the component root, then set code via `data_element_tool set_settings`.
- Use `data_scripts_tool set_site_freeform_code` (head/footer) only for genuinely global `<style>`/`<script>`. The *registered-script* apply endpoints (`add_site_script`/`add_page_script`) may 404 depending on the site; freeform code is reliable.
- **Unused combo classes get stripped from published CSS.** A class you only toggle at runtime via JS (e.g., `.menu.is-open`) has **no matching rule** unless you (a) apply the combo to an element in the Designer, or (b) **guarantee the rule in a head `<style>`**. This silently makes JS toggles do nothing.
- **HTML embed + `<style>`/`<script>` is the escape hatch** for anything Webflow's panel can't express: parent-state→child selectors, custom mobile-menu toggle, or any CSS/JS Webflow strips or can't model.
- **Native components (Navbar, etc.) cannot be created via API/whtml** — whtml just produces generic blocks with `w-*` class names (no real component JS/CSS). Either build a custom equivalent (+ a small delegated-click script) or have the user add the native element in the Designer.

### 10. Navbar (reusable recipe)

Webflow's native Navbar component can't be created via the API/whtml (whtml only yields generic blocks), yet most sites need one. Build a **semantic `<nav>` from Webflow custom elements** + a **CSS-only mobile toggle in a code embed** — no JS, no native component.

**Always ask first:** *which breakpoint should the menu collapse to a hamburger?* Then recommend based on the design, and use their answer as `{BP}`:
- **≤3–4 short links, no/short CTA** → Mobile landscape (**767**) or Mobile portrait (**479**) — they stay readable longer.
- **5+ links, long labels, or a prominent CTA** → Tablet (**991**) — collapse earlier so the bar never crowds.
- State your recommendation with the reason, then defer to their choice.

**Structure** — build with custom tags (`set_tag` / `BY_CUSTOM_TAG`) so it's semantic and Designer-editable:

```html
<nav class="nav">                         ← custom element, tag = nav; position: relative (or sticky/fixed)
  <div class="nav-inner">                 ← flex row, space-between, max-width container
    <a class="nav-brand" href="/">…logo…</a>
    <input type="checkbox" id="nav-toggle" class="nav-cb">   ← custom tag "input", attr type=checkbox
    <label for="nav-toggle" class="nav-burger">              ← custom tag "label", attr for=nav-toggle
      <span class="nav-burger-bar"></span> ×3
    </label>
    <div class="nav-menu">                 ← links + CTA (real, editable Webflow links)
      <a class="nav-link" href="#">…</a> …
      <a class="btn" href="#">CTA</a>
    </div>
  </div>
</nav>
```

**Critical:** the checkbox must be a **previous sibling** of `.nav-menu` (order: brand → checkbox → burger → menu) so `:checked ~ .nav-menu` resolves. Make `.nav` (or `.nav-inner`) `position: relative` so the dropdown anchors to the bar. Use custom-tag `input`/`label` (not the Form Checkbox element) to avoid Webflow's `.w-checkbox` wrapper, which would break the sibling chain.

**Behavior — one code embed, CSS only** (replace `{BP}` with the chosen breakpoint). This CSS uses `:checked ~` + a media query that Webflow's style panel can't express — which is exactly why it lives in an embed:

```html
<style>
  .nav-cb{ position:absolute; width:1px; height:1px; opacity:0; pointer-events:none; }  /* a11y-hidden toggle */
  .nav-burger{ display:none; }                       /* hidden on desktop */
  @media screen and (max-width:{BP}px){
    .nav-burger{ display:flex; flex-direction:column; row-gap:5px; cursor:pointer; }
    .nav-menu{
      display:none; position:absolute; top:100%; left:0; right:0;
      flex-direction:column; align-items:flex-start; row-gap:4px;
      padding:16px 24px; background:#fff; box-shadow:0 10px 24px rgba(0,0,0,.10);
    }
    .nav-cb:checked ~ .nav-menu{ display:flex; }      /* pure-CSS open/close */
  }
</style>
```

Keep all **desktop visual styling** (colors, padding, link/burger-bar look) as normal Webflow classes; the embed holds only the responsive + toggle **behavior**.

**Tradeoffs:** the pure-CSS toggle is zero-JS and publish-safe, but doesn't set `aria-expanded` or close on outside-click. If the client needs those, swap the embed for a small JS toggle (delegated click + class toggle) — but a JS-toggled class needs its open-state rule **guaranteed in custom code** (an unused combo class is stripped from published CSS — see §9). Optionally animate the bars to an "X" via `.nav-cb:checked ~ .nav-burger` rules inside the same embed.

### 11. Isolating experiments / "branching"

- **Page-branching API may be unavailable** (`create_branch`/`list_branches` → 404). Substitute: **`create_page` with `duplicateOf`** to clone the page as an experiment "branch" (gets its own page id; target its elements with that `pageId`). Revert main by deleting the experimental elements.
- For reversible enhancements, **layer the new thing over a static fallback** (e.g., an animated canvas over the static gradient image) rather than replacing it.

### 12. Verification & its hard limits

- `element_snapshot_tool`: Designer-foreground only; **desktop viewport only (no responsive/mobile simulation)**; **does not execute embeds / WebGL / `backdrop-filter`** (those render only on the published/preview site).
- Isolated-section snapshots do not include sibling overlays (e.g., page-level grids/backgrounds). Verify overlays/layering with a full-page composite snapshot of the top-level wrapper.
- Transparent regions render as **black** in isolated snapshots; on the page they show the page background. `position:fixed` elements can render unreliably in composites; verify clearance on preview/live.
- First snapshot of a session can show fallback fonts; warm the cache and re-snapshot before changing font implementation.
- You **cannot fetch `*.webflow.io`** (robots-blocked) or run JS on it. So:
  - If the user chooses to publish to the subdomain, ask them to confirm anything you can't see in the Designer — embed behavior, custom-code, mobile/responsive widths. Never claim an embed is verified from your side.

### 13. Layout patterns worth reusing

- **Background grid lines:** `repeating-linear-gradient` for dashes (control dash/gap precisely — a CSS dashed *border* can't). Give each line element a **real width (≥1px)** so Webflow doesn't flag it as an empty/clickable zero-width element. Place at `z-index:-1` inside a stacking-context wrapper so it sits behind content but above the page background.
- Use `repeating-linear-gradient`, not `border-style:dashed`, for dashed accents/dividers/underlines so dash length, gap, opacity, and direction match the design rhythm.
- Decorative overlays must sit behind content. Make `.page-wrapper` a stacking context (`position:relative; z-index:0`) and place overlays at `z-index:-1`; opaque cards then hide the overlay while gutters show it.
- Never use a fixed overlay width wider than the viewport. Prefer `left:0; right:0; width:auto; max-width:<design-width>; margin-left:auto; margin-right:auto`.
- Replicate interior grid lines too, not just outer edges; check Figma for distributed columns (e.g., 25/50/75%).
- **Perceived weight ≠ literal alpha:** lines *behind* content read lighter than identical lines *in front* (occlusion). Match the perceived weight when pairing them.
- **Section dividers:** use a thin absolutely-positioned gradient-line element to match a dashed grid's rhythm, not a dashed `border`.
- **Fixed vs sticky nav:** `fixed` lets the first section sit *under* the bar (useful when the nav is translucent/overlays content); then add top-padding to that section to clear the bar. `sticky` reserves space (content starts below the bar).
- **Replacing an `<img>` with an embed loses the img's classes/margins** — reapply spacing on the embed.

### 14. Build mechanics & gotchas

- `data_whtml_builder` requires a single root element per action. To insert multiple sibling sections, use multiple actions.
- `set_style` replaces all classes on an element. If a class does not exist yet, create it with `data_style_tool create_style` or define it in the WHTML CSS param so Webflow creates it.
- `query_elements` style filters are case-insensitive substring matches; filter returned elements by exact class/type before acting.
- Responsive work is headless: use `data_style_tool update_style` with breakpoint IDs (`main` base, then `medium`, `small`, `tiny`). Desktop-first: set base, override downward.
- Capture returned element ids from every insert. Re-find later by exact style/type when possible. Element ids are `{component, element}`, where `component` is the page id.
- Combo classes (`["base","modifier"]`) can be ambiguous. When in doubt, prefer one standalone class with full styling.
- Figma component instances often carry repeated placeholder labels (e.g., identical button text). Confirm intended labels with the user instead of copying placeholders verbatim.
- Suppress Designer-only `.wf-empty` affordances on decorative empty elements by giving normal DivBlocks a dimension-giving style in the active breakpoint (explicit zero padding works). For custom-tag empty elements, add a child or use a normal DivBlock instead.

### 15. Reference: local-file upload (presigned S3)

```bash
# 1) Download/export the image locally and compute MD5 of the bytes.
# 2) create_asset returns uploadUrl + uploadDetails (presigned form) + hostedUrl
# 3) POST the bytes (field order: form fields first, file LAST):
curl -s -o /dev/null -w "%{http_code}" -X POST "$UPLOAD_URL" \
  -F "key=$KEY" -F "acl=public-read" -F "Content-Type=image/png" \
  -F "cache-control=max-age=31536000" -F "success_action_status=201" \
  -F "X-Amz-Algorithm=..." -F "X-Amz-Credential=..." -F "X-Amz-Date=..." \
  -F "X-Amz-Signature=$SIG" -F "policy=$POLICY" -F "bucket=..." \
  -F "file=@/path/to/image.png"
# 4) Verify the asset has nonzero size / variants before using its asset ID.
```

> Validate `$POLICY` is pure base64 ASCII before sending: `printf '%s' "$POLICY" | grep -q '[^A-Za-z0-9+/=]' && echo "ABORT: non-ASCII in policy"`.

## Examples

### Example 1: Build a Figma frame into a Webflow page

**User:** "Build this Figma frame in my Webflow site: [figma.com URL]"

1. Use Figma MCP to gather metadata, design context, variables, screenshots, and export URLs for the requested frame.
2. Use Webflow MCP to call `webflow_guide_tool`, confirm the user/site/page, and inspect existing styles.
3. Ask whether to use Designer Bridge during the build or build headless first; explain the bridge is recommended for visual feedback but requires the Designer tab open and foregrounded.
4. Ask how to handle Webflow variables, whether to use FlowKit naming / existing class patterns / semantic names, and whether to use `px`, `rem`, or `em` units.
5. Ask about ambiguous design intent and navbar collapse breakpoint if relevant.
6. Confirm the build gates: Designer link/foreground tab if using bridge, SVG embeds for vector marks, 2× raster sources where needed, and gradient-based dashed accents.
7. Set up or map variables according to the selected design-system strategy, build foundations and sections via `data_whtml_builder`, attach assets by Webflow asset ID, verify each section, then ask whether they want to publish to the `.webflow.io` subdomain. Default to no.

### Example 2: Recreate a Figma section in an existing Webflow page

**User:** "Recreate this pricing section from Figma on my homepage."

1. Extract the section's Figma tokens, assets, and reference code.
2. Confirm the target Webflow site/page. Designer connection is only needed later for snapshot/visual QA or bridge-gated fallbacks.
3. Confirm build mode plus variable, naming, and unit strategy before generating new Webflow classes/CSS; default to Designer Bridge, existing variables plus missing variables, FlowKit, and `px` if the user has no preference.
4. Present a concise preview plan that calls out the non-negotiable build gates, then require explicit confirmation before creating elements.
5. Insert one section, constrain confirmed 2× images to display size, verify structurally headless or visually with bridge snapshots if selected, and ask the user to confirm any embed or responsive behavior that cannot be self-verified.

## Guidelines

- Always use Figma MCP for design extraction and Webflow MCP for Webflow operations; never use direct Webflow API calls.
- Call `webflow_guide_tool` before other Webflow tools in the workflow.
- Ask for build mode, Webflow variable, style naming, and CSS unit strategy before creating classes. Default to Designer Bridge, existing variables plus missing variables, FlowKit naming, and `px`; reference `webflow-mcp:flowkit-naming` when FlowKit is selected.
- Treat mutating Webflow operations as confirmation-gated. Require explicit user approval before creating, updating, publishing, or deleting.
- Prefer `data_whtml_builder` for section construction, then use element tools for precise asset binding, embeds, and refinements.
- Keep CSS Webflow-compatible: longhand properties, class selectors, desktop-first breakpoints, flexbox-first layout, and custom code for unsupported behavior.
- Do not publish by default. If the user wants a live review link, publish to the `.webflow.io` subdomain before any custom domains.

## Checklist before declaring done

- [ ] All CSS longhand; correct breakpoints; flexbox-first.
- [ ] Build mode followed: bridge-assisted by default with Designer tab open and foregrounded, or headless-first if the user chose it.
- [ ] Webflow variables handled according to the selected strategy; repeated colors/type/spacing/radii are mapped or created unless hard-coding was explicitly selected.
- [ ] Images attached by asset ID (not orphan `<img src>`); 2× source confirmed where crispness matters.
- [ ] Vector marks are clean inline-SVG embeds (backgrounds stripped), or user explicitly approved raster fallback.
- [ ] Dashed accents/dividers/grids use `repeating-linear-gradient`, not `border-style:dashed`, unless user explicitly approved browser-default dashes.
- [ ] Fonts uploaded + referenced by exact family name; temp `<head>` link removed.
- [ ] Runtime-toggled classes have guaranteed CSS (not stripped).
- [ ] Responsive overrides at medium/small/tiny.
- [ ] If published to subdomain, user asked to confirm anything you can't self-verify (embeds, WebGL, blur, mobile).
