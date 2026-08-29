---
name: webflow-cli:cloud
description: Create, build, and deploy Webflow Cloud apps from the CLI (site-attached or project apps), and manage existing ones — apps, domains, environments, deployments, build/runtime logs, and environment variables including secrets. Use when initializing or deploying a Cloud app, importing an existing GitHub repository, setting up CI/CD (GitHub Actions or GitHub-linked deploys), setting or importing secrets, retrying or rolling back a deployment, diagnosing a failed build, or resolving app/environment/workspace IDs from webflow.json or env vars. The `webflow apps` namespace is beta and requires the CLI's `@next` channel.
---

# Webflow Cloud

Initialize new projects from templates or an existing GitHub repository, deploy to Webflow Cloud, and manage existing apps (list, inspect, logs, deployments, environments, environment variables). Deploys support two modes: **site-attached** (deploy to an existing Webflow site) and **project app** (deploy as an independent app, no existing site required).

## Beta: `webflow apps` requires `@next`

**Every `webflow apps …` command in this skill ships only on the CLI's beta channel, `@webflow/webflow-cli@next`.** The whole namespace is gated behind the beta build; on the stable `@latest` build, `webflow apps` does not exist at all and any invocation fails with an unknown-command error.

```bash
# Required for every `apps` command in this skill:
npm install -g @webflow/webflow-cli@next

# Confirm the beta channel is installed — a beta version carries a `-next.` suffix
# (e.g. 1.14.0-next.3). A bare semver (e.g. 1.13.1) is the stable channel.
webflow --version
```

**On stable (`@latest`), only the `cloud` namespace exists**, and it covers `init` / `deploy` / `create` / `list` — there is no stable equivalent for any of the management commands (`apps list`, `get`, `domains`, `link`, `update`, `delete`, `environments`, `deployments`, `logs`, `env-vars`). If the user is on `@latest` and asks for anything under "Managing apps" below, tell them it requires `@next` rather than guessing an alternative.

A subset of the beta commands is gated a second time and will need its own promotion even after the namespace goes GA — see [Beta gating tiers](#beta-gating-tiers).

## Namespaces: `apps` (beta, canonical) vs `cloud` (stable, being deprecated)

`webflow apps <command>` is the **canonical** namespace Webflow Cloud is moving to, currently **beta-only**. `webflow cloud <command>` is what stable users have today; the `init` / `deploy` forms are **aliases of the same handler** and will be deprecated once `apps` reaches GA.

| Canonical (`@next` only)                                                                                                              | Stable alias (`@latest` + `@next`) | Notes                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `webflow apps init`                                                                                                                   | `webflow cloud init`               | Same options + handler — **except** `--import` and its repo-intake flags, which attach to `apps init` **only**, on `@next`.                                      |
| `webflow apps deploy`                                                                                                                 | `webflow cloud deploy`             | Same options + handler.                                                                                                                                          |
| —                                                                                                                                     | `webflow cloud create <name>`      | Deprecated on both channels; prefer `apps init` (or `cloud init` on stable).                                                                                     |
| —                                                                                                                                     | `webflow cloud list`               | Lists **scaffold templates**, not apps. Stays under `cloud`; there is **no** `apps` equivalent. Do not confuse with `apps list`, which lists workspace **apps**. |
| `webflow apps list` / `get` / `domains` / `link` / `update` / `delete` / `environments …` / `deployments …` / `logs …` / `env-vars …` | —                                  | **No stable equivalent.** Beta-only.                                                                                                                             |

On a beta build, `cloud init` / `cloud deploy` print a one-time deprecation notice on stderr pointing at the `apps` form (suppressed with `--json`). On a stable build that notice is **not** printed — the CLI never advertises a namespace the user doesn't have.

Prefer the `apps` forms in all new work when the user is on `@next`. This skill shows `apps` commands throughout; every `apps init` / `apps deploy` invocation can be run as `cloud init` / `cloud deploy`, with identical flags, apart from `--import`.

### Beta gating tiers

**Today this distinction changes nothing — everything below needs `@next`.** It matters only for what reaches stable first, so treat it as forward-looking context, not as a capability check.

The beta commands sit behind two independent gates:

| Tier               | Commands                                                                                                                                                                                                              | Reaches stable when                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Namespace gate** | `apps init` (incl. `--import`), `deploy`, `list`, `get`, `domains`, `environments list`, `deployments list` / `get` / `redeploy` / `trigger`, `logs build` / `runtime`, `env-vars list` / `set` / `delete` / `import` | The `apps` namespace is promoted.                                                    |
| **Second gate**    | `apps link`, `apps update`, `apps delete`, `apps environments create` / `update` / `delete`                                                                                                                           | **Separately promoted** — removing the namespace gate alone does **not** ship these. |

Until both are lifted, assume every `apps` command requires `@next`.

## Instructions

### Step 0: Verify CLI is installed

```bash
webflow --version
```

If the command is not found, install it. **Install `@next`, not `@latest`, for anything in this skill under `webflow apps`** — the whole namespace is beta-only:

```bash
npm install -g @webflow/webflow-cli@next
# or yarn global add @webflow/webflow-cli@next
# or pnpm add -g @webflow/webflow-cli@next
```

If the user only needs `webflow cloud init` / `cloud deploy`, `@latest` is sufficient — swap `@next` for `@latest` above.

A beta install reports a `-next.` version suffix (`1.14.0-next.3`); a stable install reports a bare semver (`1.13.1`). If `webflow --version` shows a bare semver and the user asks for an `apps` command, reinstall from `@next` before doing anything else — every `apps` invocation will otherwise fail as an unknown command.

Then proceed to state detection.

### Step 1: Detect project state

Run both checks before deciding which path to follow:

```bash
# Is this project already set up on Webflow Cloud?
cat webflow.json

# Is there a git remote?
git remote get-url origin 2>/dev/null
```

**Quick reference** (the CLI now writes `cloud.app_id`; older manifests may carry the legacy `cloud.project_id`, which is still read as a fallback):

| `cloud.app_id` in `webflow.json` (or legacy `cloud.project_id`) | git remote | → Path                           |
| --------------------------------------------------------------- | ---------- | -------------------------------- |
| No                                                              | —          | **A** — new project              |
| Yes                                                             | No         | **B** — existing project, no git |
| Yes                                                             | Yes        | **C** — ideal state              |

---

> **You are running without a TTY.** The CLI's interactive prompts only fire when `process.stdin.isTTY` is true. As an agent invoking the CLI through a subprocess, you do not have a TTY — every prompt is silently skipped, and any required value that wasn't passed as a flag triggers a hard error like `--app-name cannot be empty`.
>
> **Rule for every command in this skill:** pass all required flags explicitly. Never rely on prompts. Pass `--no-input` when the CLI accepts it to make this contract explicit. The required flag set per command:
>
> | Command                                   | Always pass                                                                                      |
> | ----------------------------------------- | ------------------------------------------------------------------------------------------------ |
> | `apps init` (site-attached)               | `--no-input --app-name <3–39 chars> --framework <astro\|nextjs> --mount <path> --site-id <id>`   |
> | `apps init --new` (app)                   | `--no-input --app-name <3–39 chars> --framework <astro\|nextjs> --workspace-id <id>`             |
> | `apps init --import` (site-attached)      | `--no-input --import <repo-url> --site-id <id> --mount <non-root path> --idempotency-key <key>`  |
> | `apps init --import --new` (project app)  | `--no-input --import <repo-url> --new --idempotency-key <key>` — **no `--mount`**                |
> | `apps deploy` (site-attached)             | `--no-input --mount <path> --environment <env> --site-id <id>` plus `--app-name` on first deploy |
> | `apps deploy` (project app, first deploy) | `--no-input --mount <path> --environment <env> --workspace-id <id> --app-name <name>`            |
>
> `--site-id`, `--app-id`, `--framework`, and `--workspace-id` on `apps deploy` let agents override what's in `webflow.json` at deploy time.
>
> **Multi-workspace tokens used to be an agent-fatal hang** because workspace selection had no non-TTY path. Now pass `--workspace-id` to skip the picker. **The workspace ID is not surfaced anywhere in the Webflow dashboard UI** — users can't look it up by hand. If the agent doesn't have it, ask the user to run `webflow apps deploy` interactively once from inside their project. The preflight prompts for workspace selection and writes `cloud.workspace_id` to `webflow.json`; from that point the agent can read it from the manifest and pass `--workspace-id` on subsequent runs. Do **not** suggest `apps init --new` for ID discovery — on an existing project it creates a discarded scratch directory. **Exception:** in Path A2 (empty directory) it _is_ safe to try `apps init --new` without `--workspace-id` to auto-resolve a single-workspace token — see [Path A2](#path-a2-empty-directory-scaffold-from-scratch).
>
> **Site IDs are visible in the dashboard.** When `--site-id` is needed but unknown, do not ask the user for a raw `site_XXXX` value — use [`webflow sites list`](#picking-a---site-id-from-a-list) to fetch their sites and present a picker keyed by display name. Users can still check their dashboard to fetch it.
>
> **Read/manage commands don't need `--workspace-id`.** The `apps list` / `get` / `domains` / `environments` / `deployments` / `logs` / `env-vars` commands derive the workspace server-side from the OAuth token — they have **no** `--workspace-id` flag and never prompt for a workspace. See [Managing apps](#managing-apps).

---

### Path A: No `app_id` — new project

The project has not been deployed yet. **Before doing anything else, ask the user two questions:**

> 1. "Do you already have source code for this project (an existing Next.js or Astro codebase), or are you starting from an empty directory and want a Webflow starter scaffold?"
> 2. If they have code: **"Is it already pushed to a GitHub repository, and do you want Webflow to build from that repo (rather than from your local files)?"**

Those answers choose the branch — and the three are meaningfully different:

| User has...                                                                         | Branch      | Init step                                                                                                                                                      |
| ----------------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Existing code**, deploying from **local files**                                   | **Path A1** | **Skip `apps init`.** It would create a `./<app-name>/` subfolder with a hello-world scaffold inside their repo, which they don't want.                        |
| **Empty directory** or wants a Webflow starter                                      | **Path A2** | Run `apps init` to scaffold from `Webflow-Examples/hello-world-*`.                                                                                             |
| **Existing code already on GitHub**, wants Webflow to **build from the repository** | **Path A3** | Run `apps init --import <repo-url>` — creates a **GitHub-connected** app bound to the repo. Beta (`@next`) and `apps`-only; there is no `cloud init --import`. |

**The A1 vs A3 choice is not cosmetic — it decides what the app can do later.** A GitHub-connected app (A3) can use `apps deployments trigger` / `redeploy`, and is the only kind eligible for dashboard push-to-deploy. An app first created by a local `apps deploy` (A1) is **not** GitHub-connected, so `trigger` / `redeploy` refuse it. If the user's code is already on GitHub and they say anything about CI, automatic deploys, rollbacks, or "deploy when I push", route to **A3**, not A1.

Recoverable either way: an A1 app can be pointed at a repo afterwards with `apps update --github-source <repo-url>` (see [apps update](#apps-update-appid)) — but choosing A3 up front avoids the extra step.

After the branch decision, also ask **site-attached vs app** (only relevant before the first deploy):

| User says...                                                                       | Mode              | Outcome                                                                                                          |
| ---------------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| "deploy to my Webflow site `<name>`", "site-attached", references an existing site | **Site-attached** | App is bound to an existing Webflow site; site URL hosts the app at the chosen mount path. Requires `--site-id`. |
| "project app", "just an app", "no site", or no existing site mentioned             | **Project app**   | First deploy provisions a brand-new Webflow site (`<app-name>-<hash>.webflow.io`).                               |

If the user is ambiguous on either question, **ask**. Do not default.

---

#### Path A1: existing codebase, deploying from local files

> **Check A3 first if the code is on GitHub.** This path uploads and builds **local files**, producing an app that is **not** GitHub-connected — `apps deployments trigger` / `redeploy` and dashboard push-to-deploy will all refuse it. If the repo is on GitHub and the user wants Webflow to build from it, use [Path A3](#path-a3-existing-github-repository-github-connected-app) instead.

The user has working source. `apps deploy` handles everything — framework detection runs against `package.json`, and the preflight phase resolves identity from flags or prompts the user. No `apps init` needed, no `webflow.json` to hand-write up front.

**Step 1: One-time auth (human-only).** Tell the user to run this locally; agents cannot drive the browser flow:

```bash
webflow auth login
```

**Step 2: Deploy.** The exact form depends on what the agent knows.

**A1-a — Site-attached, `--site-id` is known:**

```bash
webflow apps deploy --no-input \
  --site-id site_abc123 \
  --app-name my-app \
  --framework nextjs \
  --mount /app \
  --environment main \
  --skip-mount-path-check \
  --skip-update-check
```

`--framework` is optional if `package.json` has the framework's Cloudflare adapter (`@opennextjs/cloudflare`, `@astrojs/cloudflare`). Pass it explicitly for monorepos or when auto-detection is unreliable.

If the agent doesn't know the user's `--site-id`, do **not** ask for a raw `site_XXXX` value — use [`webflow sites list`](#picking-a---site-id-from-a-list) to fetch the user's sites and present readable display names to pick from.

**A1-b — Project app, `--workspace-id` is known:**

```bash
webflow apps deploy --no-input \
  --workspace-id ws_abc123 \
  --app-name my-app \
  --framework nextjs \
  --mount / \
  --environment main \
  --skip-mount-path-check \
  --skip-update-check
```

**A1-c — Project app, workspace ID is unknown** (the common gap):

**The workspace ID is not visible anywhere in the Webflow dashboard UI.** Users cannot look it up by hand — the only way to discover it is to run the CLI. So the path is:

**Ask the user to run one interactive deploy locally.** From inside their project directory:

```bash
webflow apps deploy
```

With no `--no-input` and no identity flags, the preflight prompts: _"This project isn't initialized for Webflow Cloud. How would you like to deploy?"_ → user picks "Create a new app" → workspace picker → done. After this one human-driven deploy, `cloud.workspace_id` and `siteId` are written to `webflow.json` and `WEBFLOW_SITE_ID` to `.env`. The agent can then run all subsequent deploys with `--site-id` (the newly provisioned site).

> Do **not** ask the user to run `apps init --new` to "discover" their workspace ID. On an existing project that creates a discarded `./<app-name>/` scratch directory with a hello-world scaffold inside the user's repo. Use the interactive `apps deploy` path above — it discovers the workspace ID _and_ completes the first deploy in the same step.

**Step 3: Set up git** (if not already) — same as Path A2 step 3 below.

---

#### Path A2: empty directory, scaffold from scratch

1. **Scaffold the project** — pick the form that matches the user's intent:

   ```bash
   # Project app (no site attachment). --workspace-id avoids the multi-workspace hang.
   webflow apps init --new --no-input \
     --app-name my-app \
     --framework astro \
     --workspace-id ws_abc123
   ```

   ```bash
   # Site-attached (connect to an existing Webflow site). Requires --site-id.
   webflow apps init --no-input \
     --app-name my-app \
     --framework astro \
     --mount /app \
     --site-id site_abc123
   ```

   See [`apps init`](#webflow-apps-init) for all flags.

   **Workspace ID discovery for project apps in Path A2 only:** because Path A2 starts from an empty directory, `apps init --new` creates a fresh scaffold either way — there's nothing to pollute. So if the agent doesn't have `--workspace-id`, it's safe to **try `apps init --new` without it first**:

   ```bash
   # Try this first if --workspace-id is unknown (Path A2 only — empty dir)
   webflow apps init --new --no-input \
     --app-name my-app \
     --framework astro
   ```

   - **Single-workspace tokens:** the CLI auto-selects the only workspace, writes `cloud.workspace_id` to `webflow.json`, and exits 0. Read it back from the manifest and pass it as `--workspace-id` to `apps deploy` in step 2.
   - **Multi-workspace tokens:** the workspace picker fires and the command hangs (no TTY). **Set a 30-second timeout on the Bash call** (or wrap the command in `timeout 30s ...`) — a successful single-workspace init completes in 10–20 seconds (OAuth check + `GET /v2/workspaces` + scaffold download from GitHub), so anything past 30s with no output is the picker hanging. Once the timeout fires, ask the user for the workspace ID directly and re-run with `--workspace-id`.

   For **site-attached** in Path A2, there is no equivalent auto-discovery — `--site-id` is always required up front. Use the [site picker](#picking-a---site-id-from-a-list) pattern below to help the user pick.

   **Path A1 (existing codebase) does not get this trick.** Running `apps init --new` in an existing project creates a discarded scratch subdirectory. The Path A1 workspace-ID discovery path stays as documented in Path A1-c.

---

#### Path A3: existing GitHub repository, GitHub-connected app

The user's code is already on GitHub and they want Webflow to build **from the repository** rather than from local files. `apps init --import <repo-url>` creates the app bound to that repo and clones it locally.

> **Beta, `apps`-only.** `--import` exists only on `@webflow/webflow-cli@next`, and only under `apps init` — there is deliberately no `cloud init --import`. If the user is on `@latest`, either move them to `@next` or fall back to [Path A1](#path-a1-existing-codebase-deploying-from-local-files) and attach the repo later with `apps update --github-source`.

**Step 0: Prerequisite — the Webflow GitHub App.** It must be installed on the repository owner and connected to the workspace. **The CLI cannot do this**; it's dashboard/GitHub-side setup. If the import fails on permissions, this is the first thing to check.

**Step 1: One-time auth (human-only).** Same as A1 — agents cannot drive the browser flow:

```bash
webflow auth login
```

**Step 2: Import.** Exactly one of `--site-id` or `--new` is required — the CLI will **not** infer the target from anything inside the repo.

**A3-a — Site-attached** (`--mount` is **required** and must be non-root):

```bash
webflow apps init --import https://github.com/acme/site \
  --site-id 6234abc --mount /app --dry-run

webflow apps init --import https://github.com/acme/site \
  --site-id 6234abc --mount /app
```

**A3-b — Project app** (`--mount` is **not allowed** — a project app owns the root of its own domain):

```bash
webflow apps init --import https://github.com/acme/site --new
```

**A3-c — Non-interactive / CI.** `--idempotency-key` is **required** here. Use a retry-stable key unique to this repo + target (e.g. `$GITHUB_RUN_ID-$REPOSITORY-$SITE_ID`) so a retry replays the original app instead of creating a second one:

```bash
webflow apps init --import https://github.com/acme/site --new --no-input \
  --idempotency-key "$GITHUB_RUN_ID-acme-site" \
  --branch main --json
```

Add `--skip-clone` to register the app without writing anything to the filesystem — the app and environment IDs are printed instead. Useful when the repo is already checked out, or when running somewhere you don't want a clone.

`--branch` picks which branch builds; it defaults to the repository's default branch.

**Step 3: Enable push-to-deploy (dashboard, manual).** The import connects the app to the repo, but **pushing does not deploy until the dashboard wiring is done** — see the [full workflow example](#full-workflow-scaffold--github--dashboard-connection--push-to-deploy-recommended), steps 3 onward. Until then, build on demand:

```bash
webflow apps deployments trigger --json
```

**Do not run `apps deploy` on an A3 app to "push an update".** That uploads local files and is the A1 model; for a GitHub-connected app the equivalents are `deployments trigger` (build current HEAD) and `deployments redeploy <depId>` (re-run a past commit, i.e. roll back).

#### Picking a `--site-id` from a list

When `--site-id` is needed (Path A1 site-attached, Path A2 site-attached, or anywhere else) and the user hasn't given one, use `webflow sites list --json` to enumerate sites the token can see, then present a short list of readable names for the user to choose from. The site ID is visible in the Webflow dashboard URL config, but a numeric-ID prompt is bad UX; surface display names instead unless asked for IDs.

```bash
# Returns a JSON array of sites with id, displayName, lastPublished, etc.
webflow sites list --json
```

Workflow:

1. Run `webflow sites list --json`. The CLI exits 0 with a JSON array.
2. Parse the output. Show the user a short list keyed by `displayName` (and `lastPublished` if the user has many sites). Example:

   ```
   Which site should this project deploy to?

   1. Acme Marketing  (last published 2 days ago)
   2. Acme Docs       (last published 3 weeks ago)
   3. Acme Internal   (never published)
   ```

3. Map the user's pick back to its `id` field. Pass that as `--site-id`.

If `webflow sites list` errors (auth missing / expired), surface the error and ask the user to run `webflow auth login` locally; do not try to drive it from the agent.

2. **Deploy:** pick the form matching the init form above. Pass `--site-id` (or `--workspace-id` for project-app first deploy) so the deploy can't misread the manifest if something is half-written.

   ```bash
   # Project-app first deploy — provisions the Cloud site/app/env
   webflow apps deploy \
     --no-input \
     --app-name my-app \
     --workspace-id ws_abc123 \
     --mount / \
     --environment main \
     --skip-mount-path-check \
     --skip-update-check
   ```

   ```bash
   # Site-attached first deploy — uses the existing Webflow site
   webflow apps deploy \
     --no-input \
     --app-name my-app \
     --site-id site_abc123 \
     --mount /app \
     --environment main \
     --skip-mount-path-check \
     --skip-update-check
   ```

   This creates the app on Webflow Cloud and sets `cloud.app_id` in `webflow.json`. Commit the updated `webflow.json`.

3. **Set up git** (if not already):

   ```bash
   git init && git add . && git commit -m "init"
   git remote add origin https://github.com/your-org/my-app.git
   git push -u origin main
   ```

4. **(Optional) Enable push-to-deploy via the Webflow dashboard.** Pushing to GitHub alone does **not** trigger deploys — that wiring lives in the Webflow dashboard, not in the CLI or the repo. Tell the user:

   1. Open the Webflow dashboard → their Cloud app → **Settings** → **Git**
   2. Connect their GitHub account, then select the repository and branch
   3. Confirm — the dashboard runs one initial deploy automatically to verify the connection
   4. From that moment on, every push to the connected branch triggers a deploy

   The CLI cannot perform any of these steps. If the user skips this, every deploy must be a manual `webflow apps deploy` invocation (Path B–style) or a CI/CD pipeline.

> If a deploy auth error occurs in step 2: run `webflow auth login`, complete the browser flow, then retry.

---

### Path B: `app_id` exists, no git remote — existing project, no git

The project is already on Webflow Cloud but has no git repo. Deploy directly and nudge toward git setup.

1. **Deploy:** read `webflow.json` first. If `siteId` is set, pass `--site-id` matching it. If only `cloud.workspace_id` is set, pass `--workspace-id` matching it.

   ```bash
   webflow apps deploy \
     --no-input \
     --site-id site_abc123 \
     --mount / \
     --environment main \
     --skip-mount-path-check \
     --skip-update-check
   ```

2. **Nudge toward push-to-deploy:** suggest the user initialize a git repo, push to GitHub, **and then connect the repo in the Webflow dashboard** (app → Settings → Git). The dashboard step is what activates push-to-deploy — the CLI can't do this. See Path A, steps 3–4.

> If a deploy auth error occurs: run `webflow auth login`, complete the browser flow, then retry step 1.

---

### Path C: `app_id` exists + git remote — possibly ideal

The project is deployed and has a git remote, **but the existence of a remote is not proof that push-to-deploy is wired up.** That wiring is a dashboard-side connection that the CLI can't introspect. Confirm before suggesting anything.

> **Always ask the user:** _"Is this repo connected to your Webflow Cloud app in the dashboard (app → Settings → Git, with a branch selected)?"_ The answer changes the recommendation:
>
> - **Yes, connected** — push-to-deploy is active. The only action needed is `git push`. Do not suggest re-linking or re-deploying.
> - **No, not connected** — `git push` does nothing on the Webflow side. Either run a manual deploy now, or have the user connect the repo in the dashboard first to activate push-to-deploy for future commits.
> - **Don't know** — assume not connected and recommend the dashboard connection (one-time setup, then push-to-deploy is permanent).

1. **If connected** — just commit and push:

   ```bash
   git add .
   git commit -m "your message"
   git push
   ```

   Webflow Cloud picks up the push and deploys automatically. The first deploy after connection is run by the dashboard itself; subsequent pushes are picked up automatically.

2. **If not connected** — two routes:

   - **Activate push-to-deploy for future commits** (recommended). Tell the user to open the Webflow dashboard → their Cloud app → **Settings** → **Git**, connect the repo, select the branch. The dashboard runs an initial deploy automatically to verify the connection. From then on, every `git push` to that branch deploys.
   - **One-off manual deploy now**, without enabling push-to-deploy. Pass `--site-id` matching the `siteId` in `webflow.json`:
     ```bash
     webflow apps deploy \
       --no-input \
       --site-id site_abc123 \
       --mount / \
       --environment main \
       --skip-mount-path-check \
       --skip-update-check
     ```
     This deploys the current state but does **not** wire up push-to-deploy. The next `git push` will still be a no-op on the Webflow side.

> If a deploy auth error occurs: run `webflow auth login`, complete the browser flow, then retry.

### Tool usage

- Use the **Bash tool** for all `webflow apps` / `webflow cloud` commands
- Use the **Read tool** to examine `webflow.json`, `package.json` — never modify these directly
- Use the **Glob tool** to discover project files
- **Do not** use Webflow MCP tools for CLI workflows

### Authentication

```bash
# Interactive — local-only, opens a browser. NOT for agents or CI.
webflow auth login
```

> `webflow auth login` performs an OAuth flow in the user's browser and then writes the token to `.env`. It refuses to run with `--no-input` (exits with `No-input mode enabled. Aborting OAuth authentication`). **Agents cannot drive this command.** If `webflow auth login` is needed (missing or expired token), ask the user to run it locally once and report back when it's done.

The CLI writes the same token env var for **both** modes. There is no per-mode split.

**`webflow auth login` writes to `.env`:**

| Variable            | Always written?                                        | Description                                                                                                                                |
| ------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `WEBFLOW_API_TOKEN` | Yes (both modes)                                       | OAuth access token. The canonical token env var. Set by `webflow auth login`.                                                              |
| `WEBFLOW_SITE_ID`   | Site-attached only (or after first project-app deploy) | Site ID. Written by `apps init` for site-attached projects, or by `apps deploy` for project apps after the first deploy provisions a site. |

After the **first project-app deploy**, the CLI provisions a site on the backend and writes `WEBFLOW_SITE_ID` to `.env`. From that point on, the project behaves like a site-attached project — but the token env var is still `WEBFLOW_API_TOKEN`.

**Deprecated legacy:** `WEBFLOW_SITE_API_TOKEN` (and `WEBFLOW_WORKSPACE_API_TOKEN`) are read-only legacy fallbacks. The CLI never writes them, but if it finds one of them set in the environment when `WEBFLOW_API_TOKEN` is not set, it uses the legacy value **and prints a deprecation warning on every run**. Do not put `WEBFLOW_SITE_API_TOKEN` in `.env` or CI secrets for new projects — use `WEBFLOW_API_TOKEN`.

Other env vars (any mode):

| Variable                     | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| `DO_NOT_TRACK`               | Set to `1` to opt out of telemetry.                      |
| `WEBFLOW_SKIP_UPDATE_CHECKS` | Set to `true` to skip the @webflow package update check. |

> **`WEBFLOW_SITE_ID` env var is read-only.** Used at runtime when no flag or manifest value is set, but never written back to `webflow.json`. Setting `WEBFLOW_SITE_ID=X` in `.env` will not update the manifest — only `apps init`, `apps deploy`, and the manifest itself drive that.

> **GitHub Secrets:** use `WEBFLOW_API_TOKEN` for the token in every mode. Also set `WEBFLOW_SITE_ID` for site-attached projects and project apps that have already had their first deploy. Never commit `.env` files. If existing CI uses `WEBFLOW_SITE_API_TOKEN`, rename it — the deploy will still succeed but every run prints a deprecation warning until you switch.

### Configuration — webflow.json

```json
{
  "siteId": "site_abc123",
  "cloud": {
    "app_id": "app_xyz",
    "environment_id": "env_xyz",
    "workspace_id": "ws_xyz",
    "framework": "nextjs",
    "skipMountPathCheck": false
  }
}
```

All `cloud.*` keys are **snake_case** (`app_id`, not `appId`).

| Key                        | When set                                                                                | Notes                                                                                                                                                                                        |
| -------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `siteId`                   | Site-attached: at `apps init`. Project app: after first deploy (CLI provisions a site). | Absent on project apps that have not been deployed yet.                                                                                                                                      |
| `cloud.framework`          | At `apps init`.                                                                         | Required for deploy resolution — see below.                                                                                                                                                  |
| `cloud.app_id`             | After first deploy.                                                                     | **Canonical.** Auto-written. Replaces the legacy `cloud.project_id`.                                                                                                                         |
| `cloud.project_id`         | Legacy only.                                                                            | **Deprecated.** Read as a fallback when `cloud.app_id` is absent (manifests created before the Project → App rename). New deploys never write it; will be removed in a future major release. |
| `cloud.environment_id`     | After first **project-app** deploy.                                                     | Auto-written by `createCloudApp`.                                                                                                                                                            |
| `cloud.workspace_id`       | At project-app `apps init` (`--new`).                                                   | Used by the first deploy to provision the site.                                                                                                                                              |
| `cloud.skipMountPathCheck` | User-managed.                                                                           | Equivalent to `--skip-mount-path-check`.                                                                                                                                                     |

The CLI also writes `cloud.deployment_type` (`"ssr" | "ssg" | "spa"`), `cloud.entrypoint_path`, and `cloud.framework_version` into the **bundled** `webflow.json` at build time (these power the cosmic deployer's wrangler config and telemetry). They're build-time outputs — do not strip them from the source `webflow.json` if you find them there; missing values silently break Next.js server-side deploys.

#### ID resolution and env vars

A shared resolver resolves `siteId`, `appId`, `environmentId`, and `workspaceId` in a **strict priority order**:

```
explicit flag / positional arg  >  env var  >  webflow.json manifest  >  interactive prompt  >  error
```

| Resource       | Flag / arg                         | Env var (read-only)          | `webflow.json`                                           |
| -------------- | ---------------------------------- | ---------------------------- | -------------------------------------------------------- |
| App ID         | `--app-id` / `[appId]` arg         | `WEBFLOW_APP_ID`             | `cloud.app_id` (falls back to legacy `cloud.project_id`) |
| Environment ID | `--environment-id` / `[envId]` arg | `WEBFLOW_APP_ENVIRONMENT_ID` | `cloud.environment_id`                                   |
| Site ID        | `--site-id`                        | `WEBFLOW_SITE_ID`            | `siteId`                                                 |
| Workspace ID   | `--workspace-id`                   | `WEBFLOW_WORKSPACE_ID`       | `cloud.workspace_id`                                     |

Env vars are **read-only** — they are never persisted back to the manifest. When a value comes from the manifest, the CLI logs a `Using <resource> from webflow.json` line (suppressed with `--json`). When nothing resolves and the command can't prompt (`--no-input`, `CI=true`, or no TTY), it exits with a machine-readable `missingFlag` on the error — see the `--no-input` contract in [Managing apps](#managing-apps).

**`cloud.framework` resolution at deploy time:**

1. **`webflow.json` exists with `cloud.framework`** — used as-is. Invalid value exits with code 1.
2. **`webflow.json` exists but `cloud.framework` is absent** — falls back to detecting from `package.json`.
3. **No `webflow.json`** — auto-detected from `package.json`. CLI **writes a new `webflow.json`** on success.

Projects created via `apps init` always land in case 1.

### Commands

#### webflow cloud list

```bash
webflow cloud list
```

Lists available **scaffold templates** (used by `init`). Check this before `apps init --framework` to confirm valid scaffold IDs. This is distinct from `apps list` (which lists your deployed apps) and lives only under the `cloud` namespace.

#### webflow apps init

Bootstrap a new app locally. Two modes: **site-attached** and **app**. (`webflow cloud init` is a deprecated alias with identical flags.)

**Site-attached** (connects to an existing Webflow site):

```bash
# Agent / non-TTY — always pass every flag
webflow apps init \
  --no-input \
  --app-name my-app \
  --framework nextjs \
  --mount /app \
  --site-id site_abc123

# Human at a real terminal — interactive prompts will fill in any missing flag
webflow apps init
```

Flags:

| Flag                      | Short | Description                                                                                                                                      |
| ------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--app-name <name>`       | `-n`  | App name. **Must be 3–39 characters** — the CLI rejects anything outside this range at init and at the first project-app deploy.                 |
| `--project-name <name>`   | —     | **Deprecated alias** of `--app-name`. Still accepted.                                                                                            |
| `--framework <framework>` | `-f`  | Must match a scaffold ID from `cloud list`. Currently: `nextjs`, `astro`.                                                                        |
| `--mount <path>`          | `-m`  | Mount path (default `/` for new domain, `/app` for existing site). Substituted into config files at scaffold time. Not stored in `webflow.json`. |
| `--site-id <id>`          | `-s`  | Required in non-interactive site-attached mode. Mutually exclusive with `--workspace-id`.                                                        |
| `--workspace-id <id>`     | `-w`  | Skips the workspace picker for `--new` (app mode). Mutually exclusive with `--site-id`.                                                          |
| `--new`                   | —     | Project-app mode (no site).                                                                                                                      |
| `--no-input`              | —     | CI mode. Requires `--app-name` and `--framework`. Without `--new`, defaults to app behavior.                                                     |

Credential resolution for `--no-input` site-attached: `--site-id` flag → `siteId` in `webflow.json` → `WEBFLOW_SITE_ID` env var → error.

After scaffolding a site-attached project, the CLI automatically runs a **DevLink sync**.

**Project app** (no site attachment):

```bash
# Agent / non-TTY — always pass --workspace-id to skip the workspace picker
webflow apps init --new --no-input \
  --app-name my-app \
  --framework nextjs \
  --workspace-id ws_abc123

# Human at a real terminal — prompts for workspace if not passed
webflow apps init --new
```

> If the token sees multiple workspaces and the agent doesn't have a workspace ID, ask the user to run `webflow apps deploy` interactively from inside their project — the preflight prompt picks a workspace and writes `cloud.workspace_id` to `webflow.json` for subsequent agent-driven runs. The workspace ID is not exposed in the Webflow dashboard UI, so the interactive CLI run is the only practical way to discover it.

|                                        | Site-attached                 | Project app (`--new`)                 |
| -------------------------------------- | ----------------------------- | ------------------------------------- |
| OAuth / site selection                 | Required at init              | Skipped (workspace selection instead) |
| `WEBFLOW_SITE_ID` in `.env`            | Written at init               | Written **after first deploy** only   |
| `WEBFLOW_API_TOKEN` in `.env`          | Written                       | Written                               |
| `cloud.workspace_id` in `webflow.json` | Not set                       | Set at init (used by first deploy)    |
| Scaffold                               | `astro`, `nextjs`             | `astro`, `nextjs`                     |
| Mount path                             | Configurable (default `/app`) | Always `/`                            |
| DevLink sync                           | Runs after init               | Skipped                               |

**Workspace selection (project-app mode only):** if `--workspace-id` is **not** passed, the CLI calls `GET /v2/workspaces` to enumerate workspaces the token has access to. Single workspace is auto-selected; multiple workspaces trigger an interactive picker. With `--workspace-id` the API roundtrip is skipped — the CLI trusts the flag and surfaces a 404 later via `createCloudApp` if it's invalid. The chosen ID is persisted as `cloud.workspace_id` in `webflow.json`.

**Agent caveat:** if the user's token sees more than one workspace and the agent can't pass `--workspace-id`, the picker fires and hangs in non-TTY contexts. The workspace ID is not visible in the Webflow dashboard UI, so the recovery is: **ask the user to run `webflow apps deploy` interactively once from inside their project.** The preflight prompt picks the workspace, completes a first deploy, and writes `cloud.workspace_id` (plus `siteId`, `app_id`, `environment_id`) to `webflow.json`. The agent can then read the workspace ID from the manifest and pass `--workspace-id` (or `--site-id`, now that the site exists) on subsequent runs. To target a different workspace later, delete `cloud.workspace_id` and have the user repeat the interactive deploy.

#### webflow apps init --import \<repo-url\> (beta, `apps` only)

Creates a Cloud app **from an existing GitHub repository** instead of a starter template, and clones it locally. This is the intake path for a codebase that already exists on GitHub — no scaffold is generated and no framework is chosen.

**This flag attaches to `apps init` only.** There is deliberately no `cloud init --import`: the repo-intake path creates real apps, so it stays on the beta-gated namespace rather than shipping through the stable alias.

**Prerequisite:** the **Webflow GitHub App must be installed on the repository and connected to your workspace.** Without it the create fails — the CLI cannot install it for you, and this is dashboard-side setup.

| Flag                      | Notes                                                                                                                                                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--import <repo-url>`     | `https://github.com/<owner>/<repo>`. Must be non-empty.                                                                                                                                                                          |
| `--site-id <siteId>`      | Attach to an existing site. **Mutually exclusive with `--new`; exactly one is required.**                                                                                                                                        |
| `--new`                   | Create a project app instead of attaching to a site.                                                                                                                                                                             |
| `--mount <path>`          | **Required (and non-root) with `--site-id`. Not allowed with `--new`** — a project app owns the root of its own domain, so it always mounts at `/`.                                                                              |
| `--branch <branch>`       | Branch to build. Defaults to the repository's default branch.                                                                                                                                                                    |
| `--idempotency-key <key>` | **Required for non-interactive runs** (CI, `--no-input`). Use a retry-stable key unique to this repo + target, e.g. `$GITHUB_RUN_ID-$REPOSITORY-$SITE_ID`, so a retry replays the original app instead of creating a second one. |
| `--skip-clone`            | Create the app without cloning locally. Nothing is written to the filesystem; the app and environment IDs are printed instead.                                                                                                   |
| `--json`                  | Import path only — the scaffold path has no single response object to serialize.                                                                                                                                                 |
| `--dry-run`               | Shared with the scaffold path: validate and preview without side effects.                                                                                                                                                        |

**A `siteId` found inside the repository is never used to pick the target** — you must say `--site-id` or `--new` explicitly.

The import-only flags (`--branch`, `--idempotency-key`, `--skip-clone`, `--json`) are **rejected, not ignored**, when `--import` is absent; likewise `--framework` / `--workspace-id` / `--project-name` are rejected _with_ `--import` (a repo brings its own code, and the workspace is derived from the token). Each refusal names the offending flag machine-readably via `missingFlag`, so an agent can correct the call without parsing prose.

```bash
# Attach an existing repo to an existing site at /app
webflow apps init --import https://github.com/acme/site \
  --site-id 6234abc --mount /app --dry-run

webflow apps init --import https://github.com/acme/site \
  --site-id 6234abc --mount /app

# Project app from a repo, CI-safe (note: --idempotency-key required, no --mount)
webflow apps init --import https://github.com/acme/site --new --no-input \
  --idempotency-key "$GITHUB_RUN_ID-acme-site" \
  --branch main --json

# Register the app without touching the local filesystem
webflow apps init --import https://github.com/acme/site --new --skip-clone --json
```

#### webflow cloud create (deprecated)

`webflow cloud create <name>` still works but **emits a deprecation warning** and will be removed in a future major release. It's hardcoded to `/app` mount in site-attached mode and offers a strict subset of `apps init`. Always prefer `apps init` (or `apps init --new` for app mode).

#### webflow apps deploy

`webflow cloud deploy` is a deprecated alias of `apps deploy` with identical flags and handler.

**Preflight phase: identity resolution.** Before any backend call, `apps deploy` runs a preflight step that resolves whether this is a site-attached deploy or a project-app first deploy. Resolution order (first match wins):

| #   | Source                                  | Result                                                                            |
| --- | --------------------------------------- | --------------------------------------------------------------------------------- |
| 1   | `--site-id <id>` flag                   | Site-attached, overrides manifest                                                 |
| 2   | `--workspace-id <id>` flag              | Project-app first deploy, overrides manifest. Mutually exclusive with `--site-id` |
| 3   | `manifest.siteId` (from `webflow.json`) | Site-attached                                                                     |
| 4   | `manifest.cloud.workspace_id`           | Project-app first deploy                                                          |
| 5   | `WEBFLOW_SITE_ID` env var               | Site-attached (used at runtime only; not persisted back to `webflow.json`)        |
| 6   | Interactive picker (no `--no-input`)    | Choose: create a new app / attach to existing site / cancel                       |
| 7   | No match + `--no-input`                 | Hard error listing required flags                                                 |

This preflight phase exists to prevent the project-app deploy path from running and provisioning a Cloud app before identity is locked in — earlier versions could orphan a new Webflow site if any later step failed.

> **Pass `--site-id` or `--workspace-id` explicitly whenever you can.** It defends against half-written manifests and removes the dependence on whatever state `apps init` happened to leave behind. If the user wants site-attached, pass `--site-id`. For project-app first deploy, pass `--workspace-id`.

**Project-app first deploy** (triggered by `--workspace-id` flag or `manifest.cloud.workspace_id`) calls `POST /cosmic/workspaces/:workspace_id/cloudApps` to atomically create a site, app, and environment. On success it writes `siteId`, `cloud.app_id`, and `cloud.environment_id` into `webflow.json`, writes `WEBFLOW_SITE_ID` into `.env`, and forces `--skip-mount-path-check` for that one deploy. Subsequent deploys behave like normal site-attached deploys.

If `--app-name` is omitted on the first project-app deploy, the CLI uses the **cwd folder name** (when 3–39 chars) and falls back to `"Cloud App"`. Provide `--app-name` explicitly in CI to avoid surprises.

**Uninitialized projects** (no `siteId`, no `workspace_id`, no flag): the CLI prompts the user to create a new project app, attach to an existing site, or cancel. With `--no-input` it hard-errors listing the required flags. Agents running with `--no-input` must always supply `--site-id` or `--workspace-id` on the first deploy of an uninitialized project.

There are two deployment approaches. **GitHub-linked deployment is recommended** — it requires no CI configuration. After a one-time dashboard setup (which the CLI can't do), every push to the connected branch triggers a deploy.

**Option 1 (recommended): GitHub-linked deployment**

Once a one-time dashboard setup is done, every push to the connected branch triggers a deploy — no CLI commands, no workflow file. **The setup is dashboard-only — the CLI cannot reach this state on its own.** Pushing a repo to GitHub does not, by itself, enable push-to-deploy.

1. Push the project to GitHub (the user needs at least one commit pushed)
2. **Tell the user to open the Webflow dashboard** → their Cloud app → **Settings** → **Git** and connect their GitHub account if not already connected
3. Select the repository, then the branch to deploy from (e.g. `main`)
4. Confirm — the dashboard runs an initial deploy automatically to verify the connection
5. From that point on: `git push` to the connected branch = deploy

Steps 2–4 cannot be scripted. If the user wants push-to-deploy, they have to click through the dashboard once. After that, the agent's job for this project is essentially done — future deploys happen on push.

> When suggesting a deployment setup to a user, always lead with this option. Only suggest GitHub Actions if the user needs custom pre/post steps, secrets injection, or multi-environment logic that the native GitHub integration does not cover.

**Option 2: GitHub Actions (manual CI/CD)**

Use when you need custom build steps, environment-specific secrets, or deploy gates not supported by the native GitHub integration. See the [GitHub Actions example](#github-actions-cicd-pipeline-when-custom-steps-are-needed) in the Examples section.

**Option 3: Local / manual deploy**

For development and one-off deploys:

```bash
webflow apps deploy \
  --no-input \
  --mount / \
  --environment main \
  --skip-mount-path-check \
  --skip-update-check
```

All `apps deploy` flags:

| Flag                      | Short | Description                                                                                                                                                                                              |
| ------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--no-input`              | —     | CI mode. Disables most prompts but **not** the project-select prompt — see callout below.                                                                                                                |
| `--mount <path>`          | `-m`  | Mount path. **Always required with `--no-input`.** Not auto-read from `webflow.json`.                                                                                                                    |
| `--environment <env>`     | `-e`  | Environment name. Creates if it does not exist. Must be passed with `--mount`.                                                                                                                           |
| `--app-name <name>`       | `-n`  | Required on first deploy with `--no-input` when no `cloud.app_id` in `webflow.json`. **Must be 3–39 characters** for project-app first deploy.                                                           |
| `--project-name <name>`   | —     | **Deprecated alias** of `--app-name`. Still accepted.                                                                                                                                                    |
| `--site-id <id>`          | `-s`  | Webflow site ID for site-attached deploys. Overrides `siteId` in `webflow.json`. Mutually exclusive with `--workspace-id`. Use this to recover from a half-written manifest without editing JSON.        |
| `--workspace-id <id>`     | `-w`  | Workspace ID for project-app first deploys. Overrides `cloud.workspace_id` in `webflow.json`. Mutually exclusive with `--site-id`.                                                                       |
| `--app-id <id>`           | `-a`  | Cloud app ID. Skips the app picker. Overrides `cloud.app_id` in `webflow.json`.                                                                                                                          |
| `--project-id <id>`       | —     | **Deprecated alias** of `--app-id`. Still accepted.                                                                                                                                                      |
| `--framework <fw>`        | `-f`  | Override framework detection. Must be `nextjs` or `astro`. Writes the value back into `webflow.json`. Use when auto-detection from `package.json` is unreliable (monorepos, missing dependencies, etc.). |
| `--directory <path>`      | `-d`  | App directory (default: cwd). Use for monorepos.                                                                                                                                                         |
| `--description <text>`    | —     | App description for the first deploy.                                                                                                                                                                    |
| `--skip-mount-path-check` | —     | Skip domain manifest validation. Required in CI. Can also be set in `webflow.json` as `cloud.skipMountPathCheck: true`.                                                                                  |
| `--auto-publish`          | —     | Publish the Webflow **site** to sync mount path routing. Does not affect app deployment.                                                                                                                 |
| `--skip-update-check`     | —     | Skip @webflow package update check.                                                                                                                                                                      |

> **Agents: pass `--mount` AND `--environment` together, every time.** The deploy prompts (select existing app, name a new app, pick an environment) are gated on whether `--mount` and `--environment` are _both_ set — not on `--no-input`. Pass `--no-input` without both and the app-select prompt still fires and hangs in non-TTY contexts. The minimum agent-safe deploy flag set is `--no-input --mount <path> --environment <env> --site-id <id>` (or `--workspace-id <id>` for project-app first deploy), plus `--app-name` whenever `cloud.app_id` is absent from `webflow.json`.

### Managing apps

> **Beta — `@next` only.** Every command in this section requires `@webflow/webflow-cli@next`. None of them exist on `@latest`. See [the beta banner](#beta-webflow-apps-requires-next).

Commands for inspecting and operating **existing** Cloud apps. They complement `init` / `deploy`:

- **Workspace is server-side.** Every read command derives the workspace from the OAuth token — there is **no `--workspace-id` flag** on any of them, and they never prompt for a workspace.
- **ID resolution.** `appId` and `envId` resolve via the shared resolver: **explicit arg/flag → env var (`WEBFLOW_APP_ID` / `WEBFLOW_APP_ENVIRONMENT_ID`) → `webflow.json` (`cloud.app_id` / `cloud.environment_id`, legacy `cloud.project_id` fallback) → interactive TTY prompt**. Running inside the app directory (so `webflow.json` resolves the IDs) is the common case, not a requirement.
- **Auto-select vs. `--no-input` contract.** When the ID isn't given, the picker auto-selects a workspace's single app / an app's single environment, so single-app/single-env setups work non-interactively (including CI). When several exist and the command can't prompt (`--no-input`, `CI=true`, no TTY, or `--json`), it exits non-zero with a **machine-readable `missingFlag`** on the error so an agent can recover by re-running with the flag. The human-readable form is e.g. `Missing required appId. Pass --app-id, set WEBFLOW_APP_ID, or add it to webflow.json.`

  **`missingFlag` comes in two shapes — match on both.** Resolver failures name a **bare key** (`appId`, `environmentId`, `depId`, `yes`); flag-compatibility refusals on `apps init` name a **flag spelling** (`--import`, `--site-id`, `--mount`, `--new`). Normalize before matching (strip a leading `--`, compare case-insensitively) rather than assuming one form. In both cases the value names **the flag to add or drop** — for a mutually-exclusive pair it names the one to **remove**, so retrying by adding the flag the error reports would loop forever.

- **`--json`.** Every command supports `--json`, which prints the raw API response and **ignores `--fields`**. Use it for programmatic parsing. `--json` also suppresses the `Using … from webflow.json` info lines.
- **`--fields <comma-list>`.** Read commands render a table; `--fields` projects which columns show (invalid field names fail fast before the network call). Each command's default and full field set are listed below.

#### Filter semantics (`list` commands)

`apps list`, `apps environments list`, and `apps env-vars list` share one filter model:

- **Exact filters** (`--name`, `--branch`, `--key`, `--site`, `--status`) match exactly and **case-sensitively**.
- **`--q`** is a **case-insensitive substring (contains)** match on that resource's primary name field only — the app name, the environment branch, the variable key. It **never** searches ids, and it **never** searches variable values. Use it to discover; use the exact filter to resolve a single item.
- **Multiple filters combine with AND.** An exact filter plus a non-matching `--q` returns an **empty page — that means nothing matched all the filters, not that the resource is absent.** Do not conclude an app or variable doesn't exist from an empty filtered page; re-run with fewer filters before reporting absence.
- Every filter value must be non-empty (`--q ""` is a usage error, not a no-op).

#### apps list

Lists all apps in your workspace. `--fields` default `id,name,siteId,createdAt` (all: `id,name,description,siteId,appPath,createdAt,siteName,shortName`).

Filters: `--site <site-id>` (exact site id), `--name <name>` (exact, case-sensitive), `--q <text>` (case-insensitive substring on the app name).

**App names are unique only within a site.** `--name` alone can match apps across several sites, and `--site` alone can match many apps — **pass `--site` AND `--name` together** to resolve to at most one app.

`--site` deliberately does **not** default from `webflow.json`: an unfiltered `apps list` returns every app the token can see, rather than silently narrowing to the manifest's site.

```bash
webflow apps list --json

# Resolve one app by name within a known site
webflow apps list --site 6234abc --name "Marketing" --json

# Discover apps whose name contains "mark" (case-insensitive)
webflow apps list --q mark --json
```

#### apps get [appId]

Details for one app. `appId` defaults to `webflow.json` / `WEBFLOW_APP_ID`. `--fields` default `id,name,description,siteId,appPath,createdAt`.

```bash
webflow apps get app_abc123 --json
```

#### apps domains [appId]

Domains and live URLs for an app. `--fields` default `id,url,lastPublished` (all + `fullSiteCompiledAt`).

Paginated: `--limit <n>` (the server caps at 100) and `--cursor <cursor>` from a previous `nextCursor`. **When paging, resend the same `--limit` and any non-default `--fields` on every page.**

```bash
webflow apps domains app_abc123 --json
webflow apps domains app_abc123 --limit 50 --cursor "$NEXT_CURSOR" --json
```

#### apps environments list [appId]

Lists an app's environments. `--fields` default `id,branch,deployUrl,latestDeploymentStatus,createdAt` (all: `id,branch,mount,deployUrl,latestDeploymentStatus,lastDeploymentSucceededAt,lastVariableModifiedAt,createdAt,updatedAt`).

> **`mount` is not in the table default.** To read an environment's mount path, either use `--json` (which returns the full API shape and ignores `--fields`) or ask for it explicitly with `--fields id,branch,mount`. A default `environments list` table will not show it.

Filters: `--branch <branch>` (exact, case-sensitive — resolves to at most one environment, since a branch is unique per app) and `--q <text>` (case-insensitive substring on the branch, for discovery).

```bash
webflow apps environments list app_abc123 --json

# Resolve the environment that builds `main`
webflow apps environments list --branch main --fields id,branch,deployUrl --json
```

#### apps deployments list

Lists the most recent deployments of an environment, **newest first**. Takes **no `appId` argument** — it resolves the app + environment from `WEBFLOW_APP_ID` / `WEBFLOW_APP_ENVIRONMENT_ID`, `webflow.json`, or a picker. `--limit` default `20`. `--fields` default `id,status,sourceType,commitHash,buildStartedAt`.

Filter: `--status <status>` (exact, one of the enum values below — an invalid value is rejected by the CLI before any network call). Paginated via `--cursor` from a previous `nextCursor`; **resend the same `--limit`, `--status`, and non-default `--fields` on every page.**

```bash
webflow apps deployments list --limit 20 --json

# Most recent failed build
webflow apps deployments list --status failed --limit 1 --json
```

**Deployment status enum:** `starting | building | deploying | success | failed | canceled | unstaged`. Note that **build-done / deploy-running maps to `deploying`** (there is no separate "deployed" state until it reaches `success`). Terminal statuses are `success`, `failed`, `canceled`, and `unstaged`.

#### apps deployments get \<depId\>

Details for one deployment (required `<depId>` positional). Resolves the app + environment the same way as `deployments list`. `--fields` default `id,status,sourceType,commitHash,buildStartedAt`.

**`--wait` blocks until the deployment reaches a terminal status** (`success` / `failed` / `canceled` / `unstaged`) or the timeout elapses, then **exits `0` on success and `1` otherwise** — so it doubles as a CI gate without any polling loop of your own. `--interval <seconds>` sets the poll cadence (floored at 5s) and `--timeout <seconds>` bounds the wait (capped at 30 minutes).

```bash
webflow apps deployments get dep_abc123 --json

# Block until the build finishes; non-zero exit fails the CI step
webflow apps deployments get dep_abc123 --wait --interval 10 --timeout 900 --json
```

#### apps deployments redeploy \<depId\>

Re-runs an existing deployment **at its same commit**, enqueuing a fresh build. **To roll back, redeploy the ID of an earlier successful deployment.** Resolves the app + environment like `deployments list`. `--dry-run` previews.

**Requires a GitHub-connected app.** Apps deployed from local files via `apps deploy` are not eligible — there is no commit to re-run.

`--idempotency-key <key>` sends an `Idempotency-Key` header so a retried enqueue is deduped rather than queuing a second build. When passed it must be non-empty printable ASCII (no control characters, newlines, or non-ASCII); omit the flag entirely to run without deduplication.

```bash
webflow apps deployments redeploy dep_abc123 --dry-run --json
webflow apps deployments redeploy dep_abc123 --idempotency-key "$GITHUB_RUN_ID-redeploy" --json

# Roll back: find the last success, then redeploy it
webflow apps deployments list --status success --limit 1 --fields id --json
```

#### apps deployments trigger

Builds the resolved environment's **current HEAD** on demand — same as `redeploy`, but with no `<depId>`: there is no past deployment to re-run, it just builds whatever the environment's configured branch points at right now. `--dry-run` previews. Same `--idempotency-key` contract as `redeploy`.

**Requires a GitHub-connected app**, same as `redeploy`.

It builds **the branch the environment is configured for**, not your checked-out branch. If those differ the CLI warns but does **not** block — check `apps environments list --fields id,branch` first if you're unsure which branch will actually build.

```bash
webflow apps deployments trigger --dry-run --json
webflow apps deployments trigger --json
```

#### apps logs build \<depId\>

Build logs for a deployment. **`depId` is required** — the CLI does not fall back to the latest deployment. Omitting it fails fast (before authenticating) with a machine-readable `missingFlag: "depId"`; run `apps deployments list` to find an ID first. `--fields` default `timestamp,message` (all + `phase`).

Filters: `--since <iso>` (only logs at/after an ISO datetime), `--q <substr>` (substring match on the message), `--limit <n>` (default `100`), `--cursor <cursor>` (pagination cursor from a previous `nextCursor`). There is **no `--level`** filter. **When paging, resend the same `--limit`, non-default `--fields`, `--since`, and `--q` on every page.**

```bash
# Find a deployment ID first — `logs build` will not guess one
webflow apps deployments list --limit 1 --fields id --json

webflow apps logs build dep_abc123 --since 2026-07-14T00:00:00Z --q error --limit 100 --json
```

#### apps logs runtime [envId]

Runtime logs for an environment. `[envId]` **defaults to the app's single environment**. If the app has several and none was given, the CLI prompts on a TTY and **errors with `missingFlag: "environmentId"` when it can't** (`--no-input`, `CI=true`, no TTY, or `--json`) — pass the env explicitly (arg, `WEBFLOW_APP_ENVIRONMENT_ID`, or `cloud.environment_id`) in that case. Same filters as `logs build` (`--since`, `--q`, `--limit`, `--cursor`; no `--level`), and the same rule about resending them on every page.

```bash
webflow apps logs runtime env_abc123 --q timeout --json
```

Pagination for both log commands: the response carries a `nextCursor` (base64url; `null` when exhausted). Pass it back verbatim via `--cursor` to fetch the next page.

#### apps env-vars

Manage a Cloud app environment's variables non-interactively. All four subcommands accept `--app-id` and `--environment-id` (defaulting from `webflow.json` via the shared resolver) and `--json`. **Secret values are never printed** to output, logs, or telemetry — the server returns secrets masked on every read, and the CLI never unmasks them.

**`apps env-vars list`** — `--fields` default `key,isSecret` (all: `key,isSecret,value,id,environmentId`). `value` is excluded by default; even with `--fields value`, secret values arrive masked.

Filters: `--key <key>` (exact, case-sensitive — resolves to at most one variable; its value is still never returned) and `--q <text>` (case-insensitive substring on the **key**). **`--q` never searches values** — there is no way to search env var contents, by design.

```bash
webflow apps env-vars list --json

# Check whether one key is set, and whether it's a secret
webflow apps env-vars list --key API_KEY --json
```

**`apps env-vars set <key> [value]`** — create or update one variable. `[value]` is optional: omit it to read from piped stdin or be prompted (recommended for secrets, keeps them out of shell history). `--secret` encrypts the value (omitting it preserves an existing key's secrecy). `--dry-run` previews without writing.

```bash
webflow apps env-vars set API_URL https://api.example.com --json
# secret — value read from stdin/prompt, never echoed:
printf '%s' "$TOKEN" | webflow apps env-vars set API_KEY --secret --json
```

**`apps env-vars delete <key>`** — delete one variable. `--dry-run` previews.

```bash
webflow apps env-vars delete API_KEY --json
```

**`apps env-vars import <file>`** — bulk upsert from a `.env` (`KEY=value`) file. `--secret` marks **every** key in the file as secret. `--dry-run` previews (values shown as `KEY=********`, never plaintext). Per-key failures are reported and cause a non-zero exit.

```bash
webflow apps env-vars import .env.production --secret --json
```

#### apps environments create [appId]

Creates an environment on an app, bound to a branch and served at a mount path. Both `--branch` and `--mount` are **required**. `--dry-run` previews.

**It does NOT deploy — the environment starts empty.** Run `apps deployments trigger` afterwards to build it.

- `--branch <branch>` — the Git branch this environment builds from. Must be a valid branch name and **not already used by another environment of this app**.
- `--mount <path>` — the URL path it is served at (e.g. `/app`). Must be **unique across the site**.
- `--idempotency-key <key>` — optional retry-stable key (sent as the request's `requestId`) to dedupe a retried create. Same printable-ASCII rule as `deployments redeploy`.

```bash
webflow apps environments create --branch staging --mount /staging --dry-run --json
webflow apps environments create --branch staging --mount /staging --json
webflow apps deployments trigger --json   # the environment is empty until you do this
```

#### apps environments update [appId] [envId]

Updates an environment's `--branch` and/or `--mount` (**at least one is required**). Same uniqueness rules as `create`. Resolves the app and environment from the positional args, `WEBFLOW_APP_ID` / `WEBFLOW_APP_ENVIRONMENT_ID`, `webflow.json`, or pickers — or via the explicit `--app-id` / `--environment-id` flags. `--dry-run` previews.

**It does NOT deploy.** After changing `--branch`, run `apps deployments trigger` to build the new branch — until you do, the environment still serves the old build.

```bash
webflow apps environments update --branch release --dry-run --json
webflow apps environments update env_abc123 --mount /v2 --json
```

#### apps environments delete [appId] [envId]

Deletes an environment from an app. Resolves app + environment like `environments update`. Requires confirmation: pass `--yes` to skip the prompt; non-interactively without it, the command refuses with `missingFlag: "yes"` rather than deleting. `--dry-run` previews.

```bash
webflow apps environments delete env_abc123 --dry-run --json
webflow apps environments delete env_abc123 --yes --json
```

#### apps link [appId]

Points the current directory at an existing app + environment by writing `webflow.json`. **It verifies the app but creates and deploys nothing** — use it to adopt an app from a fresh clone, or to repoint a directory at a different app/environment. `--dry-run` previews the manifest change.

The positional `[appId]` takes precedence over `--app-id`, `WEBFLOW_APP_ID`, and `webflow.json`. `--environment-id` selects the environment.

A workspace ID is persisted **only** when `--workspace-id` is passed explicitly — it can't be derived or verified from the app, so the CLI writes it as supplied rather than guessing.

```bash
webflow apps link app_abc123 --environment-id env_abc123 --dry-run --json
webflow apps link app_abc123 --environment-id env_abc123 --json
```

#### apps update [appId]

Update an app's `--name`, `--description`, and/or `--github-source` (at least one is required). `--dry-run` previews. `appId` defaults from `webflow.json` / `WEBFLOW_APP_ID`.

`--github-source <repo-url>` attaches a repository to an app that has none, or repoints one that already has a different repo. Pass it as `https://github.com/<owner>/<repo>`, and note:

- **It does NOT deploy.** Run `apps deployments trigger` afterwards to build from the newly attached repo.
- It requires the **Webflow GitHub App installed on the repo owner and connected to this workspace** — the same prerequisite as `apps init --import`.
- To change **which branch an environment builds**, use `apps environments update --branch`, not this flag. `--github-source` selects the repository; the environment selects the branch.

```bash
webflow apps update app_abc123 --name "New Name" --description "Marketing site app" --json

# Attach a repo, then build it
webflow apps update app_abc123 --github-source https://github.com/acme/site --json
webflow apps deployments trigger --json
```

#### apps delete [appId]

Delete (or archive — the server decides by site kind) an app. Requires confirmation: pass `--yes` to skip the prompt. Non-interactively (`--no-input` / `--json`) without `--yes`, it refuses with `missingFlag: "yes"` rather than deleting. `--dry-run` previews the impact without deleting.

```bash
webflow apps delete app_abc123 --yes --json
```

### Frameworks

| Framework | Init scaffold | Deploy support | Detected via package     |
| --------- | ------------- | -------------- | ------------------------ |
| `nextjs`  | ✓             | ✓              | `@opennextjs/cloudflare` |
| `astro`   | ✓             | ✓              | `@astrojs/cloudflare`    |

Any other value in `cloud.framework` causes `apps deploy` to exit with code 1.

> **Scaffolds are fetched from GitHub at init time.** The CLI downloads scaffold tarballs from `Webflow-Examples/hello-world-{astro,nextjs}*`, each pinned to a versioned (`vN`) branch that the installed CLI expects. `apps init` therefore requires network access to `github.com`. Old CLI installs keep working because each release stays pinned to a compatible scaffold branch.

### Global flags

| Flag                  | Description                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------- |
| `--no-input`          | Disable all interactive prompts. Required for CI/automation. Auto-enabled when `CI=true` or no TTY is detected. |
| `--manifest <path>`   | Custom path to `webflow.json`. Use for monorepos.                                                               |
| `--skip-update-check` | Skip @webflow package update check. Alternatively, set `WEBFLOW_SKIP_UPDATE_CHECKS=true`.                       |
| `--verbose`           | Display more information for debugging purposes.                                                                |

## Output

After a successful `apps deploy`, the CLI prints two pieces of output.

**1. Deployment dashboard URL** — always present on success:

```
https://webflow.com/dashboard/sites/{siteId}/webflow-cloud/projects/{appId}/environments/{environmentId}/deployments/{deploymentId}
```

Always show this to the user. From here they can view build logs, deployment status, history, and environment settings.

**2. Live app URL** — conditional:

```
🌐 Your cloud app will soon be available at:
   https://{your-site}.webflow.io/{mount-path}
```

If a real URL is printed, show it to the user as the live app link. The domain is their Webflow site's domain and the path is whatever `--mount` value was used at deploy time (e.g. `/`, `/app`, or any other user-chosen path). You can also fetch the live URL programmatically later with `webflow apps domains --json`.

If the output instead reads `No domains found with the correct mount path configuration yet.`, do not show a live URL — point the user to the dashboard deployment link above to check status and configure their domain.

**Do not** fetch or curl either URL to verify the deploy — just return what the CLI printed. To confirm status programmatically, use `webflow apps deployments list --json` or `webflow apps logs build --json` instead.

## Examples

### Full workflow: scaffold → GitHub → dashboard connection → push-to-deploy (recommended)

The CLI handles steps 1 and 2. **Step 3 must happen in the Webflow dashboard — the CLI cannot do it.** Without step 3, pushing to GitHub does not deploy.

```bash
# 1. Scaffold locally (CLI)
webflow apps init --new --no-input \
  --app-name my-app \
  --framework nextjs \
  --workspace-id ws_abc123

# 2. Push to GitHub (CLI / git)
git init && git add . && git commit -m "init"
git remote add origin https://github.com/your-org/my-app.git
git push -u origin main
```

```
# 3. Connect in the Webflow dashboard (manual, dashboard-only):
#    a. Open the Cloud app → Settings → Git
#    b. Connect the GitHub account (if not already), pick the repo
#    c. Pick the branch to deploy from (e.g. main)
#    d. Confirm — the dashboard runs an initial deploy to verify the wiring
#
# After step 3, every push to the selected branch triggers a deploy automatically.
# Skip step 3 and push-to-deploy is NOT active — deploys must be manual or CI-driven.
```

### Project-app workflow: init → first deploy provisions site

```bash
# Agent-safe init — assumes the token sees a single workspace.
# If the token sees multiple workspaces, ask the user to run this command locally first.
webflow apps init --new --no-input \
  --app-name my-app \
  --framework astro

# First deploy creates site + app + environment on the backend,
# writes siteId / app_id / environment_id back to webflow.json,
# and writes WEBFLOW_SITE_ID to .env. Subsequent deploys are normal.
cd my-app
webflow apps deploy --no-input \
  --app-name my-app \
  --mount / \
  --environment main \
  --skip-update-check
```

### Scaffold a site-attached Astro app locally

```bash
webflow apps init \
  --no-input \
  --app-name my-site-app \
  --framework astro \
  --mount /app \
  --site-id site_abc123
```

### Inspect an existing app and its latest deployment

```bash
# Which apps can this token see?
webflow apps list --json

# Details + live URLs for one app (or omit the ID inside the app dir)
webflow apps get app_abc123 --json
webflow apps domains app_abc123 --json

# Most recent deployments (newest first), then drill into one
webflow apps deployments list --limit 5 --json
webflow apps deployments get dep_abc123 --json

# Block until a build reaches a terminal status (exit 0 = success, 1 = not)
webflow apps deployments get dep_abc123 --wait --interval 10 --timeout 900 --json

# Read that deployment's build log, filtered. `logs build` requires the ID —
# it will not fall back to the latest deployment.
webflow apps logs build dep_abc123 --q error --json
```

### Manage environment variables

```bash
# Non-secret value inline
webflow apps env-vars set PUBLIC_API_URL https://api.example.com

# Secret value piped from stdin (stays out of shell history / logs)
printf '%s' "$DB_PASSWORD" | webflow apps env-vars set DB_PASSWORD --secret

# Bulk import a .env file, all keys secret; preview first
webflow apps env-vars import .env.production --secret --dry-run
webflow apps env-vars import .env.production --secret

# List (secrets shown masked) and delete
webflow apps env-vars list --json
webflow apps env-vars delete OLD_KEY
```

### GitHub Actions CI/CD pipeline (when custom steps are needed)

```yaml
name: Deploy to Webflow Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      # `apps` is beta-only — @latest has no `apps` namespace and this job
      # would fail with an unknown-command error. Use `webflow cloud deploy`
      # with @latest if you need to stay on the stable channel.
      # Pin an exact version in CI: the @next tag moves without notice.
      - name: Install Webflow CLI
        run: npm install -g @webflow/webflow-cli@next

      - name: Deploy
        run: |
          webflow apps deploy \
            --no-input \
            --mount / \
            --environment main \
            --skip-mount-path-check \
            --skip-update-check
        env:
          WEBFLOW_API_TOKEN: ${{ secrets.WEBFLOW_API_TOKEN }}
          WEBFLOW_SITE_ID: ${{ secrets.WEBFLOW_SITE_ID }}
          # For project apps pre-first-deploy, omit WEBFLOW_SITE_ID
```

### Manual deploy (local / one-off)

```bash
webflow apps deploy \
  --no-input \
  --app-name my-app \
  --mount / \
  --environment main \
  --skip-mount-path-check \
  --skip-update-check
```

### Manual deploy with error handling

```bash
webflow apps deploy --no-input --mount / --skip-mount-path-check --skip-update-check
if [ $? -ne 0 ]; then
  echo "Deploy failed. Log file:"
  webflow log
  exit 1
fi
```

## Guidelines

### Init vs Deploy in CI

- **`apps init` is for local, one-time project setup — never run it in CI.** Site-attached mode opens a browser window; there is no headless OAuth path. Run `apps init` once locally, commit the result, then use `apps deploy` in CI.

### Mount path

- `--mount` is **always required** with `--no-input`. The CLI does not read a saved mount path from `webflow.json`.
- **Never assume a default.** Assuming `/` or `/app` will cause `ENVIRONMENT_MOUNT_MISMATCH` if the app uses a different path. Check the Webflow dashboard under the environment settings, or run `webflow apps environments list --json` and read the `mount` field (`mount` is omitted from the default table — with `--fields` you must ask for it: `--fields id,branch,mount`).

### Do not add confirmation gates

When `--no-input` is set, do not add a human confirmation step before `apps deploy`. It blocks unattended CI runs and is unnecessary — the deploy path has no built-in prompt to bypass. (`apps delete` is the exception: it _requires_ `--yes` non-interactively by design.)

### Prefer `--json` for machine reads

For any read/management command (`list`, `get`, `domains`, `environments`, `deployments`, `logs`, `env-vars`), pass `--json` and parse the structured output rather than scraping the table. `--json` ignores `--fields` and returns the full API shape.

### Package manager

The CLI uses **npm only** regardless of lock files present. pnpm and yarn lock files are ignored — those projects silently receive `npm install`.

### Build-time file management

During `apps deploy`, the CLI temporarily replaces two files and restores them on success or failure:

- **Framework config** (`next.config.ts` / `astro.config.mjs`) — renamed to `clouduser.*`, replaced with CLI template, then restored.
- **`wrangler.json`** — replaced with CLI template (original saved to `clouduser.wrangler.json`), then restored. Do not modify `wrangler.json` during a deploy.

If Astro is the framework and `@astrojs/react` is absent, the CLI runs `npm install --save @astrojs/react` without prompting.

### Cloudflare bindings (D1 / KV / R2)

The CLI merges `wrangler.json` bindings at build time. Limits: **max 5 of each type**. For D1, set `migrations_dir` in the binding — the CLI copies migration files automatically.

### Error handling

- The CLI exits with **code 1 on every error**. Check the exit code — do not match on emoji or text patterns in stdout.
- For management commands, a `missingFlag` on the (JSON) error identifies the flag to re-run with (`appId`, `environmentId`, `yes`).
- Use `webflow log` after any failure to get the full error trace.

### Deploy versioning

| Situation           | Version tag sent            |
| ------------------- | --------------------------- |
| Clean working tree  | `git@{40-char-hash}`        |
| Uncommitted changes | `git@{40-char-hash}+dirty`  |
| Not in a git repo   | `noversion@{ISO-timestamp}` |

Commit all changes before deploying to production.

### Known limitations

- **The whole `apps` namespace is beta (`@next`)** — see [the beta banner](#beta-webflow-apps-requires-next). On `@latest` only `cloud init` / `deploy` / `create` / `list` exist.
- **Deploy has no `--dry-run`** — a build validation always triggers a real deployment. Every other write _does_ support `--dry-run`: `apps init` (**both** paths — the scaffold and `--import`), `link`, `update`, `delete`, `environments create` / `update` / `delete`, `deployments redeploy` / `trigger`, and all four `env-vars` subcommands. Note `--dry-run` is registered on `apps init` only, not on the `cloud init` alias.
- **Deploy has no `--json`** — the deploy URL and app ID must be parsed from stdout. The read/management commands (`list`, `get`, `domains`, `environments`, `deployments`, `logs`, `env-vars`) all support `--json`.
- **No `--watch` on logs** — the log endpoints are pollable but do not stream; poll on an interval to follow a build. Deployments are the exception: `apps deployments get --wait` blocks to a terminal status for you.
- **`apps logs build` requires a deployment ID** — it does not default to the latest deployment. Get one from `apps deployments list` first.
- **`deployments redeploy` / `trigger` need a GitHub-connected app** — apps deployed from local files via `apps deploy` are not eligible.
- **`--q` never searches values or IDs** — only the resource's primary name field (app name, environment branch, variable key).
- **No rollback command.**
- **100 MB build size limit** — builds exceeding 104,857,600 bytes fail at upload.

## Troubleshooting

### `--app-name cannot be empty` (or any required-flag error) on `apps init`

The CLI gates its interactive prompts on `process.stdin.isTTY`. Agents invoke the CLI from a subprocess that does **not** have a TTY, so the prompt block is skipped entirely and the bare validation fires for the first missing required value.

**Fix:** pass every required flag explicitly. For `apps init`:

```bash
webflow apps init --new --no-input --app-name my-app --framework astro
# or, site-attached:
webflow apps init --no-input --app-name my-app --framework astro --mount /app --site-id site_abc123
```

Passing `--no-input` is not strictly required for the prompts to be skipped — the absent TTY already does that — but it makes the contract explicit and matches the Required-flag matrix at the top of this skill.

### `apps init --new` hangs forever / never returns

Workspace selection in project-app mode prompts unconditionally when the token sees more than one workspace. Pass `--workspace-id` to skip the picker; without it, in a non-TTY context the CLI hangs at the prompt.

**Fix:** pass `--workspace-id <id>` to `apps init --new`. The workspace ID is not visible in the Webflow dashboard UI, so when the agent doesn't have one, ask the user to run `webflow apps deploy` interactively from inside an existing project. The preflight prompt picks a workspace and writes `cloud.workspace_id` to `webflow.json` — the agent can then read it and pass `--workspace-id` on future runs. Single-workspace tokens are not affected — selection is auto-skipped.

### A management command hangs or errors with a missing ID

Read/management commands resolve `appId` / `envId` from the arg/flag, then `WEBFLOW_APP_ID` / `WEBFLOW_APP_ENVIRONMENT_ID`, then `webflow.json`, then a prompt. In a non-TTY context with several apps/environments and nothing passed, the command exits with a machine-readable `missingFlag`.

**Fix:** run the command from inside the app directory (so `webflow.json` resolves the IDs), or pass the ID explicitly — `apps get <appId>`, `apps env-vars list --app-id <id> --environment-id <id>`, `apps logs runtime <envId>`. Single-app / single-env setups auto-select and need nothing extra.

### Deploy provisioned a new site when I expected site-attached

**Symptom:** user wanted to deploy to an existing Webflow site, but `apps deploy` printed `Creating Cloud app...` / `Cloud app created: <name>` and the live URL came out as `<name>-<hash>.webflow.io` (a freshly minted site) instead of the user's intended site.

**Cause:** `webflow.json` was in the project-app init state — `cloud.workspace_id` set, `siteId` absent — typically because the project was previously scaffolded with `apps init --new`. The preflight phase prefers explicit flags but still falls through to the manifest when none are passed.

**Prevention (primary fix):** pass `--site-id <existing-site-id>` to `apps deploy`. The preflight phase resolves identity from flags first, so this overrides whatever's in `webflow.json` and routes the deploy to the intended Webflow site. The skill should always pass `--site-id` when site-attached intent is known.

```bash
webflow apps deploy --no-input \
  --site-id site_abc123 \
  --mount /app --environment main \
  --skip-mount-path-check --skip-update-check
```

**Recovery if the new site was already created:**

- **Keep the new project-app site** the deploy just created — do nothing; subsequent deploys will go to the same site (or pass `--site-id` of the new site if there's any ambiguity).
- **Re-target an existing Webflow site instead.** The auto-provisioned site cannot be re-bound to an existing site after creation. Options:
  1. Delete the project app (and its auto-provisioned site) from the Webflow dashboard or with `webflow apps delete <appId> --yes`.
  2. Either edit `webflow.json` (remove `cloud.workspace_id`, `cloud.app_id`, `cloud.environment_id`, `siteId`) and re-run `apps init` with `--site-id <existing-site-id>`, or skip the manifest edit and run `apps deploy --site-id <existing-site-id>` directly — the preflight will treat this as a fresh site-attached deploy.

### Auth error on deploy

Run `webflow auth login` and complete the browser flow. The CLI writes a new `WEBFLOW_API_TOKEN` to `.env`. Retry the deploy after login.

In CI, browser auth is not possible — an auth error means `WEBFLOW_API_TOKEN` is missing or expired in your secrets. Fix the secret, do not attempt `webflow auth login`. If the CI uses the legacy `WEBFLOW_SITE_API_TOKEN`, the deploy will still work but the run log shows a deprecation warning; rename the secret to `WEBFLOW_API_TOKEN` to clear it.

### Deploying to a different workspace

For **project apps (`--new`)**: pass `--workspace-id <new-id>` to `apps init` or `apps deploy` to override `cloud.workspace_id` in `webflow.json`. Alternatively, delete `cloud.workspace_id` from `webflow.json` and re-run init (or interactive deploy on an existing project) to re-seed it.

For **site-attached projects**, workspace context is implicit in the auth token. Re-run `webflow auth login` and select the target workspace in the browser; the new token replaces the old one in `.env`.

### First project-app deploy fails with `missing_scopes`

The token saved to `.env` doesn't include the scopes needed to create a Cloud app. Re-run `webflow auth login` and re-approve the scopes, then retry the deploy.

### First project-app deploy fails: "your workspace has reached its app limit"

The selected workspace (`cloud.workspace_id`) is at its app cap. Either upgrade the workspace plan or delete unused apps in the Webflow dashboard (or with `webflow apps delete <appId> --yes`), then retry.

### First project-app deploy fails with workspace-not-found / 404

The workspace ID (from `--workspace-id` flag, or `cloud.workspace_id` in `webflow.json`) no longer resolves — workspace deleted, or token has no access. The CLI doesn't validate the flag up front: it trusts the value and surfaces the 404 from `createCloudApp`. Fixes:

- Pass `--workspace-id <correct-id>` to `apps init` or `apps deploy`.
- Or delete `cloud.workspace_id` from `webflow.json` and either re-run `apps init --new --workspace-id <id>` (empty directory) or run `webflow apps deploy` interactively (existing project) so the preflight prompt re-seeds the workspace ID.

### `ENVIRONMENT_MOUNT_MISMATCH`

The `--mount` value does not match the path registered for that environment. Check the correct mount path via `webflow apps environments list --json` (read the `mount` field), or `--fields id,branch,mount` for the table form — `mount` is not in the default field set — or the Webflow dashboard, and pass it explicitly.

### Framework cannot be detected / explicit framework required

A `webflow.json` that has a `cloud` block but no `framework` key does not throw — the CLI falls back to detecting from `package.json`. The legacy error _"webflow.json exists but doesn't contain valid framework information"_ only fires when `cloud.framework` is explicitly set to an unsupported value.

If framework detection still fails (monorepo, missing framework dependency, ambiguous setup), fix it with the `--framework` flag on `apps deploy`:

```bash
webflow apps deploy --no-input --framework nextjs --mount /app --environment main ...
```

This writes `cloud.framework` back into `webflow.json` so subsequent deploys don't need the flag. Or just edit the manifest manually:

```json
{
  "cloud": {
    "framework": "nextjs"
  }
}
```

Valid values: `nextjs`, `astro`. Any other value exits with code 1.

### Build fails, need full trace

```bash
webflow log
```

Prints the path to the latest log file with the full error trace.
