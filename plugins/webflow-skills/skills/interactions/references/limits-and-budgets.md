<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/limits-and-budgets.md
     Do not edit here. Edit the source and re-publish. -->

# Limits and budgets

## The shared value budget

One byte-and-node budget spans the entire interaction. It accumulates, so many
individually small values can still fail in aggregate — the published-payload risk
is the total, not any single value.

Counted toward it:

- trigger target values, and their nested `filterBy` values
- trigger condition values
- `scrollTriggerConfig.start` and `.end` (free-form position strings, and the
  numeric branch has no length cap of its own)
- `scrollTriggerConfig.pin` in its non-boolean form, plus `endTrigger` and
  `scroller` — even though all three are separately refused
- action target values
- action property names as well as property values

Guard: `findOversizedValueError`

The failure message names the specific field path that tipped the budget, for
example `trigger "wf:scroll" scrollTriggerConfig.start`.

This is distinct from the JSON-metadata bounds applied elsewhere (for example to a
plugin's `pluginConfig`).

## Count caps

Enforced by `findInteractionCountError` in the Designer Extension host, on create
and on update. They bound the worst-case inline response, since `get_interaction`
resolves every timeline inline, rather than reflecting a Designer authoring rule.
They are never re-applied when existing data is hydrated, so stored records over a
cap still load.

See [`capabilities.generated.md`](capabilities.generated.md) for the
current values of `IX3_MAX_TIMELINES_PER_INTERACTION`,
`IX3_MAX_ACTIONS_PER_TIMELINE`, `IX3_MAX_TRIGGERS_PER_INTERACTION`, and
`IX3_MAX_TARGETS_PER_ACTION`.

The timeline cap is a flat count of the `timelines` array. It does not read
`groupId`, so an ungrouped timeline still counts toward it.

Some triggers cap lower still — a standalone trigger allows exactly one, and load
allows at most one per interaction.

All four are exported as `IX3_MAX_*` and enforced by `findInteractionCountError`,
which runs in the Designer Extension host on create **and** update. The current
values are in the generated bounds table rather than written here by hand, so a cap
change cannot drift out of the reference.

Fragment: `An interaction may define at most`

**Stored over-cap data raises its own ceiling — but only on the host path.**
`findInteractionCountError` takes the larger of the cap and the interaction's
existing count, so a Designer Extension update to legacy data is not forced to
shrink it.

`[REJECTED]` An over-cap **list sent through MCP**, even when the stored interaction
already exceeds the cap. The MCP tools apply the same caps as Zod `.max()` on the
create and update argument schemas, which runs **before** the host's baseline-aware
check.

What that does and does not block:

| Update                          | Over-cap stored interaction                                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `name` and/or `scope` only      | **Works.** `triggers` and `timelines` are optional on update; omit them and no `.max()` applies, and the host skips the count check too |
| Sends `triggers` or `timelines` | **Refused** if the list is over cap, including an unchanged resubmission                                                                |

So an over-cap interaction is not read-only through MCP: renaming and rescoping are
safe. What breaks is read-modify-write of the capped list itself, since reading a
timeline with more actions than the cap and sending it back to edit one action is
refused on resubmission.

There is no MCP-side workaround for that path. Splitting the interaction is the only
option, and it changes what the user sees.

## Duration

`MAX_CANVAS_DURATION_S` bounds a timeline's canvas duration. See the generated
capability file for the current value.

## Pagination

`list_interactions` returns a bounded page: `{items, total, hasMore, nextOffset?}`.
Default page size 50, maximum 200. Follow `nextOffset` until `hasMore` is false
rather than assuming a single call returns everything.
