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
- Structural verification is not enough to call a build done. It can prove elements/classes exist, but not that the rendered layout is correct.

## Designer Bridge And Snapshots

- `element_snapshot_tool` requires Designer tab open and foregrounded.
- Snapshots are desktop viewport only. They do not simulate responsive/mobile.
- Snapshots do not execute embeds, WebGL, `backdrop-filter`, or custom code behavior.
- If a snapshot or `designer_tool` returns `status:false`, the bridge is likely disconnected, backgrounded, idle, or cold. Provide the Designer launch link (opens Designer with the MCP Bridge App), ask the user to open it and keep that tab foregrounded, then retry.
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
- Before saying a capability "can't" be done, test the relevant MCP tool path. If you cannot test, say it is untested and be precise about whether the limitation is Webflow itself, the MCP API, or the current tool surface.
- Avoid broad tag/global style tests on real pages. If testing a risky capability, use an isolated duplicate page or disposable element and revert immediately.
- After WHTML insertion, verify that expected classes survived and resolve to existing Webflow styles. Missing styles can leave rendered content unstyled even when the DOM exists.

## Done Criteria

- Do not call the build done until rendered output is visually checked with Designer Bridge, preview, or explicit user confirmation.
- If visual verification is blocked, report exactly what is unverified and ask the user to check it.

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
