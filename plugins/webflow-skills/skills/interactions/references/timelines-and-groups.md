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

`[REJECTED]` `assignedTimelineRole`. The panel writes `assignedGroupId` to route a
trigger to a timeline group; no Designer control produces this field.
Guard: `findAssignedTimelineRoleError` · fragment:
`must not set assignedTimelineRole`

`[LEGACY-OK-ON-UPDATE]` A stored value survives an update, allowanced per
trigger-and-role slot so one stored value cannot authorize a second.

## Groups

`groupId` marks a timeline as part of a user-managed action group.

**The five-item limit is a flat cap on timelines, not on groups.** The tool
applies `.max(IX3_MAX_TIMELINE_GROUPS)` to the `timelines` array and the store
checks `interaction.timelineIds.length`; neither reads `groupId`. A six-timeline
interaction is refused even when no timeline belongs to a group.
Fragment: `An interaction may define at most 5 timelines`

A timeline may be unassigned, which is separate from the count. Being groupless
does not exempt it from the limit.

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

No guard covers `timeline.settings.*`; the playback guards are all trigger-level.
What the runtime does with these values depends on how the timeline is routed, so
the three cases are not interchangeable.

**Role-routed timelines (`triggerMetadata`) read settings and never fall back.**
`getEffectivePlaybackConfig` takes `control`, `delay`, `jump`, and `speed` from
`timeline.settings` alone. This is where a stored value has the most effect.

`[PANEL-TRAP]` `settings.control` on a role-routed timeline whose Control dropdown
the panel hides, which happens while reusing when the trigger offers one control or
none. The runtime dispatches your value and the user cannot see or clear it.

**Grouped timelines (`groupId`) take `control` from the trigger.** For a standard
trigger routed to a group, `getEffectivePlaybackConfig` returns `control:
cfg.control` and reads only `jump` and `speed` from the group's settings. So
`settings.control` on a grouped timeline does **not** change group playback. Do not
set it expecting an effect, and do not treat it as a trap.

A non-standard play-all trigger (load, scroll, continuous) ignores group routing
entirely and keeps its own timing.

`settings.delay` is deliberately not surfaced for either case: `buildSubTimeline`
already bakes it into the GSAP sub-timeline, so returning it would double-apply it.

**Continuous timelines still consume settings.** The settings popover does not
render for a continuous, non-interval timeline, but `buildSubTimeline` passes
`timeline.settings` into the GSAP defaults regardless, so values stored there are
live rather than inert.

`[PANEL-TRAP]` Any `timeline.settings.*` on a continuous, non-interval timeline.
It affects the built timeline and there is no panel surface to inspect or clear it.

`[PANEL-TRAP]` `assignedGroupId` on a load, scroll, or continuous trigger. The
assign UI only lists standard triggers, the runtime ignores the assignment, and
the user is left with a state they cannot repair.
