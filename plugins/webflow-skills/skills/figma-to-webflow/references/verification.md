# Verification And Responsive QA

Read this before responsive work, visual QA, snapshots, or publish/review.

## Responsive

- Responsive work is headless: use `data_style_tool update_style` with breakpoint ids.
  - `main`: base desktop
  - `medium`: 991px and below
  - `small`: 767px and below
  - `tiny`: 479px and below
- Desktop-first: set base, then override downward.
- Use structural verification between visual checks: `query_elements`, `query_styles`, exact class/type filtering.

## Designer Bridge And Snapshots

- `element_snapshot_tool` requires Designer tab open and foregrounded.
- Snapshots are desktop viewport only. They do not simulate responsive/mobile.
- Snapshots do not execute embeds, WebGL, `backdrop-filter`, or custom code behavior.
- If a snapshot or `designer_tool` returns `status:false`, the bridge is likely disconnected, backgrounded, idle, or cold. Ask the user to foreground the Designer tab and retry.
- Large composites can fail transiently when bridge is cold or page is very tall; retry before assuming the build is broken.

## Snapshot Traps

- Isolated-section snapshots do not include sibling overlays such as page-level grids/backgrounds. Verify overlays/layering with a full-page composite of the top-level wrapper.
- Transparent regions render as black in isolated snapshots. On the page, the page background shows through.
- `position:fixed` elements can render unreliably in composites. Confirm fixed-element clearance in preview/live.
- First snapshot of a session can show fallback fonts because uploaded fonts load asynchronously. Warm cache with a throwaway/full-page snapshot and re-snapshot before changing font implementation.

## Structural Gotchas

- Page branching APIs may be unavailable (`create_branch` / `list_branches` can 404). Substitute `create_page` with `duplicateOf` to clone a page as an experiment.
- For reversible enhancements, layer the new thing over a static fallback rather than replacing it.
- Figma component instances often carry repeated default labels. Confirm intended labels with the user.

## Publish

- Do not publish by default.
- If the user wants a review link, publish to `.webflow.io` before any custom domain.
- You cannot fetch `*.webflow.io` from the agent because it is robots-blocked. Ask the user to confirm:
  - embed behavior
  - custom code
  - blur/backdrop effects
  - WebGL/canvas
  - animation
  - mobile/responsive widths
- Never claim those behaviors are verified from your side.
