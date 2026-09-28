# Scroll

`extensionKey` is `wf:scroll`. Scroll is the only trigger on the interaction. A second trigger fails with `Trigger "wf:scroll" cannot be combined with other triggers; the Designer only allows it as the sole trigger on an interaction.`

The trigger needs a target and `config.scrollTriggerConfig`. `start` and `end` are each two positions separated by a space, such as `top bottom` or `top 80%`. A position is `top`, `center`, `bottom`, `left`, or `right`, a number or percent such as `50%` or `-20px`, or a keyword plus an offset such as `top+=50`.

Do not set `control`, `delay`, `jump`, or `speed` on the trigger. Do not set `endTrigger`, `scroller`, or `horizontal: true`. When you set `pin`, it is a boolean. Omit `controlType`, or set it to `scroll`.

Toggle values are `play`, `pause`, `resume`, `reverse`, `restart`, `reset`, `complete`, and `none`. If you omit `enter`, `leave`, `enterBack`, or `leaveBack`, they are stored as `play`, `none`, `none`, and `none`. An explicit `none` stays `none`.

`hero-btn` must already exist as exactly one class. Read [actions.md](actions.md) and [targets.md](targets.md).

## Plays once

Omit `scrub`. Send `enter: 'play'`. `leaveBack: 'reset'` replays the reveal when the reader scrolls back up. Do not set `canvasDuration`. Use a From tween so the element starts hidden.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Scroll reveal',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:scroll',
      config: {
        scrollTriggerConfig: {
          start: 'top 90%',
          end: 'bottom 15%',
          enter: 'play',
          leaveBack: 'reset',
        },
      },
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Reveal',
      actions: [
        {
          id: 'scroll-reveal',
          name: 'Reveal',
          tt: 1,
          timing: {duration: 0.6, ease: 2},
          properties: {'wf:transform': {opacity: ['0%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

`get` adds `leave: 'none'` and `enterBack: 'none'` when you omitted them. That is expected.

## Scrubs

`scrub` is a nonnegative number of seconds, such as `0.3`. `true` is rejected. The timeline sets `canvasDuration: 1`, has no `triggerMetadata.role`, and the action `duration` is `1` so the tween spans the scrub. Do not set `timing.repeat` or `timing.yoyo`.

```ts
const page = await webflow.getCurrentPage();

const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Scroll scrub fade',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:scroll',
      config: {
        scrollTriggerConfig: {
          start: 'top bottom',
          end: 'top 10%',
          scrub: 0.3,
        },
      },
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Scrub',
      canvasDuration: 1,
      actions: [
        {
          id: 'scroll-scrub',
          name: 'Fade',
          tt: 2,
          timing: {duration: 1, ease: 2},
          properties: {
            'wf:transform': {opacity: ['0%', '100%'], xPercent: [-40, 0]},
          },
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});

const saved = await webflow.interactions.get(created.id);
```

A missing target fails with `Trigger "wf:scroll" requires a trigger target — the element whose scroll position drives the timelines.` A missing `scrollTriggerConfig` fails with `Trigger "wf:scroll" requires a "scrollTriggerConfig" (its scroll start/end settings); without it the runtime ignores the trigger.`
