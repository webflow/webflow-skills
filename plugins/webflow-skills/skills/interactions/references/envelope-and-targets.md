<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/envelope-and-targets.md
     Do not edit here. Edit the source and re-publish. -->

# Envelope, IDs, and targets

Read this alongside the file for whichever trigger you are building.

## Create envelope

Through MCP, `siteId` and `pageId` are **top-level tool arguments**, not fields in
the create action. The tool strips them before dispatch and supplies `pageId` from
the execution context. So the action body you send is:

```js
{
  name,            // [REQUIRED] non-empty
  scope,           // optional; defaults to { type: 'site' }
  triggers,        // [REQUIRED] array
  timelines,       // [REQUIRED] array
  // timelineDefaults    [OMIT] on create — see below
  // conditionalPlayback optional — see conditional-playback.md
}
```

Calling the Designer Extension API directly instead of MCP, `pageId` is a field on
the params object rather than a separate argument. Everything else is identical.

## Unknown keys on `trigger.config` are silently discarded

`[SILENTLY-DROPPED]` Any key on `trigger.config` that is not a declared field.

`triggerConfigSchema` is a plain `z.object`, so Zod strips unknown keys, and the
object→tuple transform then re-emits only the fields it names. There is no error.
The write returns success, `get_interaction` round-trips byte-identically, and the
field you sent is gone.

Declared `config` fields — everything else is dropped:

```
control · delay · jump · speed · controlType · scrollTriggerConfig
pluginConfig · assignedGroupId · assignedTimelineRole · conditionalLogic
```

**Every plugin-specific field belongs inside `config.pluginConfig`.** That is where
`eventName` (custom), `eventMode` and `multiTimeline` (hover), and `smoothness`
(mouse-move) live.

```js
// WRONG — stripped, and the trigger can never fire
config: {eventName: 'my-event'}
// RIGHT
config: {pluginConfig: {eventName: 'my-event'}}
```

Why this rule leads the file: a dogfood run put three different fields at `config`
level, watched all three vanish, and filed three capability gaps that did not
exist. The docs for each field were correct and already installed. They went
unread because the escalate-on-rejection habit that normally sends an agent to the
reference **cannot fire when the write succeeds**.

So the diagnostic is: if a field you sent is absent from the response, assume you
addressed it wrong before you conclude it is unsupported. `timingConfigSchema` is
non-strict the same way — see `easing`-for-`ease` in
[`actions-and-properties.md`](actions-and-properties.md).

## `timelineDefaults` is not authorable

`[OMIT]` on create. `[REJECTED]` for any non-null value, on create or update.

The Designer never dispatches a timeline-defaults update, so there is no authored
value to mirror. Only `null` is meaningful, and only on update, where it clears a
stored bag.

Guard: `findTimelineDefaultsError` · fragment:
`timelineDefaults is not authored by the Designer`

An empty object does not count as "unset". Leave the key out entirely on create.

## IDs

| Field         | Rule                                                                    |
| ------------- | ----------------------------------------------------------------------- |
| Timeline `id` | `[OMIT]` on create — the host mints it. Never reuse a live timeline id. |
| Action `id`   | `[REQUIRED]` on every action. A fresh unique string per action.         |
| Trigger `id`  | `[OMIT]` — the field does not exist.                                    |

`[REJECTED]` A missing action id fails schema validation before the guards run.
Fragment: `actions.0.id: Required`

## Scope

```js
{ type: 'site' }                                              // default
{ type: 'pages', value: ['PAGE_OID', ...] }                   // >= 1 existing page id
{ type: 'component', componentId: 'COMP_UUID' }               // all variants
{ type: 'component', componentId: 'COMP_UUID', variants: [...] }
```

Component and variant existence is checked by the host, not by the pure guards,
so a bad id fails at the responder rather than in schema validation. On update
that check only runs when the call actually sends `scope`.

`[REJECTED]` A `componentId` no component on the site matches.
Guard: `findComponentScopeError` · fragment: `does not exist on this site`

`[REJECTED]` A variant id that is not one of the component's variant options.
Guard: `findComponentScopeError` · fragment: `has no variant option(s)`

`[REJECTED]` A non-string `componentId`, or `variants` that is not an array.
Guard: `findScopeError` · fragments:
`Component-scoped interactions must provide a component id` /
`Component-scoped interaction variants must be an array`

### `variants` narrows playback, and empty means all

`variants` holds variant **option ids**, not names — the ids from the component's
variant options. Omitting the key and passing `[]` behave identically: the runtime
reads `componentScope?.variants?.length ? … : null`, and the existence guard only
walks a non-empty list. A non-empty list makes `IX3Engine.resolveTargets` apply
`filterByVariant` on top of the component scope selector, so only instances on
those variants animate.

Deleting a variant in the Designer cascades: an interaction scoped to that variant
alone is deleted, and one scoped to it plus others is rewritten without it.

### Do not set `libraryProfileId`

It is provenance, not an authoring option — `isLibraryInteraction` treats a scope
carrying it as library-owned, and `libraryDetach` strips it when a library is
detached. Nothing validates it, so a hand-set value silently mislabels the
interaction. There is also a known bug where the field is dropped on a server
round trip, which is why `isLibraryInteraction` falls back to asking whether the
component itself came from a library.

### `wf:inst` target parity follows scope

Under `scope.type === 'component'`, a `wf:inst` target is
`[componentDefinitionId, elementId]` and the element must exist in that
definition. Under `site` or `pages`, it must be `[pageId, elementId]`.

`[REJECTED]` A component-definition path on a non-component scope. Fragment:
`valid on component-scoped interactions`

`[REJECTED]` A component-scoped path whose element is missing from the
definition. Fragment: `does not exist on this site`

Scope-only updates deliberately skip this check for targets they retain, so a
stored `[componentDefinitionId, elementId]` survives a component-to-site flip.
Replacing triggers or timelines re-runs it, but only on **new** inst paths — you
cannot invent a component-definition path on a site-scoped interaction.

## Target shape

Targets are object format on the create/update wire:

```js
{ extensionKey, value, filterContext? }
```

A nested `filterBy` is always a **2-tuple**, never an object:

```js
filterBy: ['wf:class', [STYLE_BLOCK_ID]];
```

`value` is `[REQUIRED]` even for target types that carry no value — send `''`.

`[REJECTED]` Omitting it.
Guard: `findTargetValuePresenceError` (via the target walk) · fragment:
`target.value is required`

## Which target keys are legal where

The full matrix is generated — see
[`capabilities.generated.md`](capabilities.generated.md) → Targets.
The rules behind it:

`[REJECTED]` `wf:id` in any context. Guard: `findDisallowedTargetKeyError` ·
fragment: `is not offered by the Designer (shouldShow: false in all contexts)`

`[REJECTED]` Action-only keys (`wf:trigger-only`, `wf:trigger-only-parent`,
`wf:any-element`) used as a trigger target, or as a Filter-by on a trigger-side
target. They bind against no trigger element and never fire.
Fragment: `is only valid on timeline actions`

`[REJECTED]` `wf:trigger-only-parent` as a base target type. It is Filter-by only.

`[REJECTED]` A key the Filter-by picker does not offer, used inside `filterBy`.
Guard: `findDisallowedTargetKeyError` with `asFilterBy` · fragment:
`is not offered by the Designer's Filter-by picker`

`[REJECTED]` An active `filterContext` on `wf:trigger-only` or `wf:inst` — the
Designer hides the Filter UI for those base types.
Fragment: `does not support Filter; the Designer hides Filter UI for this target type`

A **stamped** `filterContext` with `relationship: 'none'` is accepted on those
keys. Only a filter with a real relationship is refused. This distinction matters
on read-then-write flows, where the stored value already carries the stamp.

`[REJECTED]` `wf:any-element` with `filterContext.relationship === 'none'`.
Guard: `findAnyElementFilterError`

`[REJECTED]` `firstMatchOnly: true` together with `relationship: 'none'`.

`[REJECTED]` A `DirectScope` or `SelectorScope` wrapper on a Designer-authored
`wf:` target, whether or not a filter is active. The Scope dropdown is unreachable
in the native Designer, because create always stamps a none-filter 3-tuple and the
panel hides Scope for any stamped target. Narrow to a matching set with Filter
instead.
Guard: `validateTargetValue` · fragment: `does not support Scope`

A malformed scope wrapper reports separately as
`target scope must be a valid DirectScope or SelectorScope`.

## `filterContext.relationship` — the full enum

Eight values. A wrong one is rejected with an enum-listing Zod message, so this is
the cheap kind of mistake — but a CSS-flavoured guess like `descendants` reads as
obviously correct, so check the list rather than inferring.

| Value | Selects |
| ----- | ------- |
| `none` | no filter (the stamped placeholder) |
| `within` | descendants of the filter set |
| `direct-child-of` | immediate children of the filter set |
| `contains` | ancestors of the filter set |
| `direct-parent-of` | immediate parents of the filter set |
| `next-to` | adjacent siblings |
| `next-sibling-of` | the immediately following sibling |
| `prev-sibling-of` | the immediately preceding sibling |

These are the panel's authoring names. **The published runtime uses a different
internal vocabulary** — `all`, `parent`, `children`, `siblings`, `next`,
`previous`, `first-ancestor`, `first-descendant`, `descendants`, `ancestors` — and
the host maps between them. Reading the runtime bundle and copying those names
back into a write is a trap: `descendants` looks like a real value because it is
one, just not on this side of the boundary.

```js
filterContext: {
  relationship: 'within',
  filterBy: ['wf:class', [STYLE_BLOCK_ID]],
  firstMatchOnly: false,
}
```

## The stamped filterContext

When a caller omits `filterContext` on an element-scoped target, the host stamps
the Designer's placeholder:

```js
{ relationship: 'none', filterBy: ['wf:class', []], firstMatchOnly: false }
```

Prefer omitting it and letting the host stamp, rather than composing it yourself.

## Class targets

Style-block UUIDs are preferred over class-name slugs — they round-trip through the
panel reliably. Class name strings are accepted.

Through MCP, resolve one with `data_style_tool`: `get_styles` or `query_styles`
returns each style's `id`, and that UUID is what goes in the `value` array. Note
`data_style_tool` requires both `siteId` and `pageId`, so do the page lookup first.

Calling the Designer Extension API directly instead, the equivalents are
`webflow.createStyle` and `getStyleByName`.

### One `wf:class` target is one compound selector, so the ids are ANDed

The id array is not a list of alternatives. Publishing joins every id's class name
with a dot (`transformClassTargetValue` → `.join('.')`) and the runtime resolver
queries `.${value}`, so `['a', 'b']` becomes the selector `.a.b` and matches only
elements carrying **both** classes.

That is exactly why a combo class works. The host expands each id's ancestor chain on
write (`resolveComboClassParents`, via `withComboParents` in `ix3ClassTargets.ts`), so
passing the single id for `.card.featured` stores both ids and resolves to `.card.featured`
— the selector that combo already styles. **Pass the one leaf id and let the host
expand it.** Do not assemble the chain yourself.

`[REQUIRED]` in practice: the resulting ids must form a single combo chain. Two ids
from different chains produce a selector no element carries, and the target resolves to
zero elements. Nothing rejects it — `isValidStylePath` guards `element.setStyles`, not
IX3 targets — so the interaction saves, reads back with both ids intact, and never
runs.

The shape to watch for is one leaf class name reused across different parents, for
example a `lift` combo that exists as both `.btn.lift` and `.btn.cta.lift`. Those are
two distinct style blocks with the same name. Passing both ids expands to the union of
their parents and asks for an element carrying `btn`, `cta`, and `lift` at once, which
is only the second element — or, if the parents diverge, nothing.

So: **one target means one class or one combo chain.** Two different sets of elements
means two targets or two actions. When several elements need to animate differently,
give each its own class rather than reusing one name across chains.

`[REJECTED]` A class-name **string** whose name matches more than one style block —
which is precisely the reused-leaf-name case above. The host cannot pick for you.
Resolver: `resolveWfClassBase` · fragment:
`matches multiple style blocks; use a style-block id array instead`

`[REJECTED]` A name that matches no style block on the site
(`does not match a style block on this site`), and an id array containing an id that
is not a class style block on the site (`is not on this site`).

## Value shapes per target type

`validateTargetValue` enforces a per-key value shape shared with the DE
responders. It rejects, for example, a string where an id array is expected.
Fragment varies by key; the message names the expected shape.

| Key | `value` |
| --- | ------- |
| `wf:class` | style-block id **array**, or a class-name string |
| `wf:inst` | **`[componentId, elementId]`** |
| `wf:selector` | a CSS selector string, e.g. `'body'` |
| `wf:id` | element DOM id string |
| `wf:attribute` | attribute name **or a full attribute selector** — see below |
| `wf:body`, `wf:viewport` | `''` |
| `wf:any-element` | `'*'` — **not** `''` |
| `wf:trigger-only`, `wf:trigger-only-parent` | `''` |

`wf:any-element` is the one target key whose value is a wildcard rather than a
placeholder. The three action-only keys look interchangeable and are not: sending
`''` on `wf:any-element` is refused with `"wf:any-element" value must be "*"`,
while `wf:trigger-only` and `wf:trigger-only-parent` do take `''`. Because these
keys are usually authored as a batch — one row per `filterContext` relationship —
getting this wrong loses the whole batch at once rather than one row.

**`wf:attribute` takes a bare name or a full selector.** A bare name
(`'data-thing'`) is accepted and stored as `[data-thing]`, which matches **every**
element carrying that attribute. Pass a full selector
(`'[data-thing="x"]'`, stored verbatim) when several elements share the attribute
and you mean one of them.

Two more are the ones agents get wrong.

**`wf:inst` is a 2-tuple, not a bare element id.** For an element that lives on a
page rather than inside a component definition, the `componentId` slot is the
**page id**:

```js
{extensionKey: 'wf:inst', value: [PAGE_ID, ELEMENT_ID]}
```

`[REJECTED]` A bare string. Fragment: `wf:inst value must be [componentId, elementId]`

Which of the two forms is legal is not a free choice — it follows `scope`. See
[`wf:inst` target parity follows scope](#wfinst-target-parity-follows-scope).

**`wf:selector` is how you reach the body from an action.** `wf:body` is
trigger-context-only, so an action target has to use a selector instead:

```js
{extensionKey: 'wf:selector', value: 'body'}
```

`[REJECTED]` `wf:body` as an action target.
Guard: `findActionTargetContextError` · fragment:
`is a trigger-context-only target and cannot be used as an action target`

The message names the fix, which is the only reason `wf:selector` is discoverable
at all — it appears in no capability table.

## `autoReverse` is not authorable either

`[REJECTED]` `action.timing.autoReverse` and `timeline.settings.autoReverse`.
Neither the action timing editor nor the timeline settings UI writes them, and the
runtime reverses with `playInReverse` instead.

Guard: `findTimingAutoReverseError` · fragment:
`is not authored by the Designer; the runtime uses playInReverse`

**`playInReverse` is the replacement, and it is a timeline-level boolean** — a
sibling of `name` / `immediate` / `canvasDuration` on the timeline object, not an
action `timing` field and not a trigger `config` field. It is on the MCP timeline
input, so it survives the write:

```js
timelines: [{playInReverse: true, actions: [...]}]
```

The rejection message names `playInReverse` without saying where it lives, which
reads as an instruction and sends agents guessing across three levels of the
envelope. It is one level: the timeline.

`[LEGACY-OK-ON-UPDATE]` An unchanged stored value on the same id passes. The panel
has no control that clears one either, and `get()` returns it, so rejecting it
outright would strand any interaction that already carries one on its next
read-modify-write. A new or altered value still rejects.

## Mouse-move persist bounds

`[REJECTED]` `wf:mouse-move` `pluginConfig.smoothness` outside its millisecond
range, or `restingState` x/y outside 0 to 100. Absent keys are legal.
Guard: `findMouseMoveRangeError`

Note the two numbers differ: the Smoothness **slider** in the panel is 0 to 100,
while the persisted bound follows the number input. The generated bounds table has
the current values.

## Size

Every target value, filter value, and condition value shares one interaction-wide
byte and node budget. See [`limits-and-budgets.md`](limits-and-budgets.md).
