---
name: webflow-mcp:cloud-apps
description: Monitor and troubleshoot existing Webflow Cloud apps through Webflow MCP. Use when identifying apps or environments, checking domains or deployed versions, reviewing deployment health and history, diagnosing build, deploy, or runtime failures, verifying environment-variable keys, or previewing a retry, rollback, or GitHub branch deployment. Do not use for design/CSS variables, creating Cloud apps, deploying local source, or creating/updating environment-variable values.
---

# Webflow Cloud Apps

Use `data_apps_tool` to answer operational questions about existing Webflow
Cloud apps. Start from the user's outcome, gather only the evidence needed, and
distinguish observations from conclusions.

Use the `webflow-cli:cloud` skill when the task requires creating an app,
building or deploying local source, or creating or updating environment
variables. Client-side build output is not sent to Webflow and cannot be
recovered through MCP.

## Instructions

### 1. Establish scope

1. Call `webflow_guide_tool` before any other Webflow MCP tool.
2. Use only Webflow MCP tools for Webflow operations. Never call Webflow APIs
   directly.
3. Include the required `context` parameter in every tool call. Write 15-25
   words in third-person perspective.
4. Route by the capability the task requires:
   - Use `data_apps_tool` to inspect existing apps, environments, domains,
     deployment records, available server-side logs, and variable metadata.
   - Use `data_variable_tool` for Designer color, size, font, and CSS variables.
   - Use `webflow-cli:cloud` for app creation, local builds and deployments, or
     creating and updating environment-variable values.
5. If `data_apps_tool` is unavailable, report that the Cloud Apps MCP
   capability is not enabled. Do not bypass it with a direct API request.

Never ask the user to paste an environment-variable value or secret into chat.
For a create or update, route to the installed Webflow CLI's built-in help and
require a hidden prompt, stdin, or protected file. Do not guess a CLI command.

### 2. Resolve the target

Discover identifiers in this order:

```text
list_apps -> app_id
list_environments(app_id) -> env_id
list_deployments(app_id, env_id) -> deployment_id
```

Use an identifier supplied by the user only after verifying it through the
corresponding get or list action. Use exact filters when available. If a list
action returns `nextCursor`, pass it back as `cursor` until `nextCursor` is null
whenever absence or completeness matters.

If multiple resources match, present distinguishing metadata and require the
user to select one before any mutation. Auto-select only when one resource is
unambiguous.

### 3. Follow the matching user story

#### Which app and environment am I looking at?

1. Use `list_apps` to find the app and `get_app` for its metadata.
2. Use `list_environments` to report the branch, mount, deploy URL, and latest
   deployment status exposed by the live response.
3. Use `get_app_domains` when the user asks where the app is reachable.
4. Explain that custom-domain results exclude the default `*.webflow.io`
   hostname. Domains for an app attached to a regular Webflow site may belong
   to the parent site and be shared by sibling apps.

#### What is deployed, and is it healthy?

1. Use `list_environments` for the environment's latest deployment status.
2. Use `list_deployments`, newest first, then `get_deployment` for the selected
   deployment's detailed timeline and version metadata.
3. Treat `starting`, `building`, and `deploying` as active states. Report any
   other status exactly rather than guessing its meaning.
4. A failed phase sets `buildFailedAt` or `deployFailedAt` while its matching
   finished timestamp remains null. A null finished timestamp by itself does
   not prove the phase is still running.
5. Report what is observable: selected app and environment, deployment status,
   version or commit metadata if returned, phase timestamps, and evidence gaps.

#### Why did the deployment fail?

1. Fetch the deployment with `get_deployment` and identify the failed phase
   from its status and timestamps.
2. Call `get_build_logs` only when `logsAvailable` is true. Start with a narrow
   `since` window or `q` filter, then broaden only if needed.
3. Page until `nextCursor` is null when a complete result is required.
4. Treat `logsAvailable` as a retention and retrieval signal, not proof that
   every phase produced log entries.
5. Treat an empty result as "no matching retrievable server-side logs," not as
   proof that the build succeeded or produced no errors.
6. Build output produced on a user's machine is outside MCP. Mention this only
   when the user says the deployment was built with the CLI; direct them to the
   originating CLI output for local build failures.
7. Report the failed phase, relevant timestamps, the smallest useful evidence,
   the inferred cause, and any uncertainty. Do not merely restate raw logs.

#### Why is the running app failing?

1. Resolve the exact environment and call `get_runtime_logs`.
2. Narrow by `since` and `q` before retrieving a broad window. Page completely
   when the conclusion depends on absence.
3. Runtime logs are retained for approximately one hour on the base plan. An
   empty result outside the retained window is expected.
4. Correlate runtime evidence with the latest deployment record when useful,
   but do not claim causation from timing alone.
5. Report the observed error pattern, affected interval, likely cause, evidence,
   and limitations.

#### Is required configuration present?

1. Resolve the environment and call `list_variables`.
2. Report keys and metadata only. Secret entries have `isSecret: true` and no
   value; a missing secret value is expected.
3. If a key is absent, exhaust pagination before concluding it is missing.
4. If the value must be created or changed, stop the MCP workflow and route to
   `webflow-cli:cloud` without requesting the value in chat.

#### Can this deployment be retried, rolled back, or rebuilt from branch HEAD?

Use the mutation's default dry run as the capability check. Do not infer
eligibility from missing logs, app metadata, or deployment metadata.

For a new deployment from the connected branch:

1. Resolve the environment and call `trigger_deployment` with its default dry
   run.
2. If preview rejects the target as unsupported, make no mutation and route the
   user to a fresh CLI deployment.
3. If preview succeeds, show the returned branch and explain that execution
   deploys its latest commit, not local files.
4. Require the user to type `confirm`.
5. Generate one stable `idempotency_key`, execute with `dry_run: false`, and
   reuse that key for every retry.
6. The action returns no deployment ID. Poll `list_deployments`, identify the
   new record, and use `get_deployment` until it leaves an active state or the
   bounded monitoring period ends.

For a retry or rollback:

1. Select the exact prior deployment and call `redeploy` with its default dry
   run.
2. If preview rejects the target as unsupported, make no mutation and route the
   user to a fresh CLI deployment.
3. If preview succeeds, show the returned commit hash and message. Explain that
   this creates a fresh build at that commit.
4. Require `confirm`, execute with `dry_run: false` and a stable
   `idempotency_key`, then poll as described above.

### 4. Apply shared evidence and safety rules

- Treat build, deploy, and runtime logs as potentially sensitive customer
  output. Inspect for tokens, credentials, cookies, authorization headers, and
  presigned URLs before quoting or saving them.
- Quote only the minimum log evidence needed. Redact sensitive values and URLs.
- Never conclude that a paginated resource is absent after one page.
- Never translate an empty list into a tool failure.
- The live action schema is authoritative for arguments and response fields.
  Never fabricate IDs, fields, statuses, branches, commits, or live URLs.
- A request to inspect, diagnose, or preview does not authorize a mutation.
- Require an itemized preview and the exact word `confirm` before every
  mutation.
- Reconcile an uncertain mutation through observable state before retrying it.

### 5. Handle explicit administrative requests

These operations are supported but are not the skill's primary workflow.

For `update_app`:

1. Fetch the current app with `get_app`.
2. Show the exact name or description change and require `confirm`.
3. Call `update_app`, then verify with `get_app`.
4. Pass `description: null` to clear a description. Do not use an empty string.

For `delete_variable`:

1. Preview with the default dry run.
2. If `exists` is false, report that nothing was deleted and stop.
3. If `exists` is true, show the app, environment, and key; warn that deletion
   is permanent and require `confirm`.
4. Call once with `dry_run: false`. Treat `deleted: true` as success even if the
   backend message is absent.

For `delete_app`:

1. Preview with the default dry run and report `deletionMode`.
2. Explain that `archive` unpublishes the app and removes it from the dashboard,
   while `hard_delete` permanently deletes the app and all its environments and
   cannot be undone.
3. Require `confirm`, then call once with `dry_run: false`.
4. Treat `deleted: true` as success even when the resource cannot be fetched
   afterward.

### 6. Handle errors and report

- `401` or `403`: report the authentication or permission problem; do not
  retry.
- `404`: verify the complete app -> environment -> deployment chain; do not
  silently switch targets.
- `429`: honor the backoff signal before a bounded retry.
- `5xx` on a read: retry a bounded number of times.
- `5xx` on a mutation: treat the outcome as uncertain and reconcile it before
  considering a retry.
- Rejected cursor: restart that listing without the cursor and page again.
- `GITHUB_APP_NOT_INSTALLED`: provide the returned `installUrl`, require the
  user to reconnect GitHub, and retry only after reconnection.
- An unsupported deployment preview is a capability boundary, not a reason to
  bypass MCP with a direct API call.

Final reports must state the selected app and environment, evidence inspected,
observed status, inferred cause when supported, confidence or limitations, any
remediation performed, and the next required user action only when blocked.

## Examples

### Diagnose a failed deployment

**User:** "Why did the latest production deployment fail?"

1. Resolve the app and production environment.
2. Fetch the latest deployment and inspect its status and timeline.
3. If `logsAvailable` is true, retrieve narrowly filtered build/deploy logs.
4. Redact sensitive content and report the failed phase, evidence, likely root
   cause, and limitations.
5. If the logs are empty, report that no matching server-side logs are
   retrievable; do not call that evidence of success.

### Diagnose a known CLI build failure

**User:** "I deployed with the CLI and the build failed. What went wrong?"

Explain that the client-side build output is not sent to Webflow. Inspect the
deployment record and any available server-side deployment evidence, then use
the originating CLI output for the local build failure. Do not infer the local
failure from empty MCP logs.

### Retry a failed deployment

**User:** "Retry the failed production deployment."

1. Resolve the exact failed deployment.
2. Preview `redeploy` with its default dry run.
3. If supported, show the exact commit and require `confirm` before executing.
4. If unsupported, make no mutation and route to a fresh CLI deployment.
5. After execution, poll and report the new deployment's status.

### Check or set configuration

**User:** "Is `DATABASE_URL` configured in production?"

List variable metadata and report whether the key exists without exposing a
value. If the user then asks to set it, route to `webflow-cli:cloud` and keep the
value outside chat.

## Guidelines

- Start from the user's operational question, not the action inventory.
- Prefer observable evidence over assumptions about how an app was built.
- Use mutation previews and returned errors as capability checks.
- Use CLI for app creation, local builds and deployments, and variable writes.
- Never use `data_apps_tool` for Designer variables.
- Never expose secrets from variables, logs, errors, or URLs.
- Never mutate without an exact preview and explicit `confirm`.
- Never retry an uncertain mutation before reconciling observable state.
