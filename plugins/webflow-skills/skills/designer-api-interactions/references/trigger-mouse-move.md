# Mouse move

`extensionKey` is `wf:mouse-move`. It is the only trigger on the interaction. A second trigger fails with `Trigger "wf:mouse-move" cannot be combined with other triggers; the Designer only allows it as the sole trigger on an interaction.`

Send a target. Page-wide tracking uses `wf:viewport` with `value: ''`. That target is valid only on this trigger. Do not set `control`, `delay`, `jump`, or `speed`. Omit `controlType`, or set it to `continuous`.

Every timeline needs its own `triggerMetadata.role`: `mouseX`, `mouseY`, or `interval`. Do not put `pluginConfig` inside `triggerMetadata`.

`hero-btn` must already exist as exactly one class.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Mouse follow',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:mouse-move',
      config: {},
      target: {extensionKey: 'wf:viewport', value: ''},
    },
  ],
  timelines: [
    {
      name: 'Mouse X',
      triggerMetadata: {role: 'mouseX'},
      actions: [
        {
          id: 'mouse-x',
          name: 'Follow X',
          tt: 2,
          timing: {duration: 0.4},
          properties: {'wf:transform': {x: ['0px', '40px']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
    {
      name: 'Mouse Y',
      triggerMetadata: {role: 'mouseY'},
      actions: [
        {
          id: 'mouse-y',
          name: 'Follow Y',
          tt: 2,
          timing: {duration: 0.4},
          properties: {'wf:transform': {y: ['0px', '40px']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

## Plugin settings

On `config.pluginConfig`, `smoothness` is a finite number from 0 through 2000. `restingState.x` and `restingState.y` are finite numbers from 0 through 100. Omit any key you are not setting.

`conditionalPlayback` on this interaction can use `dont-animate`. `skip-to-end` is rejected because a mouse-move timeline has no end to skip to.

`wf:mouse-follow` is an action, not a trigger. It is only valid on a `mouseX` or `mouseY` timeline. One per timeline. `followMode: 'y-only'` conflicts with `mouseX`. `followMode: 'x-only'` conflicts with `mouseY`. The property list is in [actions.md](actions.md).

A timeline without a role, or two timelines with the same role, is rejected. The error lists `mouseX`, `mouseY`, and `interval`.
