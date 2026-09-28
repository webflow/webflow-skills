# Page load

`extensionKey` is `wf:load`. Do not send a trigger target. Put the element on the action. `wf:trigger-only` is an action target, and it has no trigger element to follow on page load, so use `wf:class`, `wf:selector`, `wf:attribute`, or `wf:inst` on the action.

`hero-btn` must already exist as exactly one class.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Load fade',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:load',
      config: {control: 'play'},
    },
  ],
  timelines: [
    {
      name: 'Fade',
      actions: [
        {
          id: 'load-fade',
          name: 'Fade',
          tt: 2,
          timing: {duration: 0.6, ease: 2},
          properties: {'wf:transform': {opacity: ['0%', '100%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

A from-to from `0%` to `100%` holds the element at `0%` until the page loads the interaction. Say that to the user.

## Rules

A target fails with `Trigger "wf:load" must not carry a target; page load fires once for the page and the Designer never attaches an element to it. Target elements on the timeline actions instead.`

Any `pluginConfig` key fails. The error names the key: `Trigger "wf:load" must not set pluginConfig`.

An interaction can have one `wf:load` trigger. A second one fails with `An interaction may have at most one "wf:load" (Page load) trigger.`

`config.control` is `play` or `none`. Omit `controlType`, or set it to `load`. Any other value is rejected.

`speed` is a finite number from 0 through 10. Do not set `jump` when control is `restart` or `resume`. Page load does not offer those controls anyway. Do not set `speed` when control is `none`.
