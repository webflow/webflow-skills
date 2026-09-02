<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/gated-capabilities.md
     Do not edit here. Edit the source and re-publish. -->

# Gated and unsupported capabilities

Everything on this page is `[GATED]`: refused by the write path today. The guards
take no flag or session argument, so this is true for every caller regardless of
Statsig state — do not attempt these, and tell the user the capability is
unavailable through the API rather than producing a payload that will be
rejected.

Two different reasons are collapsed into one behavior, and the distinction
matters for what you tell the user.

## Gated pending GA

Registered in the Designer, excluded from the API's default capability set until
the feature reaches general availability. These will become authorable.

| Capability                       | Kind           | Guard                           |
| -------------------------------- | -------------- | ------------------------------- |
| `wf:navbar`                      | trigger        | `findFlagGatedTriggerError`     |
| `wf:dropdown`                    | trigger        | `findFlagGatedTriggerError`     |
| `wf:variable`                    | action         | `findFlagGatedActionError`      |
| `wf:rive`                        | action         | `findFlagGatedActionError`      |
| `wf:animate-rive`                | action         | `findFlagGatedActionError`      |
| Trigger-level `conditionalLogic` | trigger config | `findConditionsCapabilityError` |

Fragment for triggers and actions:
`is not in the Designer's default capability set`

The MCP tool layer emits its own variant of that message before the guard runs,
so the exact wording differs by surface. See
[`rejects-index.md`](rejects-index.md).

### Navbar and dropdown, for when they land

Recorded here so this file stays useful at GA rather than being rewritten. Do not
author against it yet.

Both are standalone. Their roles are `open` and `close`: each supplied timeline
needs one of the two and they must be unique, but the guard does **not** require the
pair, so a single `open` timeline is valid. Do not add a second timeline purely to
satisfy validation.

The playback editor is hidden, **but the panel still writes `control: 'play'`** and
`findGroupedTriggerControlError` requires it once the interaction has two or more
grouped timelines. They are deliberately excluded from `NO_PLAYBACK_CONTROL_TYPES`
for exactly that reason: rejecting the field would make the two guards contradict
each other.

**Send a target.** The panel supplies one through `ComponentTriggerTarget`, which
writes a `wf:inst` target for the navbar or dropdown instance. Validation does not
demand it, but `bindTrigger` only resolves elements when a target is present, so a
targetless navbar interaction saves and never fires. This is the same trap as
mouse-move, described in [`trigger-mouse-move.md`](trigger-mouse-move.md).

### Conditions

`CONDITIONS_DEFAULT_ON` is `false`, so `findConditionsCapabilityError` refuses
trigger-level `conditionalLogic` outright and wins over any deeper
outcome-shape message — **in the host**.

Through MCP the argument schema runs first, so an incomplete `conditionalLogic`
never reaches the capability check. Measured: `config: {conditionalLogic:
{conditions: []}}` returns `triggers.0.config.conditionalLogic.ifTrue:
Required`. Do not read that as "supply `ifTrue` and this will work" — it is a
shape error in front of a closed door, and completing the shape only moves you to
the capability refusal. The capability is off either way.

This is **only** about trigger `conditionalLogic`. Interaction-level
`conditionalPlayback` is a separate field and **is** authorable — see
[`conditional-playback.md`](conditional-playback.md). Do not conflate them.

## No Designer schema at all

Runtime-only trigger keys with no `addTriggerSchema` registration. Unlike the
gated set, there is no plan that makes these authorable.

| Key         | Why                              |
| ----------- | -------------------------------- |
| `wf:focus`  | runtime-only, no Designer schema |
| `wf:blur`   | runtime-only, no Designer schema |
| `wf:change` | runtime-only, no Designer schema |

They are deliberately kept out of the default-on set so the DE, MCP, and
code-views lanes all refuse to author them.

## Why the generated table cannot tell these apart

[`capabilities.generated.md`](capabilities.generated.md) marks both
groups simply as not authorable. The set that distinguishes them
(`FLAG_GATED_TRIGGER_KEYS`) is private to `designerInvariants.ts`, and it was not
exported merely to improve a docs table. That is why this file exists.
