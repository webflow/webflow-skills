---
name: webflow-workflow:status-update
description: Generate a project, team, or sprint status update. Use for weekly status, project updates, sprint updates, or summaries of shipped work from Jira, GitHub, and Slack.
argument-hint: "[optional: week offset, e.g. '-1' for last week]"
compatibility: Requires gh, slack, and atlassian
---

# Status Update

Generate a concise status update by collecting project name, Slack channel, Jira epic, GitHub authors/teams, and repo, then pulling PRs, Slack context, and Jira tickets.

## Step 0: Collect Config

Before doing anything else, check whether the user already provided the required inputs inline (e.g. "weekly status for #proj-components-and-bindings-api, STRUCT-1234, authors: alice, bob"). If all values are present, proceed directly to Step 1. Otherwise, ask the user for any that are missing.

**Required inputs:**

| Input | Description | Default / example |
|---|---|---|
| `PROJECT_NAME` | Human-readable project/team name for the update header | e.g. "Components & Bindings API" |
| `PROJECT_STATUS` | Current project status | One of: `On track`, `At risk`, `Off track` |
| `SLACK_CHANNEL` | Slack channel ID **or** channel name/URL | e.g. `C0AFFPBMCAJ` or `#proj-components-and-bindings-api` |
| `JIRA_EPIC` | Jira epic key (optional — skip if no Jira epic exists) | e.g. `STRUCT-2951` |
| `GH_AUTHORS` | Comma-separated GitHub usernames **or** team handles to include | e.g. `alice, lebron` or `@webflow/agent-loop` |
| `GH_REPO` | GitHub repo in `owner/repo` format | Default: infer from `gh repo view --json nameWithOwner` |
| `PERIOD` | Time period to cover (optional) | Default: `7` (days). Examples: `14` for biweekly, `30` for monthly, `90` for quarterly |

**Resolving `GH_AUTHORS`:**

If a value starts with `@`, treat it as a GitHub team handle. Resolve it to individual members:

```bash
# Resolve team handle to member list (e.g. @webflow/agent-loop → alice, bob, charlie)
gh api orgs/webflow/teams/agent-loop/members --jq '.[].login'
```

Mix-and-match is supported: `@webflow/agent-loop, extra-contributor`.

Resolve `SLACK_CHANNEL` to a channel ID if a name or URL was provided:

```
Use Slack tools to search for the matching channel name.
```

## Workflow

### Step 1: Determine the date range

Use `$PERIOD` to calculate the lookback window (default: 7 days). If the user passes a week offset (e.g. `-1`), shift the window back by that many periods.

```bash
# Calculate date range based on PERIOD (default 7 days)
PERIOD=${PERIOD:-7}
START_DATE=$(date -v-${PERIOD}d +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)
START_DATE_FORMATTED=$(date -v-${PERIOD}d +"%-B %-d")  # e.g. "March 16"
echo "Date range: $START_DATE to $END_DATE"
# PERIOD_LABEL: "Week" (7), "Two weeks" (14), "Month" (30), "Quarter" (90), or "{N} days"
```

### Step 2: Gather PRs from GitHub (primary source)

Search for PRs authored by each team member in the date range. Run one command per author in parallel, substituting `$GH_REPO` and each author from `$GH_AUTHORS`:

```bash
# Merged PRs (include body to extract Jira ticket)
gh pr list --repo $GH_REPO --author <author> --state merged --search "merged:>=$START_DATE" --json number,title,url,body,mergedAt --limit 30

# Open / Draft PRs (currently active)
gh pr list --repo $GH_REPO --author <author> --state open --json number,title,url,body,isDraft --limit 20
```

#### Extract Jira ticket from each PR

For each PR, parse the `body` field to find the Jira ticket key. Look for patterns like:
- A Jira URL: `https://webflow.atlassian.net/browse/PROJ-XXXX`
- A ticket key in text: `STRUCT-1234`, `DEVPL-5678`, `IDSC-999`, etc.
- The branch name often contains the ticket key, e.g. `STRUCT-3606-some-description`

Extract the **first matching Jira ticket key**. If no ticket is found, fall back to the PR number and URL.

For each PR, determine if it's related to `$PROJECT_NAME`. Relevance signals:
- Branch or title mentions keywords related to the project
- Jira ticket in the branch matches `$JIRA_EPIC` or its child tickets (if provided)

**When in doubt, include the PR** — the user will manually exclude irrelevant ones.

### Step 3: Check Slack for additional context (secondary)

Use Slack tools to read recent messages from the project channel:

```
Read the Slack channel with `channel_id: "$SLACK_CHANNEL"` and `limit: 50`.
```

Scan for:
- Decisions made (e.g. "we decided to...", "going with...", "aligned on...")
- Documents or specs shared (Confluence links, Google Docs, Figma links)
- Blockers mentioned
- Notable discussions about direction or scope changes

Summarize any relevant findings briefly (1-2 bullets max). Skip if nothing notable.

### Step 4: Check Jira epic for context (secondary)

Skip this step if no `$JIRA_EPIC` was provided.

Use Jira tools to check the epic:

```
Read the Jira issue with `issueIdOrKey: "$JIRA_EPIC"`.
```

Optionally search for child issues updated this week:

```
Search Jira with JQL: `parent = $JIRA_EPIC AND updated >= '-7d' ORDER BY updated DESC`, limit 20.
```

Use Jira to supplement context — e.g. upcoming milestones, status changes, or tickets that moved but didn't have PRs.

### Step 5: Categorize work

Sort all gathered items into two buckets:

1. **What got done** — Merged PRs and completed work
2. **What is next** — Open/draft PRs, upcoming Jira tickets, and planned work mentioned in Slack

### Step 6: Format the status update

Output the update in this exact format:

```
**{PROJECT_NAME} — {PERIOD_LABEL} of {START_DATE_FORMATTED}**

**Status**: {PROJECT_STATUS}

**What got done**
- {Brief description of merged PR or completed work} ([PROJ-XXXX](https://webflow.atlassian.net/browse/PROJ-XXXX))
- ...

**What's next**
- {Brief description of open/draft PR or upcoming work} ([PROJ-XXXX](https://webflow.atlassian.net/browse/PROJ-XXXX))
- ...

{Optional: 1-2 bullets of notable Slack decisions or docs, only if relevant}
```

**Linking rules:**
- Link to the Jira ticket extracted from the PR description, not the PR itself.
- Format: `[PROJ-XXXX](https://webflow.atlassian.net/browse/PROJ-XXXX)`
- If multiple PRs share the same Jira ticket, combine them into one bullet.
- If no Jira ticket is found in a PR, fall back to the PR link: `([#number](pr_url))`
- If no `$JIRA_EPIC` was provided, omit Jira links entirely and always use PR links.

### Step 7: Present to user and offer to post

Show the formatted update and ask:
> "Here's the draft. Want me to adjust anything, or shall I post it to Slack?"

Recommend sending it to themselves first to test. If the user approves, post to the Slack channel:

```
Send the formatted update to Slack with `channel_id: "$SLACK_CHANNEL"`.
```

## Key Instructions

- **Be concise** — each bullet should be one short line. No one wants to read a wall of text.
- **Do NOT include author names** — just describe the work and its status.
- **GitHub is the source of truth** — Slack and Jira are supplementary context only.
- **When in doubt, include a PR** — the user will manually remove irrelevant items.
- **Status is user-provided** — always use the `$PROJECT_STATUS` value the user gave; never infer or override it.
- **Link to Jira tickets, not PRs** — extract the ticket key from the PR description/branch and link to it. Fall back to PR link only if no ticket is found.
- **Do not post to Slack without explicit user approval.**
