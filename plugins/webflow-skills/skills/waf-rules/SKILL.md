---
name: webflow-mcp:waf-rules
description: Review and change a Webflow site's Web Application Firewall (WAF) rules through Webflow MCP. Use when the user wants to block or allow countries, IP addresses or CIDR ranges, networks (ASNs), bots, AI crawlers, scrapers, or User-Agents, optionally only on some paths; add, edit, or remove firewall or WAF rules; or review or explain the current rules. Every change is validated, previewed, and confirmed by the user before it reaches live traffic. Needs an Enterprise plan that includes WAF, and WAF MCP must be enabled for the workspace.
---

# WAF Rules

Review and change the Web Application Firewall (WAF) rules Webflow enforces on a site's connected custom domains. Rule changes reach live traffic without a site publish and can lock out real visitors, so every change is validated, previewed, and confirmed by the user first.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**
- Use Webflow MCP's `webflow_guide_tool` before any other tool call
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to find the site
- Use Webflow MCP's `data_enterprise_tool` with these WAF actions. Each takes `site_id`.
  - `get_waf_rules`: current rules per domain and the `siteStateHash`
  - `validate_waf_rule`: checks a candidate config and explains it in plain language. Changes nothing.
  - `test_waf_rules`: previews an update or deletion and returns a `previewToken`. Changes nothing.
  - `update_waf_rule`, `delete_waf_rule`: write the live firewall
  - `suggest_waf_changes`: proposes rule changes and applies none. Read-only.
- DO NOT call the Webflow API directly or use any other tool to change WAF rules
- Include the `context` parameter when the tool schema asks for it (15-25 words, third-person perspective)

## Before You Start

The API refuses a call by name when one of these is missing (see Errors):

- **Enterprise plan:** WAF MCP needs an Enterprise plan that includes WAF.
- **WAF MCP enabled for the workspace:** WAF MCP is rolling out, so if `data_enterprise_tool` doesn't list the WAF actions, or a call returns `waf_mcp_not_enabled`, it isn't enabled for the workspace yet. Tell the user. They can still manage rules in the Dashboard under Site settings > Security.
- **Role:** the user must be able to manage the site's custom domains: Site manager, Designer, Limited designer, or a custom role with that permission. Designer (needs approval), Marketer, Content editor, and Reviewer can't.
- **Scopes:** `site_config:read` for reads and `validate_waf_rule`, `site_config:write` for `test_waf_rules`, `update_waf_rule`, and `delete_waf_rule`. The Webflow MCP app requests both. If a call returns `missing_scopes`, the user has to reauthorize the connection.

## Instructions

### Phase 1: Read the current rules

1. Call `webflow_guide_tool`. When WAF MCP is enabled, it includes a WAF section.
2. Resolve the site with `list_sites`. If the user didn't name one, or the name matches several, ask.
3. Call `get_waf_rules` and keep:
   - `byDomain`: each connected custom domain's config, or `null` when it has none. A config holds up to four rule types (`ipRules`, `geoRules`, `asnRules`, `userAgentRules`) plus the bot bypass settings.
   - `uniform`: true when every domain has the same config. `rules` then holds it.
   - `hostnamesSkipped`: connected domains WAF can't apply rules to yet.
   - `siteStateHash`: `test_waf_rules`, `update_waf_rule`, and `delete_waf_rule` require it as `expectedSiteStateHash`. Read again before each change; a hash from an earlier read is refused with `WafSiteStateChanged`.
4. If the user asked for a review or an explanation, follow "Reviewing rules" and stop. A review doesn't authorize a change.

### Phase 2: Build and validate the change

5. Change one rule type at a time. An update replaces that rule type's **entire** config on its target domains, and any entry left out is removed. Copy the current config from `byDomain[domain][ruleType]`, apply the user's edit, and keep every other entry in its order. Leave `bypassVerifiedBots` and `bypassAuthorizedBots` out: they're settings, not part of a rule type.
6. Choose the scope (see "Domain scope"): site-wide when the change is for every domain and they share the current config, otherwise `domains` plus `previousDomains`.
7. Call `validate_waf_rule` with `ruleType`, `config`, and the `domains` and `previousDomains` you plan to use. It's read-only and needs no hash, so call it as often as needed.
   - `success: false` with `ValidationError`: fix the config from `error.details` (field path and message) and `error.schema` (the JSON Schema for the rule type, present when the shape itself is wrong). Cross-field user-agent rules appear only in `details`. Validate again. If an entry that's already live is what fails (older rules can predate today's checks), tell the user instead of dropping or rewriting it silently.
   - `success: true`: read every `explanation` line and check it against what the user asked for. If it describes anything they didn't ask for, such as "blocks every other country", fix the config or ask. Use the normalized `config` it returns from here on.
   - Non-empty `riskFindings`: tell the user now that applying will need a second confirmation (see "High-risk changes"), and offer `paths` to narrow the rule.
8. If the request spans several rule types, make one change per rule type, in sequence. You can validate them all and confirm them together, but re-read and test each one right before applying it: every apply changes the `siteStateHash`.

### Phase 3: Preview and confirm

9. Call `test_waf_rules` with the same `ruleType`, `config`, `domains`, and `previousDomains`, plus `expectedSiteStateHash` from your latest `get_waf_rules`.
10. Show the user a preview: rule type and scope, current and new entries, which domains change (`targets[].changed`), each `riskFindings` message, any `hostnamesSkipped`, and size headroom when `candidateBytes` is close to `candidateBytesLimit`. The test checks configuration, not traffic, so it can't say which visitors will be blocked.
11. Ask the user to type `confirm`. "Yes" or "ok" isn't enough. The `previewToken` expires at `expiresAt`, about 5 minutes after the test. If it lapses, test again, and show the preview again if the targets or risks changed.

### Phase 4: Apply and verify

12. Call `update_waf_rule` with exactly the tested `ruleType`, `config`, `domains`, and `previousDomains`, the same `expectedSiteStateHash`, and the `previewToken`.
13. On `HighRiskWafChange`, follow "High-risk changes". On any other `success: false`, see "Errors".
14. On success, report `hostnamesApplied`, `hostnamesCleared` (domain-scoped updates), and any `hostnamesSkipped`. Then call `get_waf_rules` and check that each target domain has the new config.

### Deleting a rule type

1. Call `test_waf_rules` with `operation: "delete"`, `ruleType`, optional `domains`, and `expectedSiteStateHash`. Don't send `config` or `previousDomains`.
2. Show which domains lose the rule type and ask for `confirm`.
3. Call `delete_waf_rule` with the same `ruleType` and `domains`, `expectedSiteStateHash`, and the `previewToken`. Other rule types and settings stay. Report `hostnamesCleared`.

To remove the last entry from `ips`, `countryList`, or `asnList`, delete the rule type: those lists can't be empty.

### Applying without a preview

`directApply: true` on `update_waf_rule` or `delete_waf_rule` skips `test_waf_rules`. Use it only when the user explicitly asks to apply without a preview, and never together with `previewToken`. Still read, validate, show the change, and get `confirm`. The high-risk confirmation still applies.

### High-risk changes

These shapes can block nearly all traffic:

- a geo or ASN `ALLOW` list without `paths`
- a user-agent `matchMode: "any"` BLOCK without `paths`
- IP BLOCK entries that cover a whole address family (`0.0.0.0/0`, `::/0`, or ranges that add up to one)

Only the rule type being changed is checked. `validate_waf_rule` and `test_waf_rules` report these in `riskFindings`, and `update_waf_rule` answers `HighRiskWafChange` and changes nothing. Then:

1. Show the user `error.highRiskChange`: `targetHostnames`, each risk's `title` and `message`, and the `confirmationPhrase` (for example `APPLY TO 2 DOMAINS`).
2. Ask the user to type that phrase. Only the user can confirm. Don't type it for them, and don't treat an earlier `confirm` or your own judgment as confirmation.
3. After the user types it, resend the same `update_waf_rule` request with `highRiskChangeConfirmation`: `candidateHash`, `currentStateHash`, `confirmationPhrase`, `expiresAt`, and `confirmationToken` copied unchanged from `error.highRiskChange`, and `acknowledgedRiskIds` listing every `risks[].id` from the challenge (not the `riskFindings` codes).
4. The challenge expires about 5 minutes after it's issued. An expired or edited confirmation gets a new challenge: show it and ask again. If the preview token lapsed (`WafPreviewExpired`), test again first.

### Reviewing rules

1. Read with `get_waf_rules` and describe each domain's rules in plain language, in evaluation order (see "How rules combine"). Say when domains differ.
2. Flag what's likely to surprise the user: geo or ASN allow-lists and user-agent catch-alls; IP or user-agent `ALLOW` entries the user may expect to exempt traffic from other rule types; entries that can never match because an earlier entry catches the same traffic; `bypassVerifiedBots: false` (search crawlers can be blocked); domains with no config; `hostnamesSkipped`.
3. For a plain-language reading of a rule type, pass its current config to `validate_waf_rule` and use `explanation`. When domains differ, set `domains` and `previousDomains` to that one domain.
4. `suggest_waf_changes` proposes changes and applies none. A `proposedChange` is a single entry: merge it into the full config and take it through the normal flow. Suggestions of type `setting` can't be applied with these actions.

## Rule Reference

`mode` is `BLOCK` or `ALLOW`. `validate_waf_rule` names the exact field when something is wrong.

### ipRules

```json
{
  "ips": [
    { "ip": "198.51.100.7", "mode": "ALLOW" },
    { "ip": "198.51.100.0/24", "mode": "BLOCK" },
    { "ip": "2001:db8::/32", "mode": "BLOCK" }
  ]
}
```

- 1-100 entries: IPv4 or IPv6 addresses or CIDR ranges. The size limit can run out before 100 (see "Size limit"). IPv4 needs all four parts (`10.0.0.0/8`, not `10/8`).
- First match wins. Above, `198.51.100.7` isn't blocked by the `/24` because it matches first.
- `ALLOW` only skips the rest of the IP list. It doesn't exempt the request from geo, ASN, or user-agent rules.
- IP entries can't have `paths`.

### geoRules

```json
{ "countryList": ["RU", "KP"], "mode": "BLOCK" }
```

- 1-250 ISO 3166-1 alpha-2 codes: `GB`, not `UK`. Unofficial codes such as `EU` and `XK` are rejected. Lowercase is accepted and stored uppercase.
- `BLOCK` blocks the listed countries. `ALLOW` blocks every country that isn't listed, and may also block requests without country data (see [IP geolocation](https://developers.cloudflare.com/network/ip-geolocation/)).
- One `mode` and one optional `paths` for the whole list, so a domain can't have a country block list and allow list at the same time.

### asnRules

```json
{ "asnList": [14061, 24940], "mode": "BLOCK", "paths": [{ "path": "/api" }] }
```

- 1-100 ASNs as numbers, not strings like `"AS14061"`. Examples: 16509 Amazon/AWS, 14061 DigitalOcean, 24940 Hetzner, 16276 OVH.
- `mode` and `paths` work as in geoRules, so an `ALLOW` list may also block requests without ASN data. Blocking a hosting network blocks everything that runs there, not only scrapers.

### userAgentRules

```json
{
  "blockEmpty": true,
  "patterns": [
    { "pattern": "AcmeApp/", "mode": "ALLOW", "paths": [{ "path": "/api" }] },
    { "matchMode": "any", "mode": "BLOCK", "paths": [{ "path": "/api" }] },
    { "pattern": "BadBot", "mode": "BLOCK" }
  ]
}
```

Above, only AcmeApp can call `/api`, `BadBot` is blocked everywhere, and requests with no User-Agent are blocked everywhere.

- Up to 50 patterns. First match wins, and a request that matches none is allowed. `ALLOW` only skips the remaining patterns.
- `blockEmpty` (default `false`) blocks requests with no User-Agent, on every path, before patterns are checked.
- `matchMode`:
  - `contains` (default): case-insensitive substring. Plain text: `*` and `?` aren't wildcards.
  - `exact`: the whole User-Agent must equal `pattern` (case-sensitive).
  - `any`: matches every request, including ones with no User-Agent. Omit `pattern`. Put it after the `ALLOW` entries as a catch-all BLOCK to build an allow-list.
  - `browserVersionFloor`: matches `browser` (`chrome`, `edge`, or `firefox`; Safari isn't supported) at or above a version floor set by `withinLatest` (the latest N major versions, 1-100), `minVersion` (1-1000), or both, in which case the higher floor applies. Omit `pattern`. Usually an `ALLOW` before a broader BLOCK.
- `browser`, `withinLatest`, and `minVersion` are only allowed with `browserVersionFloor`.
- `pattern`: up to 256 characters, using letters, digits, spaces, and `. , ; : / ( ) [ ] - _ + ! ~ * ? @ # =`.
- `paths` is set per pattern. A pattern whose `paths` don't match the request is skipped and the next one is checked.

### Blocking bots and AI crawlers

Bot bypass runs before all of the site's WAF rules. While it's on (`bypassVerifiedBots: true`, the default), every bot Cloudflare verifies skips them. Cloudflare's verified list includes the major search engines and can include AI crawlers.

- While Bot bypass is on, a User-Agent block can't stop a verified crawler. Cloudflare's [bot directory](https://radar.cloudflare.com/bots/directory) lists which bots are verified. If a block on a crawler doesn't take effect, the crawler is probably verified. Say this in the preview for any crawler block.
- Turning Bot bypass off is a setting the user changes in the Dashboard, under Site settings > Security. These actions can't change it. With it off, the rules also apply to search engine crawlers, which can affect indexing.
- Bots with Webflow bot tokens skip the rules the same way (`bypassAuthorizedBots`).

### Path scope

```json
"paths": [{ "path": "/admin" }, { "path": "/login", "matchMode": "exact" }]
```

- 1-20 entries. Each `path` starts with `/`. Omit `paths` to apply everywhere; an empty list is rejected.
- `prefix` (default) matches the path and everything under it: `/api` matches `/api` and `/api/v1`, not `/api-docs`. `exact` matches only that path. Trailing slashes count.
- With `prefix`, `/blog` covers `/blog` and the pages under it, while `/blog/` covers only `/blog/` itself, not `/blog/post`.
- `{ "path": "/" }` matches only the home page, not the whole site.
- geoRules and asnRules take `paths` on the rule, userAgentRules on each pattern, and ipRules not at all.

### How rules combine

- For each request, Bot bypass runs first (see "Blocking bots and AI crawlers"), then `ipRules`, `geoRules`, `asnRules`, and `userAgentRules`, in that order. The first BLOCK stops evaluation. If nothing blocks, the request is served.
- `ALLOW` never overrides another rule type. An IP `ALLOW` doesn't let a visitor past a geo block.

### Domain scope

- Omit `domains` to change every connected custom domain. Each domain keeps its other rule types. When the domains' configs differ, a site-wide change can be refused with `WafConfigDrift`; use domain scope instead.
- `domains` names target domains as they appear in `byDomain`. A domain-scoped update also needs `previousDomains`: the domains the rule you're editing covered before the edit, or `[]` for a new rule. The rule type is removed from every domain in `previousDomains` that isn't in `domains`. Domains in neither list don't change.
- To move a geo rule from `www.example.com` to `shop.example.com`, send `domains: ["shop.example.com"]` and `previousDomains: ["www.example.com"]`.
- Deletions take `domains` only.

### Size limit

Each domain's whole WAF config, all rule types together, has a storage limit. `targets[].candidateBytes` and `candidateBytesLimit` show the headroom, and going over is a `ValidationError`. Long IP lists and many `paths` entries use it up fastest: an IP list in the high double digits can reach it before the 100-entry cap.

### Cloudflare references

Webflow's WAF uses Cloudflare's data about each request (its country, ASN, and verified-bot status), but the rule format and behavior above are Webflow's own. Cloudflare's WAF custom rules, managed rules, rate limiting rules, and rule expressions aren't available through Webflow's WAF, so don't suggest or write them.

- [IP geolocation](https://developers.cloudflare.com/network/ip-geolocation/): when a visitor's country looks wrong. Country data is Cloudflare's estimate, updated several times a week, and the page has a correction form.
- [Radar IP lookup](https://radar.cloudflare.com/ip): to check an IP's country and ASN while writing `ipRules`, `geoRules`, or `asnRules`. ASN pages follow `https://radar.cloudflare.com/as<number>`, for example [radar.cloudflare.com/as13335](https://radar.cloudflare.com/as13335). Radar challenges automated requests, so if you can't load a page, give the user the link.
- [Verified bots](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/): what makes a bot verified. Verified bots skip all WAF rules while Bot bypass is on; to check a specific crawler, see "Blocking bots and AI crawlers".

## Errors

Every WAF action answers `{success: true, ...}` or `{success: false, error: {name, message, ...}}`. Relay `error.message` to the user. Refusals before the action runs arrive as an action error with `status`, `code`, and `message`.

| Result | Meaning and what to do |
|--------|------------------------|
| `ValidationError` | Invalid config or request: the shape (`details`, plus `schema` from `validate_waf_rule`), an unknown domain, the size limit, or a date range. Fix it and validate again. |
| `WafSiteStateChanged`, `WafPreviewStale` | The rules changed after your read or test. Don't resend. Read again, rebuild the change on the new state, show the user if it differs, then validate and test again. |
| `WafPreviewExpired`, `WafPreviewInvalid` | The token lapsed or doesn't match the request. Test again and apply exactly the tested values. |
| `WafPreviewRequired` | No `previewToken` was sent. Test first. |
| `WafConflictingApplyMode` | Both `previewToken` and `directApply` were sent. Send only the token. |
| `HighRiskWafChange` | Nothing was applied. Follow "High-risk changes". |
| `WafMutationRateLimited` | Too many changes on the site. Wait `retryAfterSeconds`, then retry once. Every update or delete attempt counts. |
| `WafPartialMutation` | Some domains changed and others didn't. Show `error.recovery` (`applied`, `failed`, `unknown`, `pending`), read again, and reconcile with the user's OK. If a domain's state is `unknown`, suggest contacting Webflow support. |
| `WafChangeInProgress`, `WafChangeUnavailable` | Another change is running, or changes are briefly unavailable. Retry shortly. |
| `WafChangeInterrupted` | Another change interrupted this one. Read again and review before retrying. |
| `WafConfigDrift` | The domains have different configs, so a site-wide change is refused. Use domain scope. |
| `NoCloudflareHostnames` | No custom domain WAF can apply to yet: none is connected, or setup hasn't finished. Tell the user. |
| `WafMcpWritesUnavailable` | Changing rules through MCP isn't available for this site yet. Nothing changed and reads still work. Point the user to Site settings > Security. |
| `WafTestedApplyUnavailable` | Applying a tested preview is off for this site. Nothing changed. Use `directApply` only if the user explicitly asks. |
| 403 `waf_mcp_not_enabled` | WAF MCP isn't enabled for this site's workspace yet. Don't retry. |
| 403 `waf_not_included_in_plan` | The site's plan doesn't include WAF, which is available on Enterprise plans. Don't retry. |
| 403 `forbidden` | The user's role can't manage this site's domains. Don't retry. |
| 403 `missing_scopes` | The connection lacks `site_config:read` or `site_config:write`. The user reauthorizes the Webflow MCP connection. |
| 404 | The site isn't in this authorization or isn't active. |
| 503 `waf_access_unavailable` | WAF access couldn't be checked, and nothing changed. Retry in a few minutes. |
| Anything else | Relay `error.message`. Don't retry a write more than once. |

## Examples

### Example 1: Add countries to an existing block list

**User prompt:**
```
Block traffic from Russia and North Korea.
```

1. `get_waf_rules`: `uniform` is true, and both domains have `geoRules: {"countryList": ["CN"], "mode": "BLOCK"}`.
2. Merge, keeping CN, and validate site-wide:
   ```json
   { "ruleType": "geoRules", "config": { "countryList": ["CN", "RU", "KP"], "mode": "BLOCK" } }
   ```
   The `explanation` says it blocks CN, RU, and KP on every domain, and there are no risk findings.
3. `test_waf_rules` with the same values and `expectedSiteStateHash`, then show:
   ```
   Country rule, all domains
   Now:   block CN
   After: block CN, RU, KP
   Changes: example.com, www.example.com
   Risks: none

   Type "confirm" to apply.
   ```
4. After `confirm`, `update_waf_rule` with the `previewToken`, then `get_waf_rules` to verify.

### Example 2: Allow only some countries (high-risk)

**User prompt:**
```
Only let visitors from the US and Canada in.
```

1. `validate_waf_rule` with `{"countryList": ["US", "CA"], "mode": "ALLOW"}` returns an `explanation` describing the allow-list and a `geo_allow_list_default_deny` risk finding. Tell the user that every other country will be blocked, and ask whether it should apply only to some paths, such as `/admin`.
2. The user wants it everywhere. Test, preview, and get `confirm`. `update_waf_rule` answers `HighRiskWafChange`. Show:
   ```
   High-risk change: Geo allow-list (default deny)
   Visitors from every country not in the allow list are blocked site-wide.
   Only traffic from the listed countries can continue.
   Domains: example.com, www.example.com

   To apply it, type: APPLY TO 2 DOMAINS
   ```
3. After the user types the phrase, resend the same request with:
   ```json
   "highRiskChangeConfirmation": {
     "candidateHash": "<copied from error.highRiskChange>",
     "currentStateHash": "<copied>",
     "confirmationPhrase": "APPLY TO 2 DOMAINS",
     "acknowledgedRiskIds": ["geo-allow-list"],
     "expiresAt": "<copied>",
     "confirmationToken": "<copied>"
   }
   ```

### Example 3: Block a script on one path, but keep an integration working

**User prompt:**
```
Block python-requests on /api. Our sync job sends "AcmeSync/2.0 python-requests/2.31", so keep that working.
```

The site has `userAgentRules: {"blockEmpty": false, "patterns": [{"pattern": "BadBot", "mode": "BLOCK"}]}`. Keep the existing entry and put the `ALLOW` before the BLOCK it has to get past:

```json
{
  "blockEmpty": false,
  "patterns": [
    { "pattern": "BadBot", "mode": "BLOCK" },
    { "pattern": "AcmeSync/", "mode": "ALLOW" },
    { "pattern": "python-requests", "mode": "BLOCK", "paths": [{ "path": "/api" }] }
  ]
}
```

Validate, check that the explanation scopes the python-requests block to `/api`, then test, confirm, and apply.

### Example 4: Remove a rule type from one domain

**User prompt:**
```
Remove the country rules from shop.example.com.
```

1. `test_waf_rules` with `{"operation": "delete", "ruleType": "geoRules", "domains": ["shop.example.com"], "expectedSiteStateHash": "<latest>"}`.
2. Show that only shop.example.com loses its country rule, and that its other rules and the other domains don't change. Ask for `confirm`.
3. `delete_waf_rule` with `ruleType`, `domains`, `expectedSiteStateHash`, and the `previewToken`.

### Example 5: Review the current rules

**User prompt:**
```
What is my firewall blocking right now?
```

**Response:**
```
WAF rules for Acme Site (2 custom domains, same rules on both)

1. IP: allows 198.51.100.7, blocks the rest of 198.51.100.0/24
2. Country: allows only US and CA, so every other country is blocked
3. User-Agent: blocks requests with no User-Agent, and anything containing "BadBot"

Bot bypass is on, so verified crawlers such as Googlebot skip these rules.

Worth knowing: the IP allow for 198.51.100.7 doesn't exempt that address from
the country rule. If it's outside the US and Canada, it's still blocked.
```

## Guidelines

- Never write without the user typing `confirm` after seeing the preview. A request to review, explain, or suggest isn't permission to change anything.
- Never send `highRiskChangeConfirmation` unless the user typed the `confirmationPhrase` after seeing that challenge.
- Never use `directApply` unless the user explicitly asked to skip the preview.
- Change one rule type at a time, and always send its complete config, merged from a fresh `get_waf_rules`.
- Don't resend a failed write unchanged: read again, rebuild, and test again. Every update or delete attempt counts against the site's change limit.
- Warn before blocking search crawlers, whole countries, or hosting networks, and suggest `paths` to limit broad rules.
- Don't paste `previewToken` or `confirmationToken` values into chat.
- When the API refuses a call, relay `error.message`. Don't work around a refusal with another tool or a direct API call.
