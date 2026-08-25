<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/panel-traps.md
     Do not edit here. Edit the source and re-publish. -->

# Panel traps

Values the write path **accepts** but the Interactions panel cannot author,
display, edit, or clear. The write succeeds. Nothing errors. The damage is only
visible to the human afterwards, when they open the panel and find a state they
cannot reach or undo.

This is the one class no error message will ever teach an agent, which is why it
is documented separately.

Every row on this page is `[PANEL-TRAP]`.

**Do not author these unsolicited.** If a user explicitly asks for one, warn that
the result will not be editable in the Designer.

## How to read an entry

Each entry names the guard that **deliberately stops short** of covering it,
rather than asserting "the API accepts this". Several of these carve-outs are
intentional — the guard matches the panel's own condition exactly so the API is
not stricter than the panel. Written this way, a future guard makes an entry
_incomplete_ rather than _wrong_.

## Timeline settings

| Field                                                                                   | Panel behavior                                                                                                                                                                                                                                                         | Guard that stops short                                                                                                                                                        |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `settings.control` on a **role-routed** timeline whose Control dropdown is hidden       | Hidden while reusing when the trigger offers one control or none. `getEffectivePlaybackConfig` reads role-routed timelines from settings alone, so the value dispatches.                                                                                               | The playback guards (`findTriggerJumpError`, `findTriggerSpeedError`, `findUneditablePlaybackFieldError`) are all **trigger-level**. Nothing validates `timeline.settings.*`. |
| Any `timeline.settings.*` on a continuous, non-interval timeline                        | The settings popover does not render, but `buildSubTimeline` still passes settings into the GSAP defaults, so the value is live.                                                                                                                                       | Same, trigger-level only.                                                                                                                                                     |
| A hover in/out authored as `multiTimeline: true` with `mouseEnter` / `mouseLeave` roles | The panel writes a trigger split instead (two `wf:hover` triggers with `eventMode`, groups keyed by `groupId`). The remove control keys off `groupId` or a `groupRoles` config, and hover declares `triggerSplit`, so neither role-based group offers a remove button. | `findTimelineRoleError` validates the roles and accepts the shape. Nothing checks that the grouping matches what the panel can edit.                                          |
| `assignedGroupId` on a load, scroll, or continuous trigger                              | The assign UI lists standard triggers only; the runtime ignores the assignment.                                                                                                                                                                                        | `findOrphanedGroupAssignmentError` covers discrete standard triggers only and deliberately exempts these, so an ignored assignment still stores.                              |

`settings.control` on a **grouped** timeline is deliberately absent from this
table. A standard trigger routed to a group takes `control` from the trigger, so
a stored value there has no effect. See
[`timelines-and-groups.md`](timelines-and-groups.md).

The role-based hover row is a trap you may knowingly accept when writing through
**MCP**, but it is no longer forced. The MCP timeline input carries `groupId` now, so
the trigger split the panel prefers is expressible there, and an unmatched
`assignedGroupId` is rejected by `findOrphanedGroupAssignmentError` instead of stored
inert. Taking the role form costs the user a remove button; taking the split form
keeps the panel fully in control. Details in
[`trigger-hover.md`](trigger-hover.md).

## Action timing

| Field                                                              | Panel behavior                                                                | Guard that stops short                                                                  |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `timing.duration` on a Set action                                  | Duration input disabled for Set.                                              | `findActionTimingPositionError` covers `position` only.                                 |
| `timing.ease` on a Set action                                      | Ease row not rendered for Set.                                                | No `timing.ease` guard exists.                                                          |
| `timing.repeat` / `yoyo` / `stagger` / `splitText` on a Set action | The whole block is gated behind a non-Set tween type.                         | `findScrollScrubActionTimingError` keys off scroll scrub, not Set.                      |
| `timing.repeat` / `yoyo` on a continuous-only interaction          | Repeat UI not rendered when a continuous trigger is present.                  | `findScrollScrubActionTimingError` keys off **scrub**; continuous alone is not covered. |
| Start plus duration past 100% of a percent canvas                  | Start is clamped to `100% − duration%` and the input disables entirely at 0%. | `findActionTimingPositionError` rejects operator strings, not out-of-range numerics.    |

## Action properties

| Field                                                          | Panel behavior                   | Guard that stops short                                                                  |
| -------------------------------------------------------------- | -------------------------------- | --------------------------------------------------------------------------------------- |
| A `from` slot value on a To tween                              | From editor disabled.            | `validateActionPropertyShape` validates leaf shapes, not slot-versus-tween consistency. |
| A `to` slot value on a From tween                              | To editor disabled.              | Same.                                                                                   |
| Plugin `from`/`to` slots on the wrong tween type (`wf:spline`) | Selects disabled per tween type. | `validateActionPropertyShape` returns early for plugin keys with no deep property list. |

## Trigger and target

| Field                                                       | Panel behavior                                                                                                                                                                                                 | Guard that stops short                                                                                                                                                                                                            |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scroll page-target start offset greater than the end offset | The panel silently drops the change, with no error shown.                                                                                                                                                      | No scroll position-ordering guard exists.                                                                                                                                                                                         |
| `velocityInfluence: true` on a non-interval timeline        | `getEffectiveVelocityState` forces the effective state to `false`, so the toggle is hidden but the animation-type selector is restored and the property picker is unrestricted. The stored flag is inert here. | No `velocityInfluence` guard exists. The risk is not a stuck editor: it is that the flag becomes effective again if the action is later placed on an eligible mouse-move interval timeline, without the user having asked for it. |

## Not traps — common misreadings

These look like traps and are not. Treating them as traps produces payloads the
API refuses.

**`triggerMetadata.distance` outside 1 to 10000, or fractional.** The panel
clamps and rounds, which resembles a trap, but `triggerMetadata`'s schema bounds
it as `z.number().finite().int().min(1).max(10000)`. An out-of-range or
fractional value is rejected at schema validation and never reaches the panel.
See [`trigger-mouse-move.md`](trigger-mouse-move.md).

**Target scope on a Designer-authored `wf:` target.** The Scope selector is
hidden when the target has filtering, which resembles a trap. But
`validateTargetValue` refuses `DirectScope` and `SelectorScope` on these targets
outright, whether or not a filter is active: the Designer narrows targets through
Filter, so Scope is not authorable through the API at all. See
[`envelope-and-targets.md`](envelope-and-targets.md).

**Navbar and dropdown playback fields.** The panel hides the playback editor for
them, which resembles the scroll and continuous case. But they still carry
`control: 'play'`, and `findGroupedTriggerControlError` _requires_ it once the
interaction has two or more grouped timelines. They are deliberately excluded from
`NO_PLAYBACK_CONTROL_TYPES` so the two guards do not contradict each other. (Both
triggers are gated anyway — see [`gated-capabilities.md`](gated-capabilities.md).)

**Conditional outcome `targetTimelineId` outside the assigned group.** The panel
narrows the outcome list to the assigned group and `findConditionalOutcomeError`
does not check membership — but the whole conditions capability is refused by
`findConditionsCapabilityError`, so this is unreachable rather than a trap.

## Candidates deliberately excluded

These surfaced during the audit and are **not** listed above because they could
not be confirmed. Do not add them without verifying against current source:
flip-ease control masking, `action.hidden`, the Lottie 0–1 frame clamp, and
invalid scroll position strings persisting after a failed inline validation.

## These are documentation, not a backlog

Documenting a trap deliberately does **not** add a guard for it. Turning any of
these into a rejection changes write behavior, needs its own risk assessment, and
must never carry a `non-prod:` label. Track that separately as parity work.
