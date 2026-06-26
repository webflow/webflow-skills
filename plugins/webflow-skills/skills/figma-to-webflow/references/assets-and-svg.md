# Assets, SVG, And Fonts

Read this before exporting, uploading, or placing images, SVGs, logos, icons, or fonts.

## Figma Extraction

- Pull `get_metadata`, `get_design_context`, and `get_variable_defs` early.
- Asset URLs from design context live about 7 days; screenshot URLs are short-lived. Download promptly.
- Read the page/canvas background color from Figma. Do not assume white.
- For composed mockups or complex product visuals, export the parent node at 2x with `download_assets` and treat it as one image instead of rebuilding every layer.

## Raster Images

- Use the headless Data API asset path first. Do not build around `asset_tool upload_image_by_url`; it is Designer Bridge-gated and may be removed.
- Download image bytes locally from the Figma export/design-context URL.
- Compute MD5 of the actual bytes.
- Call `data_assets_tool create_asset` with `site_id`, `file_name`, and `file_hash`.
- POST bytes to the returned presigned S3 form: form fields first, file field last.
- Validate the presigned `policy` is pure base64 ASCII before POSTing:

```bash
printf '%s' "$POLICY" | grep -q '[^A-Za-z0-9+/=]' && echo "ABORT: non-ASCII in policy"
```

- Verify the created asset has nonzero size/variants before placing it. If it remains `size:0` or has no variants, report that Webflow accepted the upload but has not processed a renderable asset.
- Bind images by asset ID with `set_image_asset`, or create the Image with `data_element_builder` and `set_image_asset`.
- Never rely on raw WHTML `<img src="...">`; it is inserted without a managed Webflow asset.
- Apply an image-fill class to images inside placeholders: `width:100%; height:100%; object-fit:cover; display:block`.
- For crisp display, ship a 2x source and constrain it to display size with CSS. Do not depend on the Designer-only HiDPI checkbox.
- Delete orphaned `size:0` assets when safe.

## Inline SVG Embeds

- Logos, icons, and marks must be inline SVG inside `HtmlEmbed`, not uploaded SVG assets in `<img>`, unless the user explicitly approves fallback.
- Gradient/complex SVGs placed as `<img>` can render as a filled blob; inline embed avoids that.
- Prefer Figma right-click **Copy as SVG** for logos/marks/icons; it usually gives clean artwork with tight bounds. Use MCP `download_assets` / design-context SVG export only when clipboard output is unavailable, and expect scaffolding to strip.
- Create the `HtmlEmbed` first, then set code via `data_element_tool set_settings` with key `"code"` as `static_text`.
- Pass the SVG as the literal `static_text.value` of the `code` setting and let the tool layer encode it. Do not hand-build, pre-escape, or wrap the arguments in a raw/blob form. If you get "could not be parsed as JSON," the tool call is malformed; fix the call shape, do not shrink the SVG.
- There is no ~13 KB per-SVG `set_settings` ceiling; 20 KB can pass as a string value. The real practical limit is Webflow Designer's HTML Embed UI, about 10,000 characters. Data API embeds over ~10k can render, but they are not safely hand-editable in Designer and may be truncated if opened/re-saved. If the embed must remain Designer-editable, reduce it below ~10k.
- Optimize only as needed:
  - Single-quote SVG attributes.
  - Collapse whitespace between tags.
  - Hoist shared fill to the root `<svg>` where possible.
  - Keep vectorized wordmark text as paths; never substitute live text for logo text unless the user explicitly wants editable text.
  - Never round coordinates to integers; it destroys curves on small artwork. One decimal is the floor, and only round if needed to fit the ~10k Designer-editable limit.
- Clean MCP/Figma SVG exports:
  - Strip full-canvas backing `<rect>` elements by oversized dimensions, not just fill; some inherit the root fill and render as a giant dark box.
  - Strip page-fill `<path>` elements, often `#F4F1FD` or `#F3F5F7`.
  - Strip dashed component-boundary `<rect stroke="#9747FF" stroke-dasharray=...>`.
  - Strip nested wrapper `<g id>` elements when not needed.
  - Strip `<defs><clipPath>` scaffolding only when no kept artwork references it.
  - Remove off-target paths and unused `id` attributes.
  - Keep ids referenced by `url(#...)` gradients/clips.
  - Leave `fill="white"` inside kept `<defs><clipPath>` alone; those are masks.
- Verify id integrity after cleanup: every `url(#id)` must resolve to a kept element. If embedding the same SVG more than once on a page, suffix gradient/clip ids uniquely per instance and update every `url(#...)` reference, because duplicate ids resolve to the first match.
- Export the artwork node, not its parent frame. Frame exports pad the `viewBox` with empty space so height-based sizing renders tiny artwork. Crop the `viewBox` to ink/artwork bounds; for height-based sizing, put `style="height:Npx; width:auto; display:block"` on the root `<svg>`.
- Regex gotcha: `id="X"` contains `d="X"` as a substring. Match `\sd="`, not bare `d="`.
- Replacing an `<img>` with an embed loses the image's classes/margins; reapply spacing on the embed.
- Never call `set_text("")` on a Link that contains icon embeds; it can wipe child embeds.

## Fonts

- Upload fonts with `data_fonts_tool`: `create_font` with MD5 `file_hash`, then presigned upload.
- Source woff2 from Google Fonts `css2` latin endpoint with a desktop User-Agent when needed.
- Never add Google Fonts `<link>` tags to page/site head after uploading fonts; they create duplicate `@font-face` declarations.
- Reference fonts by exact family name.
- First snapshots can show fallback fonts during cold-cache `font-display: swap`. Warm the cache with a throwaway/full-page snapshot and re-snapshot before changing font implementation.
- Variable-font woff2 files can serve multiple weights; registering each weight against the same source file is acceptable.
