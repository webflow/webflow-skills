---
name: webflow-workflow:sybg-guide
description: Create a Since You've Been Gone (SYBG) modal with Knock Guides. Use for feature announcement guides, Knock Guide setup, targeting, scheduling, and rollout gates.
argument-hint: "[guide-name]"
---

# Create a New SYBG Guide in Knock

Set up Knock Guide creation, audience targeting, tenancy mode, runtime conditions, URL activation, content setup, scheduling, and prioritization.

## Safety checks
- Always make changes and commits in the `development` environment only.
- Do not modify, update, archive, or delete any existing guides. Only create a new guide for the requested announcement.
- Always prompt the users to go to `https://dashboard.knock.app/webflow/development/guides` to verify the changes and prompt them to promote to `production` after validating visually in the dashboard.
- If you encounter issues, raise a ticket in **#triage-scale-lifecycle** Slack channel.

## References
- Knock Agent Toolkit: https://docs.knock.app/developer-tools/agent-toolkit/tools-reference
- Knock Management API Guide Upsert: https://docs.knock.app/mapi-reference/guides/upsert

## Prerequisites

### Knock Integration (Required)

The Knock integration lets agents create and commit guides directly via API — skipping manual dashboard steps for guide creation, message type inspection, committing, and promoting.

For example, set up the Knock connector in Claude Code:
```
claude mcp add --transport http knock https://mcp.knock.app/mcp
```
Then authenticate via OAuth. In other agent environments, use the available connector setup flow.

**Knock tools used by this skill:**

| Tool | When used |
|------|-----------|
| `listEnvironments` | Confirm available environments |
| `createOrUpdateGuide` | Create or update the guide |
| `commitAllChanges` | Commit guide config in development |
| `searchDocumentation` | Look up Knock API fields on demand |


## Step I: Guide Name

- Prompt the user to enter the name for the guide. This name typically maps to the name of the feature that is to be announced.
- With the guide name, generate a guide key which acts as a human-readable unique identifier for the guide. Convert the guide name to kebab-case for the guide key.

## Step II: Guide Message

- The Message Type for the SYBG guide is `since-youve-been-gone`. It has only one variant: `default`.
- The schema for the `default` variant of the `since-youve-been-gone` message type is:
   ```json
   {
      "fields": [
         {
               "key": "title",
               "label": "Full Title",
               "settings": {
                  "default": "Release name here",
                  "description": "The title of the product update",
                  "max_length": 100,
                  "min_length": 1,
                  "required": true
               },
               "type": "text"
         },
         {
               "key": "titleCondensed",
               "label": "Condensed Title",
               "settings": {
                  "default": "Short release name",
                  "description": "The condensed version of the title",
                  "max_length": 26,
                  "min_length": 1,
                  "required": true
               },
               "type": "text"
         },
         {
               "action": {
                  "key": "action",
                  "label": "Image action",
                  "settings": {
                     "default": "",
                     "required": false
                  },
                  "type": "text"
               },
               "alt": {
                  "key": "alt",
                  "label": "Alt text",
                  "settings": {
                     "default": "Short description of the image",
                     "required": true
                  },
                  "type": "text"
               },
               "key": "image",
               "label": "Image",
               "settings": {
                  "required": true
               },
               "type": "image",
               "url": {
                  "key": "url",
                  "label": "Image URL",
                  "settings": {
                     "default": "https://d3e54v103j8qbb.cloudfront.net/since-youve-been-gone/sybg-single.png",
                     "required": true
                  },
                  "type": "url"
               }
         },
         {
               "key": "content",
               "label": "Content",
               "settings": {
                  "default": "Write the description of the release here!",
                  "required": true
               },
               "type": "markdown"
         },
         {
               "action": {
                  "key": "action",
                  "label": "Action or URL",
                  "settings": {
                     "default": "https://webflow.com/update",
                     "required": false
                  },
                  "type": "text"
               },
               "key": "primaryButton",
               "label": "Primary Button",
               "settings": {
                  "required": false
               },
               "text": {
                  "key": "text",
                  "label": "Text",
                  "settings": {
                     "default": "Learn more",
                     "required": false
                  },
                  "type": "text"
               },
               "type": "button"
         },
         {
               "action": {
                  "key": "action",
                  "label": "Action or URL",
                  "settings": {
                     "default": "",
                     "required": false
                  },
                  "type": "text"
               },
               "key": "secondaryButton",
               "label": "Secondary Button",
               "settings": {
                  "required": false
               },
               "text": {
                  "key": "text",
                  "label": "Text",
                  "settings": {
                     "default": "",
                     "required": false
                  },
                  "type": "text"
               },
               "type": "button"
         }
      ],
      "key": "default",
      "name": "Default"
   }
   ```
- Prompt the user to enter the title for the guide. The title should be limited to a 100 characters.
- Prompt the user to enter the condensed title for the guide. The condensed title should be limited to 26 characters.
- Prompt the user to enter the image URL for the guide. The image should be a high resolution image (>= 1200x630) and should be optimized for web (<= 100kb). This input is optional, and if no image URL is provided, then default to: `https://d3e54v103j8qbb.cloudfront.net/since-youve-been-gone/sybg-single.png`
- Prompt the user to enter the alt text for the image. If no alt text is provided, then default to: "Webflow product update".
- Prompt the user to enter the content for the guide. This represents the "body" of the guide.
- Prompt the user to enter the text of the Primary CTA Button. This input is optional, and if no text is provided, then default to: "Learn more".
- Prompt the user to enter the URL of the Primary CTA Button. This input is optional, and if no URL is provided, then default to: "https://webflow.com/update".
- Prompt the user to enter the text of the Secondary CTA Button. This input is optional, and if no text is provided, then default to: "".
- Prompt the user to enter the URL of the Secondary CTA Button. This input is optional, and if no URL is provided, then default to: "".

## Step III: Guide Targeting

### III-A. Choose Audience

Select the set of Users eligible to receive the Guide. Audiences can be:
- All users
- A specific list (e.g., users enrolled in a beta, imported CSV)
- A dynamically computed segment

- Default the audience to "All users". If the user wants to target a specific audience, then prompt the user to enter the audience key. The list of audiences can be found at: `https://dashboard.knock.app/webflow/development/audiences`.

### III-B. Tenancy Strict Mode

Enable this when a Guide should only appear to a User when they are in a **specific workspace**.

| Mode | Behavior |
|------|----------|
| **Enabled** | Knock checks for an exact `{userId, tenantId}` match. User must be in the Audience *with that specific workspace's tenantId*. |
| **Disabled** | Knock only checks `userId`. User sees the Guide in **all** their workspaces if present in the Audience. |

A Knock `Tenant` maps 1:1 to a Webflow Workspace. Enable strict mode when the Guide is workspace-specific; leave it off for account-level announcements.

Ask the user: "For a particular user, should this guide appear to this user across all their workspaces, or only in specific workspaces?". If the user wants the guide to appear in all workspaces, then set the tenancy strict mode to `false`. If the user wants the guide to appear in specific workspaces, then set the tenancy strict mode to `true`.

In most cases, the ``tenancy strict mode`` will most likely be set to `false` for SYBG guides.

### III-C. Activation (URL Targeting)

Specify which URLs the Guide should appear on.

- **Simple**: Enter a path (e.g., `/dashboard`) to restrict to that exact page.
- **Advanced**: Use regular expressions to match multiple paths, or add query parameter conditions.

Leave blank to show the Guide on all pages.

## Step IV: Create and commit to `development` environment

1. Call `createOrUpdateGuide` in `development` with the appropriate payload. For reference: https://docs.knock.app/mapi-reference/guides/upsert.
2. Call `commitAllChanges` on the `development` environment to save the guide configuration.
