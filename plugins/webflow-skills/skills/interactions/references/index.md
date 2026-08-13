<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/index.md
     Do not edit here. Edit the source and re-publish. -->

# IX3 agent pack — reference index

Hand-written half of the IX3 authoring contract, for agents building interactions
through the Designer Extension or MCP write path.

The generated half is [`capabilities.generated.md`](capabilities.generated.md):
trigger and action capability tables, target legality, property allowlists, value
modes. Those are rendered from exported constants and cannot drift. Everything
here lives inside a guard body instead, so it is maintained by hand.

## Governing rule

Send only what the Interactions panel can author. The storage schema
(`parseIX3DataStrict`) is deliberately permissive so legacy and runtime data still
parse; the authoring boundary is `designerInvariants.ts`. A payload that satisfies
the schema can still be refused.

## Which file to read

Read the file for the trigger you are building, plus `envelope-and-targets.md`.
That pair is enough to author any single-trigger interaction.

| Building                                      | Read                                             |
| --------------------------------------------- | ------------------------------------------------ |
| Click                                         | [`trigger-click.md`](trigger-click.md)           |
| Hover / mouse enter / mouse leave             | [`trigger-hover.md`](trigger-hover.md)           |
| Page load                                     | [`trigger-load.md`](trigger-load.md)             |
| Scroll, scroll scrub, parallax                | [`trigger-scroll.md`](trigger-scroll.md)         |
| Mouse move, cursor follow                     | [`trigger-mouse-move.md`](trigger-mouse-move.md) |
| Custom JS event                               | [`trigger-custom.md`](trigger-custom.md)         |
| Navbar, dropdown, conditions, Rive, variables | [`gated-capabilities.md`](gated-capabilities.md) |

| Also relevant                                         | Read                                                     |
| ----------------------------------------------------- | -------------------------------------------------------- |
| Envelope, IDs, scope, targets, filters                | [`envelope-and-targets.md`](envelope-and-targets.md)     |
| Animation properties, values, `tt`, timing, splitText | [`actions-and-properties.md`](actions-and-properties.md) |
| Timeline roles, groups, percent canvas                | [`timelines-and-groups.md`](timelines-and-groups.md)     |
| Reduced motion, breakpoint playback rules             | [`conditional-playback.md`](conditional-playback.md)     |
| Editing an existing interaction                       | [`updating-interactions.md`](updating-interactions.md)   |
| Size and count limits                                 | [`limits-and-budgets.md`](limits-and-budgets.md)         |
| A write succeeded but the user cannot edit it         | [`panel-traps.md`](panel-traps.md)                       |
| Decoding a rejection message                          | [`rejects-index.md`](rejects-index.md)                   |

## Enforcement tags

Every rule carries exactly one. They are not interchangeable — each implies
different behavior when you hit it.

| Tag                     | Meaning                                                                                                                | What to do                                                                                                 |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `[REQUIRED]`            | Must be present.                                                                                                       | Always send it.                                                                                            |
| `[OMIT]`                | The Designer never writes it.                                                                                          | Leave the key out entirely. Do not send a default.                                                         |
| `[REJECTED]`            | The write path refuses it. Cites the guard and a message fragment.                                                     | Never author. The error explains itself.                                                                   |
| `[PENDING]`             | The rejection is written but has not landed on every build yet. The guard is named so it can be verified once it does. | Never author. Do **not** rely on getting an error — today the write may succeed silently.                  |
| `[GATED]`               | Not authorable through this API today. The guards take no flag or session parameter, so every caller is refused.       | Do not attempt. Tell the user the capability is unavailable.                                               |
| `[PANEL-TRAP]`          | The API accepts it, but the Interactions panel cannot author, display, edit, or clear the result.                      | Do not author unsolicited. If explicitly asked, warn that the result will not be editable in the Designer. |
| `[LEGACY-OK-ON-UPDATE]` | Refused on create, but forwarded unchanged when an existing interaction is updated without replacing that field.       | On a read-then-write flow, pass the stored value through untouched. Do not "fix" it.                       |

`[PANEL-TRAP]` is the class no error will ever teach you: the write succeeds and
the damage is only visible to the human afterwards.

## Maintaining this pack

These files are **published copies**. The source of record is the Webflow
monorepo at `packages/systems/ix3/schema/agent-pack/`, where the capability
tables are generated from code and a test fails when they drift.

Edit there and re-publish. Changes made directly in this repo will be
overwritten and are not covered by the drift gate.
