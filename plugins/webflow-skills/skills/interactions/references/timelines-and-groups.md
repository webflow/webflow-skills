<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/timelines-and-groups.md
     Do not edit here. Edit the source and re-publish. -->

# Timelines, roles, and groups

## Roles

A timeline's `triggerMetadata.role` routes it for triggers that drive more than
one timeline. Which roles are valid per trigger is generated:
[`capabilities.generated.md`](capabilities.generated.md) → Triggers.

Hover is the only conditional case — roles are required only when
`pluginConfig.multiTimeline` is `true`.

`[REJECTED]` A missing role on a trigger that routes by role, a role outside that
trigger's set, or a duplicate role across timelines.
Guard: `findTimelineRoleError` · fragments: `requires a triggerMetadata.role`,
`Expected one of:`

`[PENDING]` `assignedTimelineRole`. The panel writes `assignedGroupId` instead;
there is no Designer control that produces this field. The rejection, and the
allowance that lets a stored value survive an unrelated update, are part of
DES-7448 and are **not on `dev` yet** — today the write may succeed silently.
Do not author it; pass a stored one through untouched.
Guard once landed: `findAssignedTimelineRoleError` · fragment:
`must not set assignedTimelineRole`

## Groups

`groupId` marks a timeline as part of a user-managed action group. The cap is
`IX3_MAX_TIMELINE_GROUPS` (5), and it counts **user-managed groups** — orphan
groups are legal, so this is not a flat five-timeline limit.

`[REJECTED]` Any standard-controlType trigger whose `control` is not `play` once
two or more grouped timelines exist. The panel offers only Play there, the store
writes `play` on both entry points, and the runtime treats a missing control as
`restart`, so only an explicit `play` matches what the panel would produce.
Guard: `findGroupedTriggerControlError` · fragment:
`must use control "play" when the interaction has multiple action groups`

Load, scroll, and continuous triggers ignore group routing and keep their own
control.

## Percent canvas

Scroll-scrub and mouse X/Y timelines are not time-based — progress is driven by
the gesture — so the panel authors action `timing` as a percent of the timeline's
nominal `canvasDuration`. Values are still **stored in seconds**; the percent is a
presentation layer.

`[REJECTED]` `canvasDuration` on a timeline that is neither scroll-scrub nor mouse
X/Y, or on one that carries a role when the scrub percent timeline must be
roleless.
Guard: `findPercentTimelineError`

`[PANEL-TRAP]` A start plus duration that runs past 100% of the canvas. The panel
clamps the Start field to `100% − duration%` and disables it entirely when the
action already fills the canvas, but the write path has no equivalent bound. An
API-authored value places the action past the gesture end, and the panel silently
re-clamps it on the next edit.

## Timeline targets

`[REJECTED]` A malformed target tuple — wrong length, or a corrupt
`filterContext`. Guard: `findTimelineTargetInvariantError`

## Timeline settings

`[PANEL-TRAP]` `timeline.settings.control` on a grouped or role-routed timeline.
The panel hides the Control dropdown when the timeline has a `groupId`, when the
trigger carries group control, or while reusing — but the runtime still reads
`settings.control` through `getEffectivePlaybackConfig`. No guard covers
`timeline.settings.*`; the playback guards are all trigger-level. The stored value
changes behavior and the user cannot see or clear it.

`[PANEL-TRAP]` Any `timeline.settings.*` on a continuous, non-interval timeline.
The settings popover does not render at all for those, so nothing you store there
is reachable.

`[PANEL-TRAP]` `assignedGroupId` on a load, scroll, or continuous trigger. The
assign UI only lists standard triggers, the runtime ignores the assignment, and
the user is left with a state they cannot repair.
