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

## Do not repair legacy data

Several shapes are refused on create but deliberately forwarded on update. If you
read an interaction, "correct" one of these, and write it back, you are forcing a
migration the panel never asks for — and the write may now be refused.

Pass these through untouched:

| Shape                                                                        | Status on `dev`                     | Detail                                                   |
| ---------------------------------------------------------------------------- | ----------------------------------- | -------------------------------------------------------- |
| Legacy string `splitText`                                                    | `[LEGACY-OK-ON-UPDATE]`             | [`actions-and-properties.md`](actions-and-properties.md) |
| Non-animatable `wf:class.class` / `wf:transform.display` on a non-Set action | `[LEGACY-OK-ON-UPDATE]`             | [`actions-and-properties.md`](actions-and-properties.md) |
| Duplicate `conditionalPlayback` types                                        | `[LEGACY-OK-ON-UPDATE]`             | [`conditional-playback.md`](conditional-playback.md)     |
| Hover `pluginConfig.type: 'mouseover'`                                       | `[PENDING]` — DES-7448 not on `dev` | [`trigger-hover.md`](trigger-hover.md)                   |
| `assignedTimelineRole`                                                       | `[PENDING]` — DES-7448 not on `dev` | [`timelines-and-groups.md`](timelines-and-groups.md)     |

The first three are enforced today. The last two describe behavior that lands with
DES-7448 — but the safe action is identical either way: pass the stored value
through untouched.

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
