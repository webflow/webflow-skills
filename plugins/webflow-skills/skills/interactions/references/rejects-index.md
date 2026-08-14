<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/rejects-index.md
     Do not edit here. Edit the source and re-publish. -->

# Decoding a rejection

Match the fragment in the error against this table, then read the linked file.

## Two message families

The same rule can produce different wording depending on which surface refused
it. The page-automation tool layer validates before the DE host does, and it
phrases some messages differently — it also deliberately softens
`validateActionPropertyShape` so a get-then-update round trip is not rejected
before the host runs.

If a fragment below does not match your error exactly, check the other family:

| Surface                      | Example wording                                                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guard (`designerInvariants`) | `Action type "wf:rive" in timeline "t1" is not in the Designer's default capability set (it is gated behind a feature flag) and cannot be created through the API.` |
| MCP tool layer               | `Trigger type "wf:navbar" is not in the Designer's default capability set and cannot be used.`                                                                      |

## Fragment to cause

| Fragment                                                                              | Cause                                                                                                                                                                                                   | Read                                                 |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `cannot be combined`                                                                  | A standalone trigger shares the interaction                                                                                                                                                             | scroll, mouse-move                                   |
| `at most one`                                                                         | Second `wf:load`                                                                                                                                                                                        | [load](trigger-load.md)                              |
| `must not carry a target`                                                             | Load purity                                                                                                                                                                                             | [load](trigger-load.md)                              |
| `must not set pluginConfig`                                                           | Load purity                                                                                                                                                                                             | [load](trigger-load.md)                              |
| `requires a trigger target`                                                           | Scroll with no target                                                                                                                                                                                   | [scroll](trigger-scroll.md)                          |
| `requires a "scrollTriggerConfig"`                                                    | Scroll config missing or null                                                                                                                                                                           | [scroll](trigger-scroll.md)                          |
| `must not set "scrollTriggerConfig"`                                                  | Config on a non-scroll trigger                                                                                                                                                                          | [scroll](trigger-scroll.md)                          |
| `endTrigger is not offered` / `scroller is not offered` / `horizontal is not offered` | Unauthorable scroll setting                                                                                                                                                                             | [scroll](trigger-scroll.md)                          |
| `pin must be a boolean`                                                               | Tuple pin                                                                                                                                                                                               | [scroll](trigger-scroll.md)                          |
| `the Designer shows no playback settings for it`                                      | `control`/`delay`/`jump`/`speed` on scroll or continuous                                                                                                                                                | scroll, mouse-move                                   |
| `must not set a jump when control is`                                                 | Jump with a clearing control                                                                                                                                                                            | [click](trigger-click.md)                            |
| `must use control "play" when the interaction has multiple action groups`             | Grouped timelines need Play                                                                                                                                                                             | [timelines](timelines-and-groups.md)                 |
| `requires controlType`                                                                | Explicit `controlType` contradicts the registry                                                                                                                                                         | [updating](updating-interactions.md)                 |
| `requires a triggerMetadata.role`                                                     | Missing role on a role-routed trigger                                                                                                                                                                   | [timelines](timelines-and-groups.md)                 |
| `Expected one of: mouseX, mouseY, interval`                                           | Bad mouse-move role                                                                                                                                                                                     | [mouse-move](trigger-mouse-move.md)                  |
| `Expected one of: open, close`                                                        | Bad navbar/dropdown role                                                                                                                                                                                | [gated](gated-capabilities.md)                       |
| `without a boolean "multiTimeline"` / `legacy field`                                  | Hover config models mixed                                                                                                                                                                               | [hover](trigger-hover.md)                            |
| `must use the hidden "wf:body"`                                                       | Custom trigger target                                                                                                                                                                                   | [custom](trigger-custom.md)                          |
| `requires a target element`                                                           | A trigger in `TRIGGER_REQUIRES_TARGET_KEYS` (click, hover, focus, blur, change) sent with no target. From the missing-target branch of `findTriggerInvariantError`, not `findTriggerTargetContextError` | [click](trigger-click.md), [hover](trigger-hover.md) |
| `is only valid on timeline actions`                                                   | Action-only target key on a trigger                                                                                                                                                                     | [envelope](envelope-and-targets.md)                  |
| `does not support Filter`                                                             | Active filter on `wf:trigger-only` / `wf:inst`                                                                                                                                                          | [envelope](envelope-and-targets.md)                  |
| `is not offered by the Designer (shouldShow: false in all contexts)`                  | `wf:id`                                                                                                                                                                                                 | [envelope](envelope-and-targets.md)                  |
| `is not offered by the Designer's Filter-by picker`                                   | Bad key inside `filterBy`                                                                                                                                                                               | [envelope](envelope-and-targets.md)                  |
| `target.value is required`                                                            | Missing `value` — use `''`                                                                                                                                                                              | [envelope](envelope-and-targets.md)                  |
| `is not a supported`                                                                  | Property not on the allowlist for its key                                                                                                                                                               | [actions](actions-and-properties.md)                 |
| `is non-animatable and must only be used in a Set action`                             | Needs `tt: 3`                                                                                                                                                                                           | [actions](actions-and-properties.md)                 |
| `must not be a plain {from, to} object`                                               | Use an array                                                                                                                                                                                            | [actions](actions-and-properties.md)                 |
| `does not support random values` / `random min/max` / `additive values`               | Value mode unsupported for that property                                                                                                                                                                | [actions](actions-and-properties.md)                 |
| `random-array must have between`                                                      | Random set size                                                                                                                                                                                         | [limits](limits-and-budgets.md)                      |
| `is not a start time the Designer can author`                                         | GSAP operator or bad ms string in `timing.position`                                                                                                                                                     | [actions](actions-and-properties.md)                 |
| `must match` (splitText mask)                                                         | A valid mask that differs from `type`. `mask: 'none'` is a schema failure, not this                                                                                                                     | [actions](actions-and-properties.md)                 |
| `cannot be set on a scroll-scrub interaction`                                         | `timing.repeat` / `yoyo` under scrub                                                                                                                                                                    | [scroll](trigger-scroll.md)                          |
| `distance and axes are only authored on interval`                                     | Off-interval metadata — `[PENDING]`, DES-7448                                                                                                                                                           | [mouse-move](trigger-mouse-move.md)                  |
| `must not set assignedTimelineRole`                                                   | Panel writes `assignedGroupId` — `[PENDING]`, DES-7448                                                                                                                                                  | [timelines](timelines-and-groups.md)                 |
| `is not in the Designer's default capability set`                                     | Gated trigger or action                                                                                                                                                                                 | [gated](gated-capabilities.md)                       |
| `not yet default-on`                                                                  | Trigger `conditionalLogic`                                                                                                                                                                              | [gated](gated-capabilities.md)                       |
| `actions.0.id: Required`                                                              | Missing action id — schema, not a guard                                                                                                                                                                 | [envelope](envelope-and-targets.md)                  |

## Errors that never reach a guard

Some payloads fail Zod before any invariant runs, so the message names a format
rather than the Designer. These have no guard to cite.

| Fragment                                                    | Cause                                                                                                                                         | Read                                 |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `Absolute position must be a number or milliseconds string` | `timing.position` as `'1.5s'`, a bare `'500'`, or another unsupported string. Operator forms pass schema and are refused by the guard instead | [actions](actions-and-properties.md) |
| `Invalid input` on `timing.position`                        | `NaN`. Zod's `z.number()` refuses it before the guard runs; `Infinity` passes schema and the guard catches it instead                         | [actions](actions-and-properties.md) |
| Invalid enum value on `splitText.mask`                      | `mask: 'none'` or any value outside `chars` / `words` / `lines`. Omit the key instead                                                         | [actions](actions-and-properties.md) |
| Expected number on `scrollTriggerConfig.scrub`              | `scrub: true` or `scrub: false`. Use `0` to scrub without smoothing, omit to disable                                                          | [scroll](trigger-scroll.md)          |
| Invalid input on `triggerMetadata.distance`                 | Fractional, or outside 1 to 10000                                                                                                             | [mouse-move](trigger-mouse-move.md)  |
| `actions.0.id: Required`                                    | Missing action id                                                                                                                             | [envelope](envelope-and-targets.md)  |

## Ordering

Only the **first** violation is reported. `findTriggerInvariantError` fixes the
order guards run in, and `findConditionsCapabilityError` runs early on purpose so
"not offered" wins over deeper outcome-shape messages. Fixing one error can
surface another that was always present — that is expected, not a regression.

## When the message is not here

Read the guard directly in
`packages/systems/ix3/schema/src/designerInvariants.ts`. Every guard cites the
Designer source it mirrors, which is usually a faster explanation than the message
itself. If you add a rule, add its fragment to this table.
