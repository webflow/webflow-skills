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
| **Data API** (headless) | pages, sites, scripts, fonts, asset *metadata*, publish | No |
| **Designer Bridge** | image upload, element create/edit/move/query, snapshots, styles | **Yes — Designer tab open AND foregrounded** |

- Call `webflow_guide_tool` once before other Webflow tools. Confirm auth/site with `whoami` + `get_site`.
- If a Designer tool returns "Unable to connect to Webflow Designer," share the launch link and ask the user to open the Designer **and keep that browser tab in the foreground** — it idles/disconnects when backgrounded. Snapshots especially fail (`status:false`) when unfocused; retry before assuming anything broke.

### 1. Workflow order

1. **Gather** — Figma structure, tokens, per-section code/colors/assets; Webflow site, pages, existing styles.
2. **Choose style preferences** — ask how Webflow variables, new styles, and CSS units should be handled before creating any classes/CSS (see §3).
3. **Set up foundations** — Webflow variables/design tokens, page wrapper w/ base typography, and fonts.
4. **Build section by section** via `data_whtml_builder` (capture each returned element id to nest the next piece). Verify after each.
5. **Attach assets** (images by ID; inline SVGs via embeds).
6. **Responsive pass** (desktop-first overrides).
7. **Custom code / interactions** last (mobile menu, animated backgrounds, blur).
8. **Offer review/publish next steps** — default to **no publish**. Only publish to the `.webflow.io` subdomain if the user explicitly asks or confirms after reviewing the build.

Confirm ambiguous design intent up front (e.g., a button whose label is a repeated component placeholder) rather than guessing. **If the build includes a navbar, ask which breakpoint the mobile menu should collapse at before building it (see §10).**

### 2. Extracting from Figma

- `get_metadata` → node/structure map. `get_design_context` per node → reference code + exact colors + asset download URLs + a screenshot. `get_variable_defs` → design tokens (colors, type scale, spacing, radii). Pull tokens early and treat them as law.
- **Asset URLs from design-context live ~7 days; `get_screenshot` URLs are short-lived** — upload promptly.
- **Vector assets (logos, icons, marks): use `download_assets` with `defaultFormat: "svg"`** — NOT `get_screenshot`. Screenshot only rasterizes and **never upscales past the node's native size** (so it can't give you 2×, and it bakes in surrounding background).
  - **Gotcha:** the SVG export wraps the node in its ancestor chain and **bakes in background fills** clipped to the node box (page background rect, card background, a node "backing" rect). Strip the full-bleed background `<rect>`/`<path>` elements that aren't part of the target → clean transparent vector. (Remaining `fill="white"` inside `<defs><clipPath>` are just clip masks — leave them.)
- **Raster (photos, complex product mockups): can't get 2× from `get_screenshot`.** Use the design-context layer export URLs (often already 2×) or composite the 2× image locally, then upload (see §5, §6).

### 3. Style preferences

Before creating Webflow variables, classes, or CSS, ask about design-system strategy, naming, and units.

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
- **Bridge-gated fallback:** if processed variants are required and `create_asset` does not process them, ask the user to open and foreground Webflow Designer before using any bridge-gated asset processing fallback. Do not assume `upload_image_by_url` will remain available.
- **`whtml <img src="...">` does NOT link to the asset library by URL** ("inserted without a managed asset"). After inserting, `query_elements` for the `Image` and `set_image_asset` by asset ID.
- **hiDPI/retina:** Webflow's HiDPI checkbox is Designer-UI-only. Equivalent via API: ship a **2× source and let CSS constrain it to its display width** → crisp automatically.
- Delete orphaned `size:0` assets to keep the library clean.

### 7. SVG, logos, icons → use embeds

- **An SVG uploaded as an asset and placed via `<img>` can render as a filled blob** when it has gradients/complex fills. **Inline the SVG inside an `HtmlEmbed`** for crisp, transparent, recolorable vectors.
- **Setting embed code:** create the `HtmlEmbed` (code can't be set at creation), then `data_element_tool set_settings` with key `"code"` and the raw markup as `static_text`.
- Dark-background variant: duplicate the SVG and swap wordmark `fill` hex to white (leave `fill="url(#…)"` gradient fills alone).
- **`set_text("")` on a Link wipes its child embeds.** Never clear a link's text after inserting an icon embed (or re-add the embed after).
- For multiple logos of different proportions, **crop each SVG `viewBox` to its content bounds** so you can size them uniformly in a flex row.

### 8. Fonts (`data_fonts_tool`)

- `create_font` (`file_hash` = MD5 of the woff2) → presigned upload → POST the bytes. Source woff2 from the Google Fonts `css2` endpoint (latin subset) with a desktop User-Agent.
- Custom fonts resolve by **exact family name** referenced in your CSS once published — then you can remove any temporary Google Fonts `<head>` link.

### 9. Custom code & interactions

- **Prefer `data_scripts_tool set_site_freeform_code` (head/footer) for `<style>`/`<script>`.** The *registered-script* apply endpoints (`add_site_script`/`add_page_script`) may 404 depending on the site; freeform code is reliable.
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

- `element_snapshot_tool`: Designer-foreground only; **desktop viewport only (no responsive/mobile simulation)**; **does not execute embeds / WebGL / `backdrop-filter`** (those render only on the published/preview site). An isolated-section snapshot renders transparent areas as **black** — not a bug.
- You **cannot fetch `*.webflow.io`** (robots-blocked) or run JS on it. So:
  - If the user chooses to publish to the subdomain, ask them to confirm anything you can't see in the Designer — embed behavior, custom-code, mobile/responsive widths. Never claim an embed is verified from your side.

### 13. Layout patterns worth reusing

- **Background grid lines:** `repeating-linear-gradient` for dashes (control dash/gap precisely — a CSS dashed *border* can't). Give each line element a **real width (≥1px)** so Webflow doesn't flag it as an empty/clickable zero-width element. Place at `z-index:-1` inside a stacking-context wrapper so it sits behind content but above the page background.
- **Perceived weight ≠ literal alpha:** lines *behind* content read lighter than identical lines *in front* (occlusion). Match the perceived weight when pairing them.
- **Section dividers:** use a thin absolutely-positioned gradient-line element to match a dashed grid's rhythm, not a dashed `border`.
- **Fixed vs sticky nav:** `fixed` lets the first section sit *under* the bar (useful when the nav is translucent/overlays content); then add top-padding to that section to clear the bar. `sticky` reserves space (content starts below the bar).
- **Replacing an `<img>` with an embed loses the img's classes/margins** — reapply spacing on the embed.

### 14. Reference: local-file upload (presigned S3)

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
3. Ask how to handle Webflow variables, whether to use FlowKit naming / existing class patterns / semantic names, and whether to use `px`, `rem`, or `em` units.
4. Ask about ambiguous design intent and navbar collapse breakpoint if relevant.
5. Set up or map variables according to the selected design-system strategy, build foundations and sections via `data_whtml_builder`, attach assets by Webflow asset ID, verify each section, then ask whether they want to publish to the `.webflow.io` subdomain. Default to no.

### Example 2: Recreate a Figma section in an existing Webflow page

**User:** "Recreate this pricing section from Figma on my homepage."

1. Extract the section's Figma tokens, assets, and reference code.
2. Confirm the target Webflow site/page and Designer connection.
3. Confirm variable, naming, and unit strategy before generating new Webflow classes/CSS; default to existing variables plus missing variables, FlowKit, and `px` if the user has no preference.
4. Present a concise preview plan and require explicit confirmation before creating elements.
5. Insert one section, constrain images with 2× sources where needed, verify with Designer snapshots, and ask the user to confirm any embed or responsive behavior that cannot be self-verified.

## Guidelines

- Always use Figma MCP for design extraction and Webflow MCP for Webflow operations; never use direct Webflow API calls.
- Call `webflow_guide_tool` before other Webflow tools in the workflow.
- Ask for Webflow variable, style naming, and CSS unit strategy before creating classes. Default to existing variables plus missing variables, FlowKit naming, and `px`; reference `webflow-mcp:flowkit-naming` when FlowKit is selected.
- Treat mutating Webflow operations as confirmation-gated. Require explicit user approval before creating, updating, publishing, or deleting.
- Prefer `data_whtml_builder` for section construction, then use element tools for precise asset binding, embeds, and refinements.
- Keep CSS Webflow-compatible: longhand properties, class selectors, desktop-first breakpoints, flexbox-first layout, and custom code for unsupported behavior.
- Do not publish by default. If the user wants a live review link, publish to the `.webflow.io` subdomain before any custom domains.

## Checklist before declaring done

- [ ] All CSS longhand; correct breakpoints; flexbox-first.
- [ ] Webflow variables handled according to the selected strategy; repeated colors/type/spacing/radii are mapped or created unless hard-coding was explicitly selected.
- [ ] Images attached by asset ID (not orphan `<img src>`); 2× where crispness matters.
- [ ] Vector marks are clean inline-SVG embeds (backgrounds stripped).
- [ ] Fonts uploaded + referenced by exact family name; temp `<head>` link removed.
- [ ] Runtime-toggled classes have guaranteed CSS (not stripped).
- [ ] Responsive overrides at medium/small/tiny.
- [ ] If published to subdomain, user asked to confirm anything you can't self-verify (embeds, WebGL, blur, mobile).
