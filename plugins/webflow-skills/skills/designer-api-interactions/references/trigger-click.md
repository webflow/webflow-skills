# Click

`extensionKey` is `wf:click`. The trigger needs a target. Action targets are separate. See [targets.md](targets.md) and [actions.md](actions.md).

`hero-btn` in this example must already exist as exactly one class. A from-to opacity of `0%` to `100%` holds the element at `0%` until the first click. Say that to the user. If the element should be visible before the click, animate a property whose rest value is already visible, such as `x`, or use a To tween (`tt: 0` and a scalar).

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Click fade',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:click',
      config: {control: 'play'},
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Fade',
      actions: [
        {
          id: 'click-fade',
          name: 'Fade',
          tt: 2,
          timing: {duration: 0.4, ease: 2},
          properties: {'wf:transform': {opacity: ['0%', '100%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

`ease: 2` is `power1.out`. The index list is in [actions.md](actions.md).

## Rules

A missing target fails with `Trigger "wf:click" requires a target element; the Designer always prompts for one in the trigger configuration panel.`

`config.control` is one of `restart`, `play`, `reverse`, `reverseFlipEase`, `pause`, `resume`, `togglePlayReverse`, `togglePlayReverseFlipEase`, `stop`. `none` is rejected.

`config.pluginConfig.click` is `each`, `first`, `second`, `odd`, `even`, or `custom`. Omit it to fire on every click. When it is not `each`, `togglePlayReverse` and `togglePlayReverseFlipEase` are also rejected. `custom` requires `pluginConfig.custom` as a finite number of at least 1, and `custom` is rejected for every other mode.

Do not set `jump` when control is `none`, `restart`, `resume`, `togglePlayReverse`, or `togglePlayReverseFlipEase`. Do not set `speed` when control is `pause`, `stop`, or `none`. A `speed` you do set is a finite number from 0 through 10.

`eventMode`, `eventName`, and `scrollTriggerConfig` do not belong on a click trigger. An unknown key on `config` is dropped. Put click settings under `config.pluginConfig`.
