---
name: site-audit
description: "Audit a Webflow site via MCP — counts pages, catalogs CMS collection schemas, detects missing SEO metadata, scores content health 0-100, and exports inventory as Markdown/JSON/CSV. Use when a user asks for a Webflow audit, site review, content inventory, site health check, or migration planning."
---

# Site Audit

Comprehensive audit of a Webflow site's structure, content health, and quality with detailed analysis and multiple export formats.

## MCP Tool Reference

All operations MUST use Webflow MCP tools — no other tools or methods. Every call requires a `context` parameter (15-25 words, third-person).

| Action | Tool | MCP Action |
|--------|------|------------|
| List sites | `data_sites_tool` | `list_sites` |
| Get site details | `data_sites_tool` | `get_site` |
| List pages | `data_pages_tool` | `list_pages` |
| List collections | `data_cms_tool` | `get_collection_list` |
| Get collection schema | `data_cms_tool` | `get_collection_details` |
| Count collection items | `data_cms_tool` | `list_collection_items` |
| Get best practices | `webflow_guide_tool` | — |

## Instructions

### Phase 1: Site Selection & Discovery
1. **Get site**: Identify the target site. If user does not provide site ID, ask for it.
2. **Fetch site details** via `data_sites_tool` → `get_site` to retrieve:
   - Site name and ID
   - Last published date
   - Last updated date
   - Timezone
   - Locales (primary and secondary)
   - Custom domains
3. **Ask user preferences**: Ask what level of detail they want:
   - Quick summary (counts only)
   - Standard inventory (pages + collections + counts)
   - Detailed inventory (includes all field schemas, item samples, SEO data)
   - Full export (everything + export to file format)

**Checkpoint:** Confirm site ID resolved and detail level chosen before proceeding.

### Phase 2: Pages Inventory
4. **List all pages** via `data_pages_tool` → `list_pages`
5. **Categorize pages**:
   - Static pages (no collectionId)
   - CMS template pages (has collectionId)
   - Archived pages
   - Draft pages
6. **Analyze page structure**:
   - Count pages by type
   - Identify pages missing SEO metadata
   - Detect orphaned pages (no navigation links)
   - Check for duplicate slugs

**Checkpoint:** If `list_pages` fails, log the error and continue to Phase 3.

### Phase 3: CMS Collections Inventory
7. **List all collections** via `data_cms_tool` → `get_collection_list`
8. **For each collection**:
   - Get schema via `get_collection_details`
   - Count items via `list_collection_items`
   - Analyze field types and requirements
   - Identify required vs optional fields
   - Detect reference fields and relationships
9. **Collection analysis**:
   - Empty collections (0 items)
   - Unused collections (no template page)
   - Large collections (100+ items)
   - Collections with missing required fields

**Checkpoint:** If `get_collection_details` fails for a collection, show basic info and continue.

### Phase 4: Analysis & Insights
10. **Generate insights**:
    - Total content count (pages + items)
    - Content health score
    - SEO readiness
    - Recommended improvements
11. **Identify issues**:
    - Missing SEO metadata
    - Empty collections
    - Orphaned pages
    - Draft content ratio
12. **Show relationships**:
    - Which pages use which collections
    - Reference field connections
    - Content dependencies

### Phase 5: Export & Formatting
13. **Ask export format** (if user wants full export):
    - Markdown (readable, great for documentation)
    - JSON (machine-readable, for migrations)
    - CSV (spreadsheet-friendly, for analysis)
    - Text summary (console output only)
14. **Generate report** in requested format. See [export-templates.md](references/export-templates.md) for format structure.
15. **Provide actionable insights**: Suggest next steps based on findings

## Examples

**User prompt:**
```
Give me a complete inventory of my site.
```

**Step 1: Initial Report (Standard Inventory)**
```
📊 Site Audit: MCP Demo#1

**Site Details:**
- Site ID: 6924868ede9d3fbbc3195eb0
- Last published: January 9, 2026
- Last updated: January 9, 2026
- Timezone: Asia/Calcutta
- Primary locale: English (en)

---

**Pages (2 total):**

Static Pages (1):
├── Home (/)

CMS Template Pages (1):
└── Blog Posts Template (/post)
    - Collection: Blog Posts

---

**CMS Collections (1):**

Blog Posts (9 items)
├── Slug: post
├── Fields (8):
│   ├── Name (PlainText, required)
│   ├── Slug (PlainText, required)
│   ├── Post Body (RichText)
│   ├── Post Summary (PlainText)
│   ├── Main Image (Image)
│   ├── Thumbnail image (Image)
│   ├── Featured? (Switch)
│   └── Color (Color)

---

**Summary:**
- ✅ 2 pages (1 static, 1 CMS template)
- ✅ 1 CMS collection with 9 published items
- ✅ Site fully published and up-to-date

Would you like a detailed analysis or export in a specific format?
```

**Step 2: Detailed Analysis (when user requests)**
```
🔍 Detailed Analysis: MCP Demo#1

**Content Health Score: 85/100**

✅ Strengths:
- All collections have items (no empty collections)
- All pages are published (no drafts)
- Site recently published (Jan 9, 2026)
- Consistent field structure in Blog Posts

⚠️ Areas for Improvement:
- No SEO metadata on template page (missing meta description)
- Limited page count (consider adding About, Contact pages)
- No reference fields (could link categories/authors to posts)

💡 Recommendations:
1. Add meta descriptions to all pages for better SEO
2. Consider creating a Categories collection for post organization
3. Add an Authors collection for multi-author blog support
4. Create navigation pages (About, Contact, Privacy Policy)

**Collection Breakdown:**

Blog Posts:
- 9 published items (0 drafts, 0 archived)
- 5 featured posts (56%)
- All required fields populated ✓
- Field usage:
  - Name: 100% (9/9)
  - Slug: 100% (9/9)
  - Post Body: 100% (9/9)
  - Post Summary: 100% (9/9)
  - Main Image: 100% (9/9)
  - Thumbnail: 100% (9/9)
  - Featured: 100% (9/9)
  - Color: 100% (9/9)

**Sample Items:**
1. "Why Webflow is the Best Choice for 2026" (featured)
2. "Top Webflow Features to Look Forward to in 2026"
3. "Webflow vs. Competitors: Who Will Win in 2026?" (featured)

---

Export this inventory? (markdown/json/csv/no)
```

## Guidelines

### Health Scoring Formula (0-100)

Start at 100 and deduct for issues found:
- −5 per page missing meta description (max −25)
- −10 per empty collection
- −5 per unused collection with no template page
- −3 per draft page (max −15)
- −10 if site not published in last 90 days
- −5 if no reference fields exist across all collections

Categorize issues: 🔴 Critical (missing required fields, duplicate slugs) | ⚠️ Warning (empty collections, missing SEO) | 💡 Suggestion (add pages, create relationships).

### Operational Guidelines

- **Read-only**: No confirmation needed. Safe to run repeatedly with no side effects.
- **Graceful degradation**: If any MCP call fails, report what succeeded and continue. Offer to retry failed operations.
- **Pagination**: For 20+ collections show progress; for 100+ item collections paginate counts. Only fetch detailed schemas at Detailed/Export level. Limit item samples to 3-5 per collection.
- **Version tracking**: If user runs audit multiple times, compare with previous run and highlight changes.
