<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/__generated__/capabilities.md
     Do not edit here. Edit the source and re-publish. -->

<!-- GENERATED FILE — do not edit by hand.
     Source: packages/tooling/ix3-agent-pack/src/renderCapabilities.ts
     Regenerate: npx nx run packages/tooling/ix3-agent-pack:generate -->

# IX3 capability reference

Machine-generated from the exported constants in
`packages/systems/ix3/schema/src/designerInvariants.ts`, which is the
server-side mirror of the Designer's authoring rules. Every value below is
read from code, so it cannot drift from the write path.

This file covers the facts that exist as data. Rules that live inside a guard
body — value shapes, ordering, the reasons behind a rejection — are in the
pack's `references/` files and are maintained by hand.

## Triggers

Authorable = the write path accepts it today. A `no` row is rejected for
every caller; the guards take no flag or session parameter. This table
cannot say *why* a row is unauthorable — some are gated pending GA and some
have no Designer schema at all. See `references/gated-capabilities.md`.

The Target column is probed against the write path rather than read from a
single constant, because the policy is spread across several guards.
`required, specific key` means a target is required but only one key is legal
(the trigger reference names it). `see reference` means another guard fired
first, so the target rule could not be isolated.

| Trigger | Authorable | controlType | Standalone | Target | Timeline roles | Allowed `control` |
| --- | --- | --- | --- | --- | --- | --- |
| `wf:blur` | **no** | `standard` | no | **required** | — | n/a — not authorable |
| `wf:change` | **no** | `standard` | no | **required** | — | n/a — not authorable |
| `wf:click` | yes | `standard` | no | **required** | — | each: `pause`, `play`, `restart`, `resume`, `reverse`, `reverseFlipEase`, `stop`, `togglePlayReverse`, `togglePlayReverseFlipEase`<br>restricted occurrence: `pause`, `play`, `restart`, `resume`, `reverse`, `reverseFlipEase`, `stop` |
| `wf:custom` | yes | `standard` | no | required, specific key | — | standard set (`none`, `pause`, `play`, `restart`, `resume`, `reverse`, `reverseFlipEase`, `stop`, `togglePlayReverse`, `togglePlayReverseFlipEase`) |
| `wf:dropdown` | **no** | `standard` | yes | optional | `close`, `open` | n/a — not authorable |
| `wf:focus` | **no** | `standard` | no | **required** | — | n/a — not authorable |
| `wf:hover` | yes | `standard` | no | **required** | conditional: `mouseEnter`, `mouseLeave` when `multiTimeline: true` | standard set (`none`, `pause`, `play`, `restart`, `resume`, `reverse`, `reverseFlipEase`, `stop`, `togglePlayReverse`, `togglePlayReverseFlipEase`) |
| `wf:load` | yes | `load` | no | **must omit** | — | `none`, `play` |
| `wf:mouse-move` | yes | `continuous` | yes | optional | `interval`, `mouseX`, `mouseY` | n/a — playback fields rejected |
| `wf:navbar` | **no** | `standard` | yes | optional | `close`, `open` | n/a — not authorable |
| `wf:scroll` | yes | `scroll` | yes | **required** | — | n/a — playback fields rejected |

Playback fields (`control`, `delay`, `jump`, `speed`) are rejected on control types `continuous`, `scroll`. Navbar and dropdown also hide the playback editor in the panel, but they
still carry `control: "play"` and are *not* covered by that rejection —
omitting it fails the grouped-trigger check once the interaction has two or
more action groups.

Conditions capability (trigger-level `conditionalLogic`): **not available**. Interaction-level `conditionalPlayback` is a separate field and is authorable.

## Actions

Authorable action keys: `wf:class`, `wf:lottie`, `wf:mouse-follow`, `wf:spline`, `wf:style`, `wf:transform`.

Non-animatable properties are only valid inside a Set action (`tt: 3`).
Plugin keys absent from the property table skip the property-name check.

| Extension key | Authorable | Properties | Non-animatable (Set only) |
| --- | --- | --- | --- |
| `wf:class` | yes | `class` | `class` |
| `wf:style` | yes | `backgroundColor`, `borderColor`, `color`, `overflow`, `pointerEvents`, `position`, `zIndex` | `overflow`, `pointerEvents`, `position`, `zIndex` |
| `wf:transform` | yes | `autoAlpha`, `display`, `height`, `opacity`, `rotation`, `rotationX`, `rotationY`, `scale`, `scaleX`, `scaleY`, `skewX`, `skewY`, `transformOrigin`, `transformPerspective`, `width`, `x`, `xPercent`, `y`, `yPercent`, `z` | `display` |

### Value modes

| Extension key | Random array | Random min/max | Additive |
| --- | --- | --- | --- |
| `wf:class` | — | — | — |
| `wf:style` | `backgroundColor`, `borderColor`, `color` | — | — |
| `wf:transform` | `autoAlpha`, `height`, `opacity`, `rotation`, `rotationX`, `rotationY`, `scale`, `scaleX`, `scaleY`, `skewX`, `skewY`, `transformPerspective`, `width`, `x`, `xPercent`, `y`, `yPercent`, `z` | `autoAlpha`, `height`, `opacity`, `rotation`, `rotationX`, `rotationY`, `scale`, `scaleX`, `scaleY`, `skewX`, `skewY`, `transformPerspective`, `width`, `x`, `xPercent`, `y`, `yPercent`, `z` | `autoAlpha`, `height`, `opacity`, `rotation`, `rotationX`, `rotationY`, `scale`, `scaleX`, `scaleY`, `skewX`, `skewY`, `transformPerspective`, `width`, `x`, `xPercent`, `y`, `yPercent`, `z` |

A random-array set holds between 2 and 12 values.

## Targets

| Rule | Target keys |
| --- | --- |
| Valid only on timeline actions | `wf:any-element`, `wf:trigger-only`, `wf:trigger-only-parent` |
| Valid only on trigger targets | `wf:body`, `wf:viewport` |
| No Filter — active `filterContext` rejected | `wf:inst`, `wf:trigger-only` |
| Not offered by the Filter-by picker | `wf:any-element`, `wf:body`, `wf:viewport` |

Default `filterContext` stamped when a caller omits it: `{ relationship: "none", filterBy: ["wf:class",[]], firstMatchOnly: false }`.
A stamped placeholder is accepted on the no-Filter keys above; only a filter
with a real relationship is refused.

## Playback field clearing

The panel clears these fields for the listed controls, so sending them is
rejected on any trigger whose playback editor is visible.

| Field | Must be omitted when `control` is |
| --- | --- |
| `jump` | `none`, `restart`, `resume`, `togglePlayReverse`, `togglePlayReverseFlipEase` |
| `speed` | `none`, `pause`, `stop` |

Note: `STANDARD_TRIGGER_ALLOWED_CONTROLS` is the opt-in complete set, not the
panel's default dropdown. `reverseFlipEase` is accepted by the write path but
the panel filters it out of the default options as a guard against stale-CDN
GSAP versions, so prefer not to author it.

## Numeric bounds

| Field | Bound |
| --- | --- |
| `timeline.canvasDuration` | at most 12 seconds |
| `ix3-random-array` values | 2 to 12 entries |

Per-interaction count caps (timelines, actions, triggers, targets) are
applied at the page-automation tool boundary rather than in this schema, so
they are not exported and cannot be rendered here. See
`references/limits-and-budgets.md`.
