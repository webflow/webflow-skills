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

| Field                                                            | Panel behavior                                                                                                                              | Guard that stops short                                                                                                                                                        |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `timeline.settings.control` on a grouped or role-routed timeline | Control dropdown hidden when the timeline has a `groupId`, the trigger carries group control, or while reusing. The runtime still reads it. | The playback guards (`findTriggerJumpError`, `findTriggerSpeedError`, `findUneditablePlaybackFieldError`) are all **trigger-level**. Nothing validates `timeline.settings.*`. |
| Any `timeline.settings.*` on a continuous, non-interval timeline | The settings popover does not render at all.                                                                                                | Same — trigger-level only.                                                                                                                                                    |
| `assignedGroupId` on a load, scroll, or continuous trigger       | The assign UI lists standard triggers only; the runtime ignores the assignment.                                                             | No guard covers `assignedGroupId`. The DES-7448 rejection in progress targets the separate legacy `assignedTimelineRole` field.                                               |

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

| Field                                                                        | Panel behavior                                                                                                              | Guard that stops short                                                                                                                                                      |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scroll page-target start offset greater than the end offset                  | The panel silently drops the change — no error shown.                                                                       | No scroll position-ordering guard exists.                                                                                                                                   |
| `triggerMetadata.distance` outside 1–10000 on a mouse-move interval timeline | The panel clamps and rounds on the next edit.                                                                               | No interval-metadata guard exists on `dev` at all. The DES-7448 work in progress checks role and trigger presence, not numeric bounds, so this stays a trap after it lands. |
| `velocityInfluence` on a non-interval timeline                               | Toggle hidden; the property picker is restricted and the animation-type selector is hidden, so the user cannot turn it off. | No `velocityInfluence` guard exists.                                                                                                                                        |
| Target scope while a filter is active                                        | The Scope selector is hidden when the target definition has filtering.                                                      | `validateTargetValue` validates scope **shape**, not scope-versus-filter exclusivity.                                                                                       |

## Not traps — common misreadings

Two things look like traps and are not. Getting these wrong produces rejected
writes.

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
