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

`[REJECTED]` Any target other than `wf:body`, **and** omitting the target
entirely. Both produce the same message from different places: a wrong key is
caught by `findTriggerTargetContextError`, an absent target by the missing-target
branch in `findTriggerInvariantError`.
Fragment: `must use the hidden "wf:body"`

`[REJECTED]` Action targets `wf:trigger-only` or `wf:trigger-only-parent`. There is
no trigger element to bind against.
Guard: `findActionTargetContextError`

## A missing `eventName` is the one silent case the panel does surface

`eventName` written at `config` level instead of `config.pluginConfig` is stripped
before persist, so the trigger stores with no event name and can never fire. The
write returns success and a read echoes the payload without it — see the
silent-strip rule in [`envelope-and-targets.md`](envelope-and-targets.md).

**The Interactions panel flags it.** Verified on an interaction stored that way:
the Event Name field renders empty with a yellow **"No event name"** warning
beside it. That makes this the rare `[SILENTLY-DROPPED]` case with a human-visible
recovery path — nothing in the API surfaces it, but the panel does.

So when a user reports a custom trigger that never fires, send them to the panel
before re-reading the payload. An empty field with that warning confirms the
event name was addressed at the wrong level.
