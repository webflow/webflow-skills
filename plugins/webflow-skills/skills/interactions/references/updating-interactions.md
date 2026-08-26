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

## Worked payloads

All four verified accepted against the live API.

**There is no way to patch a single action.** `timelines` is the smallest unit you
can replace, so changing one action's duration means re-sending every timeline the
interaction owns, in full. Read the interaction first and carry over everything you
are not changing — roles, `groupId`, `canvasDuration`, `settings`, and the other
timelines — because anything you omit is gone. That replace also re-runs the
cross-field guards against the stored triggers you did not send, so a
single-action edit can be refused for a reason that has nothing to do with your
edit.

The identifier is `id`, inside the action body. `siteId` and `pageId` stay
top-level tool arguments and must **not** be echoed into the body.

**Rename, changing nothing else.** Send `name` alone.

```js
{id: 'i-42e7f215', name: 'New name'}
```

**Clear a nullable field.** `null` clears; omitting leaves the stored value.

```js
{id: 'i-42e7f215', conditionalPlayback: null}
```

**Replace every timeline.** `timelines` is a full replace when present. Omit the
timeline `id`s — the host mints new ones and the old timelines are dropped, not
edited in place. Confirmed: the replacement came back with a fresh
`t-…` id and `version: 0` while the interaction's own `version` incremented.

```js
{
  id: 'i-42e7f215',
  timelines: [{
    actions: [{
      id: 'act-replacement', name: 'Fade', tt: 2,
      timing: {duration: 0.4, ease: 2},
      properties: {'wf:transform': {opacity: ['0%', '100%']}},
      targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
    }],
  }],
}
```

### Read-then-write: send the minimum, not the echo

After a `get_interaction`, do **not** send the fetched object back wholesale. Send
only the fields you are changing. To rename, that is `{id, name}` — nothing else.

A full echo is accepted in practice (server-owned keys like top-level `pageId` and
`version` are tolerated and ignored), but it is the wrong habit for four reasons
this file already documents:

- Echoing `triggers` or `timelines` **revalidates the whole replaced structure**,
  so a value stored months ago can be refused now.
- A fetched non-null `timelineDefaults` is `[REJECTED]` on update as well as
  create, so it has to be dropped or nulled.
- An over-cap `timelines` or `actions` list is refused by the MCP `.max()` even as
  an unchanged resubmission — the host's grandfathering does not apply here.
- Guards run only on fields you replace, so the smaller the payload, the fewer
  ways it can fail.

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

| Shape                                                                        | Status on `dev`         | Detail                                                   |
| ---------------------------------------------------------------------------- | ----------------------- | -------------------------------------------------------- |
| Non-animatable `wf:class.class` / `wf:transform.display` on a non-Set action | `[LEGACY-OK-ON-UPDATE]` | [`actions-and-properties.md`](actions-and-properties.md) |
| Off-interval `triggerMetadata.distance` / `axes`                             | `[LEGACY-OK-ON-UPDATE]` | [`trigger-mouse-move.md`](trigger-mouse-move.md)         |
| `timing.autoReverse` / `settings.autoReverse`                                | `[LEGACY-OK-ON-UPDATE]` | [`envelope-and-targets.md`](envelope-and-targets.md)     |
| Duplicate `conditionalPlayback` types                                        | `[LEGACY-OK-ON-UPDATE]` | [`conditional-playback.md`](conditional-playback.md)     |
| Legacy string `splitText`                                                    | `[LEGACY-OK-ON-UPDATE]` | [`actions-and-properties.md`](actions-and-properties.md) |
| Hover `pluginConfig.type: 'mouseover'`                                       | `[LEGACY-OK-ON-UPDATE]` | [`trigger-hover.md`](trigger-hover.md)                   |
| `assignedTimelineRole`                                                       | `[LEGACY-OK-ON-UPDATE]` | [`timelines-and-groups.md`](timelines-and-groups.md)     |

Every row is refused on create and forwarded on update. The allowances are narrow:
most are counted or matched per id, so one stored legacy value cannot authorize a
second, and altering the value re-enters the reject.

The safe action is the same in every row: pass the stored value through untouched.

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
