# Hover

`extensionKey` is `wf:hover`. Each trigger needs a target.

This example is an enter and a leave that fades out. It is two triggers and two timeline groups. `eventMode` is `enter` or `leave`, and it sits in `config.pluginConfig` next to `multiTimeline: false`. Two grouped timelines require `control: 'play'`.

`hero-btn` must already exist as exactly one class. The enter action is a from-to from `0%` to `100%`, so the element stays at `0%` until the pointer enters. Say that to the user.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Hover fade',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:hover',
      config: {
        control: 'play',
        assignedGroupId: 'hover-in',
        pluginConfig: {multiTimeline: false, eventMode: 'enter'},
      },
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
    {
      extensionKey: 'wf:hover',
      config: {
        control: 'play',
        assignedGroupId: 'hover-out',
        pluginConfig: {multiTimeline: false, eventMode: 'leave'},
      },
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Enter',
      groupId: 'hover-in',
      actions: [
        {
          id: 'hover-in',
          name: 'Fade in',
          tt: 2,
          timing: {duration: 0.3, ease: 2},
          properties: {'wf:transform': {opacity: ['0%', '100%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
    {
      name: 'Leave',
      groupId: 'hover-out',
      actions: [
        {
          id: 'hover-out',
          name: 'Fade out',
          tt: 2,
          timing: {duration: 0.3, ease: 2},
          properties: {'wf:transform': {opacity: ['100%', '0%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

## Where `eventMode` goes

`eventMode` is `both`, `enter`, or `leave`. It is a `pluginConfig` field. `config: {eventMode: 'leave'}` saves without `eventMode`, and the leave trigger never receives a leave.

`eventMode` also requires a boolean `multiTimeline` beside it. Without that boolean the write fails with `Trigger "wf:hover" pluginConfig sets "eventMode" without a boolean "multiTimeline"; the Designer only offers the event type selector on the multi-timeline hover editor.`

Use `multiTimeline: false` for the two-trigger example above. Each trigger drives its own `groupId`.

Do not also set `type`, `hover`, or `custom` on a trigger that sets `multiTimeline`. Those fields belong to the other hover form, and the write fails when both are present.

## One trigger and two roles

This form is also accepted. One `wf:hover` trigger uses `pluginConfig: {multiTimeline: true}`. The two timelines set `triggerMetadata.role` to `mouseEnter` and `mouseLeave`. Each role is used once. Do not set `type`, `hover`, or `custom` on that trigger. Do not put `eventMode` on `config`.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Hover fade roles',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:hover',
      config: {
        control: 'play',
        pluginConfig: {multiTimeline: true},
      },
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Enter',
      triggerMetadata: {role: 'mouseEnter'},
      actions: [
        {
          id: 'role-in',
          name: 'Fade in',
          tt: 2,
          timing: {duration: 0.3},
          properties: {'wf:transform': {opacity: ['0%', '100%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
    {
      name: 'Leave',
      triggerMetadata: {role: 'mouseLeave'},
      actions: [
        {
          id: 'role-out',
          name: 'Fade out',
          tt: 2,
          timing: {duration: 0.3},
          properties: {'wf:transform': {opacity: ['100%', '0%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

A timeline without one of those roles, or two timelines with the same role, is rejected. The error names the role it expected: `mouseEnter` or `mouseLeave`.

## Other click-like limits

A missing target fails with `Trigger "wf:hover" requires a target element; the Designer always prompts for one in the trigger configuration panel.`

`pluginConfig.hover` uses the same occurrence modes as click (`each`, `first`, `second`, `odd`, `even`, `custom`). `pluginConfig.type` is `mouseenter` or `mouseleave` when you are not using `multiTimeline`. Prefer the `eventMode` example above for an enter and a leave.

`speed` is a finite number from 0 through 10. Do not set `speed` when control is `pause`, `stop`, or `none`. Do not set `jump` when control is `none`, `restart`, `resume`, `togglePlayReverse`, or `togglePlayReverseFlipEase`.
