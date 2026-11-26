# Traps

After every `create` or `set`, call `get` and compare the stored interaction with the payload you sent. TypeScript will not catch a field placed on the wrong object.

## Rejected with an error

The call throws. Fix the payload and send it again.

| What you sent | What you see | Fix |
| --- | --- | --- |
| A write while `canModifyInteractions` is false | `User does not have permission to modify interactions.` | Check `webflow.canForAppMode` first. Writes need the main branch, the canvas workflow, and Design mode. |
| A read while `canReadInteractions` is false | `User does not have permission to access interactions.` | The same check, for reads. |
| `wf:click` or `wf:hover` with no target | `Trigger "wf:click" requires a target element; the Designer always prompts for one in the trigger configuration panel.` | Add a target. The hover sentence uses `wf:hover`. |
| `wf:load` with a target | `Trigger "wf:load" must not carry a target; page load fires once for the page and the Designer never attaches an element to it. Target elements on the timeline actions instead.` | Remove the trigger target. |
| `wf:load` with `pluginConfig` | `Trigger "wf:load" must not set pluginConfig` | Send `config: {control: 'play'}` only. |
| Two `wf:load` triggers | `An interaction may have at most one "wf:load" (Page load) trigger.` | Keep one. |
| `wf:scroll` or `wf:mouse-move` plus another trigger | `Trigger "wf:scroll" cannot be combined with other triggers; the Designer only allows it as the sole trigger on an interaction.` | One trigger. The mouse-move sentence uses `wf:mouse-move`. |
| `wf:scroll` with no target | `Trigger "wf:scroll" requires a trigger target — the element whose scroll position drives the timelines.` | Add a target. |
| `wf:scroll` with no `scrollTriggerConfig` | `Trigger "wf:scroll" requires a "scrollTriggerConfig" (its scroll start/end settings); without it the runtime ignores the trigger.` | Send `start` and `end`. |
| `wf:custom` with any target other than `wf:body`, or with no target | `Trigger "wf:custom" must use the hidden "wf:body" target the Designer writes.` | `target: {extensionKey: 'wf:body', value: ''}`. |
| `eventMode` without a boolean `multiTimeline` | `Trigger "wf:hover" pluginConfig sets "eventMode" without a boolean "multiTimeline"; the Designer only offers the event type selector on the multi-timeline hover editor.` | Set `multiTimeline` to `true` or `false` beside `eventMode`. |
| `eventMode` together with `type`, `hover`, or `custom` | The error names the extra field and says the multi-timeline editor cannot show or clear it. | Use one hover form. See [trigger-hover.md](trigger-hover.md). |
| `wf:navbar`, `wf:dropdown`, `wf:focus`, `wf:blur`, `wf:change`, or any other trigger key | The write is rejected. | Use `wf:click`, `wf:hover`, `wf:load`, `wf:scroll`, `wf:custom`, or `wf:mouse-move`. |
| An action key other than the nine in [actions.md](actions.md) | The write is rejected. | Move the property under a supported action key. |
| A property on the wrong action, or a set-only property without `tt: 3` | The error names the property and, for a set-only property, says it must be used in a Set action (`tt: 3`). | See [actions.md](actions.md). |
| `timing.delay` on an action | `timing.delay is not applied to an action; the runtime ignores it. Use timing.position to sequence actions within a timeline, or set delay on the trigger or on the timeline's settings.` | Use `timing.position`, or delay on the trigger or on `timeline.settings`. |
| A `timelineDefaults` object | `timelineDefaults is not authored by the Designer; omit the field, or pass null on set to clear a stored value.` | Omit it. On `set`, `null` clears a stored value. |
| A class slug that matches nothing | `wf:class value "hero-btn" does not match a style block on this site.` | Create the class, or pass a style-block id from `webflow.getAllStyles()`. |
| A class slug that matches more than one class | `wf:class value "hero-btn" matches multiple style blocks; use a style-block id array instead.` | Pass the id array. |
| `wf:id` | The target type is not offered. | Use `wf:selector`, `wf:class`, or `wf:inst`. |
| `conditionalLogic` on a trigger you pass to `create` or `set` | The write is rejected. | Use `conditionalPlayback`. |
| `assignedTimelineRole` on a new trigger | `Trigger "wf:click" must not set assignedTimelineRole; the Designer writes assignedGroupId to route a trigger to a timeline group.` | Use `assignedGroupId` and a timeline `groupId`. |
| `scrub: true` | The write is rejected. | Use a nonnegative number of seconds, such as `0.3`, or omit `scrub` for a play-once scroll. |
| The Designer does not confirm the write | `The write may or may not have been applied; read the interaction before retrying.` | Call `get` before you retry. |

`conditionalPlayback` is how you limit playback. One row per `type`. A second row of the same type is rejected.

```ts
const reducedMotion: {
  type: 'prefers-reduced-motion';
  behavior: 'dont-animate';
} = {type: 'prefers-reduced-motion', behavior: 'dont-animate'};

const smallScreens: {
  type: 'breakpoint';
  breakpoints: Array<'main' | 'medium' | 'small' | 'tiny'>;
  behavior: 'dont-animate';
} = {
  type: 'breakpoint',
  breakpoints: ['medium', 'small', 'tiny'],
  behavior: 'dont-animate',
};
```

`behavior` is `dont-animate` or `skip-to-end`. Breakpoints are `main`, `medium`, `small`, and `tiny`. On a mouse-move interaction, `skip-to-end` is rejected. Use `dont-animate`.

A `set` that omits `triggers` keeps a stored `conditionalLogic` value. Sending `triggers` again, including a copy you just read with `get`, rejects that bag. Build the triggers you send without `conditionalLogic`.

## Accepted but changed

The call resolves. `get` does not match what you sent.

Unknown keys on `config` are dropped. The declared keys are `delay`, `control`, `jump`, `speed`, `controlType`, `scrollTriggerConfig`, `pluginConfig`, `assignedGroupId`, `assignedTimelineRole`, and `conditionalLogic`. Plugin fields belong under `pluginConfig`: `eventName`, `eventMode`, `multiTimeline`, `click`, `hover`, `smoothness`, `restingState`.

`config: {eventMode: 'leave'}` saves without `eventMode`. The same field under `config.pluginConfig`, next to a boolean `multiTimeline`, is still there on `get`.

Unknown keys on `timing` are dropped. The ease field is `ease`. `timing: {duration: 0.4, easing: 2}` saves the duration and drops `easing`, so the action plays with no easing.

Unknown keys on `stagger` are dropped. `stagger` itself must be an object. A number is rejected, which is the previous section, not this one.

A class slug is stored as a style-block id array. A combo class includes its parent ids. Compare ids, not the slug.

A bare attribute name is stored as `[name]`.

`"500ms"` is stored as `0.5`. `delay: null` is stored as `0.25`.

An omitted `scope` is stored as `{type: 'site'}`.

An omitted `controlType` is stored as `load` on page load, `scroll` on scroll, and `continuous` on mouse move. Click, hover, and custom event leave it unset when you omit it.

Omitted scroll `enter`, `leave`, `enterBack`, and `leaveBack` are stored as `play`, `none`, `none`, and `none`. An explicit `none` stays `none`.

An omitted `tt` may be stored as `1` or `2` when the value shapes imply From or fromTo.

An omitted `filterContext` is stored as `{relationship: 'none', filterBy: ['wf:class', []], firstMatchOnly: false}`.

An ease index above `30` is stored. It plays as no easing. Use `0` through `30`.

## Saved but never animates

`get` matches the stored interaction, and Preview or the published page does not move the way you expected.

- `wf:custom` with no `pluginConfig.eventName`. The write succeeds. Nothing is listening. Set the name, then fire it with `Webflow.require('ix3').emit('my-event')`. A DOM event does not call `emit`.
- `hidden: true` on an action. That action is excluded from Preview and from the published page.
- A from-to opacity that starts at `0%`. The element stays at `0%` until the trigger runs. That is the from-to rest state, not a failed write.
- A site scope, which is what you get when you omit `scope`. The interaction runs on every page. Pass `{type: 'pages', value: [page.id]}` when it should run on the current page only.
- `getAll` does not return Classic Interactions. An empty list can hide motion the published page still runs. Ask the user to check the interactions version control in the Designer. The other version is labeled Classic Interactions.
- An ease index above `30`, or a dropped `easing` key. The action plays with no easing.

`getAll({pageId: ''})` returns no rows. Pass `page.id` from `webflow.getCurrentPage()`.
