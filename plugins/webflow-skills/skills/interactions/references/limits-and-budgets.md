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

Applied at the tool boundary on create and update. They bound the worst-case
inline response — `get_interaction` resolves every timeline inline — rather than
reflecting a Designer authoring rule. They are never re-applied when existing data
is hydrated, so stored records over a cap still load.

| Cap                       | Value                         | Source                                                    |
| ------------------------- | ----------------------------- | --------------------------------------------------------- |
| Timelines per interaction | `IX3_MAX_TIMELINE_GROUPS` (5) | mirrors the store's authoring cap on `timelineIds.length` |
| Actions per timeline      | 200                           | guardrail                                                 |
| Triggers per interaction  | 20                            | guardrail                                                 |
| Targets per action        | 20                            | guardrail                                                 |

The timeline cap is a flat count of the `timelines` array. It does not read
`groupId`, so an ungrouped timeline still counts toward it.

Some triggers cap lower still — a standalone trigger allows exactly one, and load
allows at most one per interaction.

These four live as local constants in the page-automation tool layer
(`packages/systems/page-automation/core/tools/interactions.ts`) rather than as
exports, which is why they are written here by hand instead of generated. If you
change them, update this table.

## Duration

`MAX_CANVAS_DURATION_S` bounds a timeline's canvas duration. See the generated
capability file for the current value.

## Pagination

`list_interactions` returns a bounded page: `{items, total, hasMore, nextOffset?}`.
Default page size 50, maximum 200. Follow `nextOffset` until `hasMore` is false
rather than assuming a single call returns everything.
