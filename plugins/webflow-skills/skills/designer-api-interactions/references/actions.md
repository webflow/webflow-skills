# Actions and properties

Each action has `id`, `name`, `timing`, `properties`, and `targets`. `tt` is the tween type. Property names belong under one action key. A name under the wrong key is rejected, and the error lists the names that key supports. `opacity` under `wf:style` is rejected as a `wf:transform` property.

## Action keys and property names

`wf:transform`: `opacity`, `autoAlpha`, `display`, `x`, `y`, `xPercent`, `yPercent`, `scale`, `scaleX`, `scaleY`, `z`, `skewX`, `skewY`, `rotation`, `rotationX`, `rotationY`, `transformPerspective`, `transformOrigin`, `width`, `height`.

`wf:style`: `backgroundColor`, `borderColor`, `color`, `zIndex`, `position`, `overflow`, `pointerEvents`.

`wf:class`: `class`.

`wf:lottie`: `manualDuration`, `lottie`.

`wf:spline`: `objectId`, `animatingState`, `spline`.

`wf:mouse-follow`: `axis`, `leaveBehavior`, `onEnter`, `anchor`, `groupId`, `syncedActionId`, `followMode`. Only on a `mouseX` or `mouseY` timeline of a `wf:mouse-move` interaction, and only one such action on that timeline. `axis` is `x` or `y`. `leaveBehavior` is `return` or `stay`. `onEnter` is `animate` or `snap`. `followMode` is `full`, `x-only`, or `y-only`. `y-only` conflicts with role `mouseX`. `x-only` conflicts with role `mouseY`.

`wf:variable`: `variable`.

`wf:rive`: `rive`.

`wf:animate-rive`: `rive`.

Any other action key is rejected.

## Tween type

`tt` is `0` (to), `1` (from), `2` (fromTo), or `3` (set).

- A scalar, such as `x: '8px'` or `display: 'none'`, is a To value.
- `[from, to]`, such as `opacity: ['0%', '100%']`, is fromTo.
- `[from]` or `[from, null]` is From.
- `[null, to]` is To.

Omit `tt` and a real `[from, to]` pair with no From-only sibling is stored as `2`. When every transform and style value is From, it is stored as `1`. Scalar-only and To-only payloads stay omitted and play as To. Mixing From-only and To-only shapes without `tt` is rejected.

These combinations are rejected:

- `[from, to]` with `tt` `0`, `1`, or `3`.
- `tt: 1` with a scalar or `[null, to]`.
- `tt: 2` with `[from]` or `[from, null]`.
- `tt` `0` or `3` when every value is From-only.

Do not write a plain `{from, to}` object. Use an array or a scalar. The error says to use an array, a scalar To value, `[from]`, `[from, to]`, or a random or additive wrapper.

`transformOrigin` is one value, such as `'50% 50%'`. Two endpoints are rejected. The Origin control writes one value, and that value is used for both ends of the tween.

## Set-only properties

These properties require `tt: 3`. Any other `tt` is rejected:

- `wf:transform` `display`
- `wf:style` `zIndex`, `position`, `overflow`, `pointerEvents`
- `wf:class` `class`

```ts
const page = await webflow.getCurrentPage();

await webflow.interactions.create({
  pageId: page.id,
  name: 'Hide on click',
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
      actions: [
        {
          id: 'hide',
          name: 'Hide',
          tt: 3,
          timing: {},
          properties: {'wf:transform': {display: 'none'}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});
```

## Time, position, and delay

`duration` is seconds or a `"123ms"` string. `"500ms"` is stored as `0.5`. `delay: null` is stored as `0.25`. It does not clear a delay. Omit `delay` when you do not want one.

`timing.delay` on an action is rejected: `timing.delay is not applied to an action; the runtime ignores it. Use timing.position to sequence actions within a timeline, or set delay on the trigger or on the timeline's settings.`

`timing.position` is a finite number of seconds or a `"500ms"` string. `+=0.5`, `<`, and `>` are rejected.

`repeat` is a count. `-1` repeats without a set end. `yoyo: true` plays forward and then backward. Do not set `autoReverse`. On a scroll scrub, do not set `repeat` or `yoyo` on the action.

## Ease

`timing.ease` is an integer from 0 through 30, or an advanced object with a `type` field. A string such as `"power2.out"` is rejected. An integer above 30 is stored and plays as no easing. Unknown keys on `timing`, including `easing`, are dropped, and the action plays with no easing.

| Index | Ease | Index | Ease |
| --- | --- | --- | --- |
| 0 | `none` | 16 | `bounce.in` |
| 1 | `power1.in` | 17 | `bounce.out` |
| 2 | `power1.out` | 18 | `bounce.inOut` |
| 3 | `power1.inOut` | 19 | `circ.in` |
| 4 | `power2.in` | 20 | `circ.out` |
| 5 | `power2.out` | 21 | `circ.inOut` |
| 6 | `power2.inOut` | 22 | `elastic.in` |
| 7 | `power3.in` | 23 | `elastic.out` |
| 8 | `power3.out` | 24 | `elastic.inOut` |
| 9 | `power3.inOut` | 25 | `expo.in` |
| 10 | `power4.in` | 26 | `expo.out` |
| 11 | `power4.out` | 27 | `expo.inOut` |
| 12 | `power4.inOut` | 28 | `sine.in` |
| 13 | `back.in` | 29 | `sine.out` |
| 14 | `back.out` | 30 | `sine.inOut` |
| 15 | `back.inOut` |  |  |

Advanced `type` values, and the fields each object includes:

- `back`: `curve`, `power`
- `elastic`: `curve`, `amplitude`, `period`
- `steps`: `stepCount`
- `rough`: `templateCurve`, `points`, `strength`, `taper`, `randomizePoints`, `clampPoints`
- `slowMo`: `linearRatio`, `power`, `yoyoMode`
- `expoScale`: `startingScale`, `endingScale`, `templateCurve`
- `customWiggle`: `wiggles`, `wiggleType`
- `customBounce`: `strength`, `squash`, `endAtStart`
- `customEase`: `bezierCurve`

`curve` is `in`, `out`, or `inOut`. `taper` is `none`, `in`, `out`, or `both`. `wiggleType` is `easeOut`, `easeInOut`, `anticipate`, `uniform`, or `random`. An extra field on the ease object is rejected.

## Stagger

`timing.stagger` is an object. A number is rejected. Fields: `amount`, `each`, `axis` (`x` or `y`), `from` (`start`, `center`, `end`, `edges`, `random`, or a number), `ease` (the same ease values as `timing.ease`), and `grid` (`'auto'` or `[columns, rows]`). Unknown keys on `stagger` are dropped.

```ts
const staggerTiming = {
  duration: 0.4,
  stagger: {each: 0.08, from: 'start' as const},
};
```

## Split text

`splitText` is `{type: 'chars' | 'words' | 'lines'}`. When `mask` is present it equals `type`. A string such as `'chars'` is rejected on create.

## Class change

`tt` is `3`. `selectors` is an array of style-block id strings, not class slugs. `operation` is `addClass`, `removeClass`, or `toggleClass`.

```ts
const page = await webflow.getCurrentPage();
const style = await webflow.getStyleByName('is-active');
if (style) {
  await webflow.interactions.create({
    pageId: page.id,
    name: 'Add class on click',
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
        actions: [
          {
            id: 'add-class',
            name: 'Add class',
            tt: 3,
            timing: {},
            properties: {
              'wf:class': {
                class: {operation: 'addClass', selectors: [style.id]},
              },
            },
            targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
          },
        ],
      },
    ],
  });
}
```

## Variable and Rive

Variable value `type` is `number`, `length`, `percentage`, `color`, or `ref`. `value` may be `null` when it is unset. Length is `{value: number, unit: string}`. Percentage uses unit `"%"`. A unitless number uses unit `"-"`. Color is a color string. A reference is `{type: 'ref', value: {variableId}}`.

```ts
const variableProperties = {
  'wf:variable': {
    variable: {
      variables: [
        {
          variableId: 'variable-id',
          value: {type: 'length', value: {value: 16, unit: 'px'}},
        },
      ],
    },
  },
};
```

Use `tt: 3` for this assignment. `value: null` means the value is unset.

Rive set:

```ts
const riveProperties = {
  'wf:rive': {
    rive: {
      animationSource: {name: 'State machine'},
      addedProperties: {
        'pressed:pressed': {
          propertyName: 'pressed',
          propertyType: 'boolean' as const,
          value: true,
        },
      },
    },
  },
};
```

`animationSource` is `null` or `{name, instanceName?}`. `addedProperties` is an object. A non-empty map requires `animationSource`. Each entry is `{propertyName, propertyType, value?}`. `propertyType` is `string`, `number`, `boolean`, `color`, `enum`, `trigger`, or `artboard`. The map key ends with `:${propertyName}`.

Animate Rive uses `wf:animate-rive` and `propertyType` `number` or `color`.

Lottie `lottie` is `{from, to}` as numbers or `{type: 'ref', value: {variableId}}`, plus optional `manualDuration: boolean`.

Spline `objectId` is a string. `spline` is a map of channel objects `{from?, to?}`. Channels include `positionX`, `positionY`, `positionZ`, `rotationX`, `rotationY`, `rotationZ`, `scaleX`, `scaleY`, `scaleZ`, `intensity`, `opacity`, `zoom`, `color`, and `stateName`.

## Timeline settings

`timeline.settings` may include `control`, `delay`, `jump`, `speed` from 0 through 10, `repeat` (`-1` or `>= 0`), and `yoyo`. Omit `duration`, `ease`, `repeatDelay`, `stagger`, and `position` there. Those belong on the action.

Omit `timelineDefaults` on create. On `set`, pass `null` to clear a stored value. An object fails with `timelineDefaults is not authored by the Designer; omit the field, or pass null on set to clear a stored value.`

Omit `actionPresetIds`, `previewSpeed`, `playInReverse`, and `immediate`. `canvasDuration`, when you set it, is `1`, and only on a scroll-scrub timeline or a mouse X or mouse Y timeline.

Create allows at most 20 triggers, 5 timelines, 200 actions on a timeline, and 20 targets on an action.
