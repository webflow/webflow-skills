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
- Create the `HtmlEmbed` first, then set code via `data_element_tool set_settings` with key `"code"` and the raw markup as `static_text`. Do not rely on setting embed code at element creation.
- To avoid malformed tool-call JSON:
  - Single-quote SVG attributes.
  - Collapse whitespace between tags.
  - Round path coordinates to about 1 decimal.
  - Hoist shared fill to the root `<svg>` where possible.
  - Do one SVG per tool call. Around 13 KB is usually reliable; 16-20 KB is risky.
- Clean Figma SVG exports:
  - Strip full-page/canvas backing rects.
  - Strip dashed component-boundary rects.
  - Remove off-target paths and unused `id` attributes.
  - Keep ids referenced by `url(#...)` gradients/clips.
  - Leave `fill="white"` inside `<defs><clipPath>` alone; those are masks.
- Crop the `viewBox` to artwork bounds. For height-based sizing, put `style="height:Npx; width:auto; display:block"` on the root `<svg>`.
- If `download_assets` output is too noisy, ask the user to paste Figma's cleaner "Copy as SVG" output.
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
