# Targets

A target is `{extensionKey, value, filterContext?}`. Trigger targets and action targets are not the same set.

## Trigger only

| Key | Value | Where it is valid |
| --- | --- | --- |
| `wf:body` | `""` | `wf:scroll`, and the required target of `wf:custom` |
| `wf:viewport` | `""` | `wf:mouse-move` only |

`wf:body` on a click, hover, or load trigger is rejected. `wf:viewport` on any trigger except mouse move is rejected. Neither key is an action target.

## Action only

| Key | Value | Notes |
| --- | --- | --- |
| `wf:trigger-only` | `""` | The element that received the trigger |
| `wf:trigger-only-parent` | `""` | The parent of that element |
| `wf:any-element` | `"*"` | Requires `filterContext.relationship` other than `none` |

Using these as a trigger target fails with `Trigger target "wf:trigger-only" is only valid on timeline actions, not trigger targets.` The same sentence is used for `wf:trigger-only-parent` and `wf:any-element`.

`wf:trigger-only` does not take a scope wrapper. Use `""`.

## Trigger and action

| Key | Value |
| --- | --- |
| `wf:class` | A non-empty class slug, or a non-empty array of style-block ids |
| `wf:selector` | A non-empty CSS selector |
| `wf:attribute` | `[name]` or `[name="value"]` |
| `wf:inst` | `[ownerId, elementId]`, two non-empty strings |

A class slug that matches nothing fails with `wf:class value "hero-btn" does not match a style block on this site.` A slug that matches more than one class fails with `wf:class value "hero-btn" matches multiple style blocks; use a style-block id array instead.` Look up a style with `webflow.getStyleByName`. List styles with `webflow.getAllStyles`. After a successful write, `get` returns style-block ids, not the slug. A combo class includes its parent ids in that array.

A bare attribute name such as `data-state` is stored as `[data-state]`. An invalid name is rejected. The error says the value must be a CSS attribute selector (`[name]` or `[name="value"]`) or a valid attribute name.

`wf:id` is rejected. Use `wf:selector`, `wf:class`, or `wf:inst`.

`wf:inst` on a site or pages scope is `[pageId, elementId]`. On a component scope it is `[componentId, elementId]`. A component pair on a site or pages scope fails with `wf:inst [componentDefinitionId, elementId] is only valid on component-scoped interactions; page/site Element targets must be [pageId, elementId].` The component root uses the same id in both slots, `[componentId, componentId]`. `wf:inst` does not take a scope wrapper.

An unknown `wf:` target type is rejected as not a known target type.

## Filter

`filterContext.relationship` is `none`, `within`, `direct-child-of`, `contains`, `direct-parent-of`, `next-to`, `next-sibling-of`, or `prev-sibling-of`.

`filterBy` is `[extensionKey, value]`. Filter-by cannot be `wf:body`, `wf:viewport`, or `wf:any-element`. Filter by a class, a selector, an attribute, an element (`wf:inst`), or the trigger element (`wf:trigger-only` or `wf:trigger-only-parent`).

When you omit `filterContext`, it is stored as:

```ts
const defaultFilter = {
  relationship: 'none' as const,
  filterBy: ['wf:class', []] as ['wf:class', []],
  firstMatchOnly: false,
};
```

`firstMatchOnly: true` with `relationship: 'none'` is rejected.

`wf:any-element` with `relationship: 'none'`, or with no filter, fails with `"wf:any-element" requires a filter relationship other than "none".` The sentence is prefixed with the target location, for example `trigger "wf:click" target:`.
