# Export Templates

## Markdown

```markdown
# Site Audit: [Site Name]
## Site Information
- ID: [site-id]
- Last Published: [date]
## Pages
### Static Pages
- Home (/)
### CMS Templates
- Blog Post (/post/[slug])
## Collections
### Blog Posts (47 items)
- Title (PlainText, required)
- Slug (PlainText, required)
- Content (RichText)
```

## JSON

```json
{
  "site": { "id": "...", "name": "...", "lastPublished": "..." },
  "pages": [],
  "collections": []
}
```

## CSV

Generate separate files:
- `pages.csv` — all pages with slug, type, SEO status
- `collections.csv` — collection name, slug, item count, field count
- `fields.csv` — all fields across collections with type and constraints
