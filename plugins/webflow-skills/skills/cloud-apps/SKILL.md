---
name: webflow-mcp:cloud-apps
description: Inspect and operate existing Webflow Cloud apps through Webflow MCP. Use when listing Cloud apps, checking app metadata or domains, inspecting environments or environment-variable names, reviewing deployments, diagnosing build or runtime failures, triggering or re-running GitHub deployments, updating app metadata, deleting environment variables, or removing apps. Do not use for design/CSS variables, creating Cloud apps, CLI-driven builds or deployments from local source, or creating/updating environment-variable values.
---

# Webflow Cloud Apps

Inspect and manage existing Webflow Cloud apps with `data_apps_tool`. Use the
Webflow CLI skill for project creation, building local source and deploying it
to Webflow Cloud, and environment-variable writes that this tool does not
support.

## Instructions

### Phase 1: Establish scope

1. Call `webflow_guide_tool` before any other Webflow MCP tool.
2. Use only Webflow MCP tools for Webflow operations. Do not call Webflow APIs
   directly.
3. Include the required `context` parameter in every tool call. Write 15-25
   words in third-person perspective.
4. Confirm that the request concerns a Webflow Cloud app:
   - Use `data_apps_tool` for existing Cloud apps, environments, deployments,
     logs, domains, and environment-variable metadata.
   - Use `data_variable_tool` for Designer color, size, font, and CSS variables.
   - Use the `webflow-cli:cloud` skill to create an app, build or deploy local
     source, or create/update an environment variable.
5. If `data_apps_tool` is unavailable, report that the Cloud Apps MCP capability
   is not enabled. Do not bypass it with a direct API request.

Never ask the user to paste an environment-variable value or secret into chat.
When a value must be created or changed, direct the user to the installed
Webflow CLI's built-in help and require a hidden prompt, stdin, or protected
file. Do not guess a CLI command.

### Phase 2: Resolve identifiers

Discover identifiers in this order:

```text
list_apps -> app_id
list_environments(app_id) -> env_id
list_deployments(app_id, env_id) -> deployment_id
```

Use an identifier supplied by the user only after verifying it through the
corresponding get or list action. If a list action returns `nextCursor`, pass it
back as `cursor` until `nextCursor` is null. One page is not proof that a
resource is absent.

If multiple resources match, present identifying metadata and require the user
to choose before any mutation. Auto-select only when exactly one unambiguous
resource matches.

### Phase 3: Route the request

| Intent | Action sequence |
|---|---|
| Find apps | `list_apps` |
| Inspect one app | `get_app` |
| Find live custom hostnames | `get_app_domains` |
| Rename or describe an app | `get_app` -> confirm -> `update_app` -> `get_app` |
| Remove an app | `delete_app` dry run -> confirm -> `delete_app` with `dry_run: false` |
| Find environments | `list_environments` |
| Inspect variable names | `list_variables` |
| Delete one variable | `delete_variable` dry run -> confirm -> `delete_variable` with `dry_run: false` |
| Review deployment history | `list_deployments` -> `get_deployment` |
| Deploy the connected branch HEAD | `trigger_deployment` dry run -> confirm -> execute -> poll |
| Retry or roll back an exact commit | Select deployment -> `redeploy` dry run -> confirm -> execute -> poll |
| Diagnose a build or deploy failure | `get_deployment` -> `get_build_logs` |
| Diagnose the running app | `get_runtime_logs` |

The action's live schema is authoritative for arguments and response fields. Do
not invent fields from this table.

### Phase 4: Execute read-only workflows

For app inspection:

1. Locate the app with `list_apps`.
2. Use `get_app` for app metadata or `get_app_domains` for custom hostnames.
3. Explain that `get_app_domains` excludes the default `*.webflow.io` hostname.
   For an app attached to a regular Webflow site, returned domains belong to the
   parent site and may be shared by sibling apps.

For environment variables:

1. Locate the environment with `list_environments`.
2. Call `list_variables`.
3. Report keys and metadata. Secret entries have `isSecret: true` and no value;
   never imply that a missing secret value is an error.

For deployment inspection:

1. Use `list_environments` for the environment and its
   `latestDeploymentStatus`.
2. Use `list_deployments`, which returns newest first.
3. Use `get_deployment` for the selected deployment's full timeline.
4. Treat `starting`, `building`, and `deploying` as active states. Report any
   other value rather than guessing what it means.
5. A failed phase sets `buildFailedAt` or `deployFailedAt` while its matching
   finished timestamp remains null. A null finished timestamp alone does not
   prove that the phase is still running.

For logs:

1. Prefer a deployment whose `logsAvailable` value is true before calling
   `get_build_logs`.
2. Use `since` and `q` to narrow results before retrieving broad log windows.
3. Page until `nextCursor` is null when completeness matters.
4. Treat build-phase and runtime logs as raw, potentially sensitive customer
   output. Inspect lines for tokens, credentials, cookies, authorization
   headers, and presigned URLs before quoting or saving them.
5. Explain that runtime logs are retained for approximately one hour on the
   base plan. An empty result for an older window is valid.

### Phase 5: Preview and execute mutations

Require the user to explicitly type `confirm` after showing the exact target and
effect. A prior request to inspect, diagnose, or preview does not authorize a
mutation.

For `update_app`:

1. Fetch the current app with `get_app`.
2. Show the exact name and description change. Explain that this cannot change
   source configuration or deployments.
3. Require confirmation, call `update_app`, then verify with `get_app`.
4. Pass `description: null` to clear a description. Do not use an empty string.

For `delete_variable`:

1. Call `delete_variable` with the default dry run. The preview confirms whether
   the exact key exists and returns no value.
2. If `exists` is false, report that no variable was deleted. Do not request
   confirmation or call the destructive operation.
3. If the preview cannot confirm existence, stop and report the error. Do not
   treat an incomplete paginated read as a missing key.
4. If `exists` is true, show the app, environment, and key, then warn that the
   action permanently deletes the variable.
5. Require confirmation, then call `delete_variable` with `dry_run: false`
   exactly once. Treat its successful `deleted: true` response as success even
   when the backend body has no readable message.

For `trigger_deployment`:

1. Call it with the default dry run and show the connected branch.
2. Explain that execution deploys the branch's latest commit, not local files.
3. Require confirmation.
4. Generate one stable `idempotency_key` before the first call with
   `dry_run: false`. Reuse the same key for every retry.
5. The action returns no deployment ID. Poll `list_deployments`, identify the
   new record, and use `get_deployment` until it leaves an active state or the
   bounded monitoring period ends.

For `redeploy`:

1. Select the previous deployment and call `redeploy` with the default dry run.
2. Show its exact commit hash and message. Explain that this creates a fresh
   build at that commit.
3. Require confirmation.
4. Execute with `dry_run: false` and a stable `idempotency_key`, then poll as
   described for `trigger_deployment`.

For `delete_app`:

1. Call it with the default dry run.
2. Report the returned `deletionMode`:
   - `archive`: reversible archival of the Cloud app.
   - `hard_delete`: permanent deletion of the attached app's project and
     environments.
3. Require confirmation after the mode-specific warning.
4. Call with `dry_run: false` exactly once. A successful `deleted: true`
   response remains success even when the backend body has no readable message.
   Do not infer failure from an unavailable post-delete resource.

### Phase 6: Handle errors

- `401` or `403`: report the authentication or permission problem; do not
  retry.
- `404`: verify the complete app -> environment -> deployment chain; do not
  silently switch targets.
- `429`: honor the backoff signal before a bounded retry.
- `5xx` on a read: retry a bounded number of times.
- `5xx` on a mutation: treat the outcome as uncertain. Reconcile with list/get
  actions before considering a retry.
- A successful mutation response with sparse or unreadable backend content is
  not a failure. Do not retry a deletion; poll deployment records when a deploy
  action cannot report its final status.
- Rejected cursor: restart that listing without the cursor and page again.
- `GITHUB_APP_NOT_INSTALLED`: provide the returned `installUrl`, require the
  user to reconnect GitHub, then retry only after reconnection.

An empty list is a valid success. Do not translate it into a tool failure.

### Phase 7: Report

State:

- The app and environment selected
- The actions performed
- The deployment status or mutation outcome
- Any pagination, retention, permission, or uncertainty limitation
- The next required user action only when the workflow cannot continue

Do not expose sensitive log content or environment-variable values.

## Examples

### Inspect a failed deployment

**User:** "Why did the latest production deployment fail?"

1. Call `webflow_guide_tool`.
2. Resolve the app with `list_apps`.
3. Resolve production with `list_environments`.
4. Fetch the latest record with `list_deployments`, then `get_deployment`.
5. If logs are available, call `get_build_logs` with a narrow error query.
6. Redact sensitive values and report the failed phase, relevant timestamps,
   concise root cause, and evidence.

### Trigger a deployment

**User:** "Deploy the latest commit for production."

1. Resolve the app and production environment.
2. Call `trigger_deployment` as a dry run.
3. Report the exact connected branch and request `confirm`.
4. After confirmation, execute with a stable idempotency key.
5. Poll the deployment list and report the resulting status.

### Set a secret

**User:** "Set `DATABASE_URL` in production."

Do not request the value and do not call `data_apps_tool`. State that MCP cannot
create or update environment variables. Route the task to
`webflow-cli:cloud`, using the installed CLI's help and a secret-safe input
method.

### Delete an environment variable

**User:** "Delete `OLD_FEATURE_FLAG` from staging."

1. Resolve the app and staging environment.
2. Call `delete_variable` with its default dry run.
3. If the preview confirms the key exists, disclose the exact target and stop
   until the user types `confirm`.
4. Call `delete_variable` with `dry_run: false` once, then report the result.

### Delete an app

**User:** "Delete my staging Cloud app."

1. Resolve the exact app.
2. Call `delete_app` as a dry run.
3. Explain whether the operation archives or permanently deletes it.
4. Stop until the user types `confirm`.
5. Execute once and report the returned outcome.

## Guidelines

- Call `webflow_guide_tool` first.
- Prefer MCP over CLI for supported operations on existing Cloud apps.
- Use CLI only for app creation, building local source and deploying it to
  Webflow Cloud, and environment-variable creation or updates.
- Never use `data_apps_tool` for Designer variables.
- Never mutate without an itemized preview and explicit `confirm`.
- Never retry an uncertain mutation before reconciling observable state.
- Never expose secrets from variables, logs, errors, or URLs.
- Never conclude that a paginated resource is absent after one page.
- Never fabricate IDs, deployment status, action arguments, or live URLs.
