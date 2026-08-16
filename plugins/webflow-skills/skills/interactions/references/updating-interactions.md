<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/updating-interactions.md
     Do not edit here. Edit the source and re-publish. -->

# Updating an existing interaction

Read this before any read-then-write flow. It is the dominant MCP pattern and the
place agents most often make things worse.

## Partial-update contract

| You send           | Result                                                                            |
| ------------------ | --------------------------------------------------------------------------------- |
| Field omitted      | Left unchanged                                                                    |
| Field with a value | Replaces the stored value                                                         |
| `null`             | Clears the field — only `timelineDefaults` and `conditionalPlayback` are nullable |
| `timelines`        | **Full replace** of the resolved timeline set, not a merge                        |

The DE method is `webflow.interactions.set`. The MCP action is
`update_interaction`.

## Guards run on replaced fields only

This is the rule that matters most. Validation is scoped to what you are
replacing:

- Omit `triggers` and the trigger invariants do not run against stored data.
- Send `triggers` and the **whole** replaced structure is revalidated, including
  parts you copied verbatim out of the read.

So a metadata-only edit — renaming an interaction, say — will not trip on legacy
data. The same edit expressed as a full read-modify-write of `triggers` can be
refused for a value that has been stored for months.

**Prefer the narrowest possible update.** To rename, send `name` alone.

## Cross-field checks see the half you did not send

The rule above is about **field-scoped** guards. A second set of checks is
cross-field, and they run whenever **either** `triggers` or `timelines` is
replaced, against the stored counterpart for whichever one you omitted:

| Guard                              | What it compares                                               |
| ---------------------------------- | -------------------------------------------------------------- |
| `findActionTargetContextError`     | trigger keys against action targets                            |
| `findTimelineRoleError`            | trigger role routing against timeline roles                    |
| `findPercentTimelineError`         | scrub/continuous triggers against `canvasDuration`             |
| `findMouseFollowContextError`      | mouse-move triggers against `wf:mouse-follow` actions          |
| `findScrollScrubActionTimingError` | scrub state against action `timing.repeat` / `yoyo`            |
| `findGroupedTriggerControlError`   | trigger `control` against the number of grouped timelines      |
| `findIntervalMetadataTriggerError` | interval metadata against the presence of a mouse-move trigger |

The consequence: **a narrow update can be refused for something you never sent.**
Replacing only `triggers` runs these against the stored timelines, and replacing
only `timelines` runs them against the stored triggers.

Two concrete cases:

- Swapping a click trigger's `control` away from `play` on an interaction that
  already stores two grouped timelines fails `findGroupedTriggerControlError`, even
  though you sent no timelines. The guard is deliberately wired to live timelines so
  a trigger-only update cannot strand a grouped interaction on a non-Play control.
- Replacing `timelines` with roleless ones on an interaction whose stored trigger is
  role-routed fails `findTimelineRoleError`, even though you sent no triggers.

So "omitted fields are not validated" holds for the field-scoped guards only. If you
touch either half of the trigger/timeline pair, expect the other half to be
re-examined as it currently stands in storage.

## Do not repair legacy data

Several shapes are refused on create but deliberately forwarded on update. If you
read an interaction, "correct" one of these, and write it back, you are forcing a
migration the panel never asks for — and the write may now be refused.

Pass these through untouched:

| Shape                                                                        | Status on `dev`                                 | Detail                                                   |
| ---------------------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------- |
| Non-animatable `wf:class.class` / `wf:transform.display` on a non-Set action | `[LEGACY-OK-ON-UPDATE]`                         | [`actions-and-properties.md`](actions-and-properties.md) |
| Duplicate `conditionalPlayback` types                                        | `[LEGACY-OK-ON-UPDATE]`                         | [`conditional-playback.md`](conditional-playback.md)     |
| Legacy string `splitText`                                                    | `[PENDING]` accepted today, DES-7448 may reject | [`actions-and-properties.md`](actions-and-properties.md) |
| Hover `pluginConfig.type: 'mouseover'`                                       | `[PENDING]` accepted today, DES-7448 rejects    | [`trigger-hover.md`](trigger-hover.md)                   |
| `assignedTimelineRole`                                                       | `[PENDING]` accepted today, DES-7448 rejects    | [`timelines-and-groups.md`](timelines-and-groups.md)     |

The first two are enforced today. The last three are accepted on `dev` and become
rejections when DES-7448 lands. The safe action is the same in every row: pass the
stored value through untouched.

The mechanism differs slightly per guard — some check a baseline copy of the
stored value and only reject a _changed_ legacy shape. The safe behavior is the
same either way: do not touch what you did not intend to edit.

## `controlType` stamping

The host stamps `controlType` when a caller omits it, so omitting is correct and
safe. Only an explicit contradiction is refused.

`[REJECTED]` A `controlType` that disagrees with the trigger's registered type. A
mismatch binds the wrong runtime strategy and the trigger never fires.
Guard: `findControlTypeMismatchError` · fragment: `requires controlType`

## Deleting

Delete is a soft delete. Timelines used only by the deleted interaction are
soft-deleted with it; timelines shared with another live interaction are kept.
Deleting an already-deleted interaction is idempotent, but deleting one that never
existed is an error.
