---
name: webflow-workflow:dx-team-lookup
description: Look up what team a person belongs to using the DX data warehouse. Accepts a git committer name, email address, GitHub username, or commit SHA. Use when asked "what team is X on?", "who does this commit belong to?", or "map this committer to a team".
argument-hint: "[name, email, GitHub username, or commit SHA]"
compatibility: Requires dx
---

# DX Team Lookup

Look up what team a person belongs to using the DX developer productivity data warehouse.

Verify `psql` is available: `which psql`. If missing: "Install with: `brew install postgresql`"

## Step 1: Resolve the input

**Commit SHA** (e.g. `abc1234`):
```bash
git log -1 --format="%ae|||%an" <SHA>
```
Use the extracted email/name for the lookup.

**No argument**: use HEAD commit:
```bash
git log -1 --format="%ae|||%an"
```

**GitHub noreply email** (format: `12345+username@users.noreply.github.com`):
Extract the GitHub username from between `+` and `@`. Use that as the search term against `github_username`.

**Name, email, or username**: use directly as the search term.

## Step 2: Run the lookup

The query is extracted into a checked-in script to avoid agent transcription errors:

```bash
bash ~/.claude/skills/dx-team-lookup/scripts/lookup.sh "<search_term>"
```

Replace `<search_term>` with the resolved value from Step 2. If this skill is installed in a different agent-specific directory, substitute that installed skill path.

For noreply emails, run two passes: one with the GitHub username (e.g. `Roach`), and if no result, one with the numeric ID prefix stripped full name if available.

## Step 3: Output

**Match found:**
```
Person:  Arafat Abdulla (arafat.abdulla@webflow.com)
GitHub:  arafat-webflow
Team:    Subscription & Payments
Pillar:  Growth Pillar
As of:   2026-03-07

(Source: DX data warehouse)
```

If `pillar` is NULL (team has no parent in DX), omit the Pillar line entirely rather than printing blank.

**Multiple matches:**
```
Multiple matches for "zhang":

  Daniel Zhang  (daniel.zhang@webflow.com)  — Code Gen
  Alice Zhang   (alice.zhang@webflow.com)   — Platform Engineering

Tip: re-run with a full email or GitHub username for an exact match.
```

**No match:**
```
No match found for: "fbaralle"

This person may be an external contributor, contractor, former employee,
a recent hire not yet in DX, or a bot/automation account. The DX
warehouse only includes current Webflow employees.
```

## Future improvements

- **Agent-initiated outreach**: Once team membership is known, agents could use this data to route review requests, context questions, or approval workflows to the right people automatically.

## Key rules

- **Never print the value of `$DX_WAREHOUSE_DSN`** — it contains credentials.
- If `psql` returns a connection error, show the error message but not the DSN.
- The `as_of` date reflects the latest DX snapshot that includes this person. Team membership is synced from Workday quarterly (aligned with the quarterly survey), so data may lag by up to a quarter for org changes.
- If a person isn't found, that's a valid result (external contributor, contractor, former employee, recent hire, or bot/automation account).
- Common bot usernames in Webflow's git history (e.g. `wolfdew`, `renovate`, `github-actions`) will never appear in DX — skip lookup for these rather than treating a no-match as inconclusive.
