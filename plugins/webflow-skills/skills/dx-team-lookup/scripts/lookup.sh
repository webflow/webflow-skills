#!/usr/bin/env bash
# DX team lookup — resolves a name, email, or GitHub username to team + pillar.
#
# Usage:
#   bash ~/.claude/skills/dx-team-lookup/scripts/lookup.sh "<search_term>"
#
# Outputs CSV: name,email,github_username,team,pillar,as_of

set -euo pipefail

SEARCH_TERM="${1:?Usage: lookup.sh <search_term>}"

if [[ -z "${DX_WAREHOUSE_DSN:-}" ]]; then
  DX_WAREHOUSE_DSN=$(AWS_PROFILE=dev-publish-only ops/secret-manager get-secret-value \
    --secret-id arn:aws:secretsmanager:us-east-1:735392911607:secret:localdev-secrets/dx-secrets-b1ae64d-xUIxez \
    2>/dev/null) || {
    cat >&2 <<'BANNER'
+------------------------------------------------------------------+
| Could not fetch DX warehouse credentials from AWS                |
|                                                                   |
| Your SSO session may be expired. Try:                            |
|   aws sso login --sso-session wf-session                         |
|                                                                   |
| Then re-run this skill. No manual setup is required —            |
| credentials are fetched automatically via dev-publish-only.      |
+------------------------------------------------------------------+
BANNER
    exit 1
  }
fi

# Pipe query via stdin so psql processes :'var' substitution client-side.
# (The -c flag sends queries directly to the server, bypassing psql variable substitution.)
psql "$DX_WAREHOUSE_DSN" --csv -v search_term="$SEARCH_TERM" <<'ENDSQL'
WITH latest_per_user AS (
  SELECT vtm.user_id, MAX(vd.date) AS latest_date
  FROM public.dx_versioned_team_members vtm
  JOIN public.dx_versioned_teams vt ON vtm.versioned_team_id = vt.id
  JOIN public.dx_versioned_team_dates vd ON vt.versioned_team_date_id = vd.id
  GROUP BY vtm.user_id
)
SELECT
  u.name,
  u.email,
  u.github_username,
  vt.name AS team,
  COALESCE(
    CASE WHEN ggpt.parent_id IS NULL AND ggpt.is_parent THEN ggpt.name END,
    CASE WHEN  gpt.parent_id IS NULL AND  gpt.is_parent THEN  gpt.name END,
    CASE WHEN   pt.parent_id IS NULL AND   pt.is_parent THEN   pt.name END,
    CASE WHEN   vt.parent_id IS NULL AND   vt.is_parent THEN   vt.name END
  ) AS pillar,
  vd.date AS as_of
FROM public.dx_users u
JOIN latest_per_user lpu ON lpu.user_id = u.id
JOIN public.dx_versioned_team_members vtm ON vtm.user_id = u.id
JOIN public.dx_versioned_teams vt ON vtm.versioned_team_id = vt.id
JOIN public.dx_versioned_team_dates vd ON vt.versioned_team_date_id = vd.id AND vd.date = lpu.latest_date
LEFT JOIN public.dx_versioned_teams pt   ON vt.parent_id  = pt.id   AND pt.versioned_team_date_id  = vd.id
LEFT JOIN public.dx_versioned_teams gpt  ON pt.parent_id  = gpt.id  AND gpt.versioned_team_date_id = vd.id
LEFT JOIN public.dx_versioned_teams ggpt ON gpt.parent_id = ggpt.id AND ggpt.versioned_team_date_id = vd.id
WHERE u.deleted_at IS NULL
  AND (
    u.name ILIKE '%' || :'search_term' || '%'
    OR u.email ILIKE '%' || :'search_term' || '%'
    OR u.github_username ILIKE '%' || :'search_term' || '%'
  );
ENDSQL
