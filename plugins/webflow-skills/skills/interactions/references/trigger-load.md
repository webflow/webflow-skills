<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-load.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:load`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|              |                                                         |
| ------------ | ------------------------------------------------------- |
| controlType  | `load` (omit and the host stamps it)                    |
| Standalone   | No, but at most **one** per interaction                 |
| Target       | `[OMIT]` — must not be present                          |
| pluginConfig | `[OMIT]` — must be empty or absent                      |
| Roles        | None                                                    |
| Playback     | `control` limited to `play` or `none`. `delay` allowed. |

Page load is the one trigger the panel gives no configuration surface at all: it
registers `component: null`, no `defaultTarget`, and an empty `defaultValue`. A
native load trigger is always a bare tuple with an empty `pluginConfig`.

## Accept

```js
{
  pageId,
  name: 'Load',
  triggers: [{extensionKey: 'wf:load', config: {control: 'play'}}],
  timelines: [{
    actions: [{
      ...ACTION,
      targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
    }],
  }],
}
```

## Rejected

`[REJECTED]` Any `target` on the trigger. Page load fires once for the page and
the Designer never attaches it to an element.
Guard: `findLoadTriggerPurityError` · fragment: `must not carry a target`

`[REJECTED]` Any `pluginConfig` key, including `triggerPoint`. DE writes stamp
`controlType: 'load'`, which routes through `LoadTriggerStrategy` — that strategy
never reads `triggerPoint`, so it is dormant rather than a lever for publish
timing, and the panel can neither show nor clear it.
Fragment: `must not set pluginConfig`

`[REJECTED]` A second `wf:load` trigger in the same interaction.
Guard: `findMultipleLoadTriggerError` · fragment: `at most one`

`[REJECTED]` A `control` outside `play` / `none`. There is no timeline to resume.
Guard: `findTriggerControlAllowedError`

`[REJECTED]` Action targets `wf:trigger-only` or `wf:trigger-only-parent`. With no
trigger element they bind against nothing.
Guard: `findActionTargetContextError`

`[REJECTED]` `controlType` explicitly set to something other than `load`. A
mismatch binds the wrong runtime strategy and the trigger never fires.
Guard: `findControlTypeMismatchError` · fragment: `requires controlType`
