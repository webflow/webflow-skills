<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-custom.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:custom`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|              |                                                    |
| ------------ | -------------------------------------------------- |
| controlType  | `standard`                                         |
| Standalone   | No                                                 |
| Target       | `[REQUIRED]` — **only** `wf:body` with `value: ''` |
| Roles        | None                                               |
| Playback     | Allowed                                            |
| pluginConfig | `{eventName: 'my-event'}`                          |

Custom is the one trigger that must use the hidden body target. It listens for a
JS event rather than binding to an element.

## Accept

```js
{
  pageId,
  name: 'Custom',
  triggers: [{
    extensionKey: 'wf:custom',
    config: {control: 'play', pluginConfig: {eventName: 'my-event'}},
    target: {extensionKey: 'wf:body', value: ''},
  }],
  timelines: [{
    actions: [{
      ...ACTION,
      targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
    }],
  }],
}
```

Emit it in Preview with:

```js
Webflow.require('ix3').emit('my-event');
```

## Rejected

`[REJECTED]` Any target other than `wf:body`.
Guard: `findTriggerTargetContextError` · fragment: `must use the hidden "wf:body"`

`[REJECTED]` Action targets `wf:trigger-only` or `wf:trigger-only-parent`. There is
no trigger element to bind against.
Guard: `findActionTargetContextError`
