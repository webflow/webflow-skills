# Custom event

`extensionKey` is `wf:custom`. The trigger target is `wf:body` with `value: ''`. The event name is `config.pluginConfig.eventName`. Putting `eventName` on `config` drops it, the write still succeeds, and the trigger never plays.

`hero-btn` must already exist as exactly one class.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Custom event flash',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:custom',
      config: {
        control: 'play',
        pluginConfig: {eventName: 'my-event'},
      },
      target: {extensionKey: 'wf:body', value: ''},
    },
  ],
  timelines: [
    {
      name: 'Flash',
      actions: [
        {
          id: 'custom-flash',
          name: 'Flash',
          tt: 2,
          timing: {duration: 0.4, ease: 2},
          properties: {'wf:transform': {opacity: ['100%', '20%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

Any other target, and a missing target, fail with `Trigger "wf:custom" must use the hidden "wf:body" target the Designer writes.`

`eventName` must be a string. A whitespace-only name is rejected. An absent `eventName` is saved and does not play. `get` will not invent a name for you.

`config.control` uses the standard set: `restart`, `play`, `reverse`, `reverseFlipEase`, `pause`, `resume`, `togglePlayReverse`, `togglePlayReverseFlipEase`, `stop`, and `none`.

## Page code that fires the event

The published page listens through the interactions module. Dispatching a DOM event does not call that module, so the interaction does not play. After the page has loaded interactions, run:

```js
const interactionsApi = Webflow.require('ix3');
interactionsApi.emit('my-event');
```

`emit` is the method that fires `my-event`. The first argument is the same string you stored in `pluginConfig.eventName`.
