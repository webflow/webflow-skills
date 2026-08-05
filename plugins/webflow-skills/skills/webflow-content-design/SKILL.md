---
name: webflow-workflow:webflow-content-design
description: Write or review Webflow product UX copy and content design. Use for buttons, tooltips, modals, errors, empty states, SYBG, updates posts, terminology, or tone.
---

# Content Design & UX Writing

Help Webflow engineers, product designers, and PMs write customer-facing content that's on-brand, consistent, and doesn't need to bounce back from the content design team. Covers voice, tone, grammar, product terminology, Spring component-specific writing rules, release announcements, help documentation, and University articles. The Content Design team can be reached on **#content-design** in Slack — reference this channel when flagging issues or when the user needs human guidance.

---

## How This Skill Works

This skill supports two modes and four content types. Start by figuring out which mode and type the user needs, then follow the corresponding workflow.

### Modes
1. **Write** — Generate new copy from a feature description, Jira ticket, or conversation
2. **Audit** — Review existing copy against the guidelines and return a corrected version with brief notes on what changed

### Content Types
1. **In-product UI copy** — Buttons, tooltips, modals, error messages, empty states, onboarding, dialogs, dashboards, forms, notifications, banners, toasts, tabs, tags, accordions, links, badges
2. **SYBG modal content** — "Since You've Been Gone" entries displayed in the Webflow Dashboard via Knock Guides
3. **webflow.com/updates posts** — Feature release announcements on the public updates page
4. **Help documentation** — Webflow University articles and tutorials

---

## Tradeoff Prioritization

When guidelines conflict, follow this priority order:

**1. Clarity over brevity.** If a 3-word button label is ambiguous but a 4-word version is clear, go with clarity.

**2. User-centeredness over brand voice.** If being "bold" would confuse the user or bury the action, dial it back.

**3. Accessibility over aesthetics.** If a concise link label fails screen reader users, add a descriptive `aria-label` even though it adds engineering work. If a tooltip is the only way to explain an icon-only button, consider whether a visible text label would serve more users.

**4. Consistency over local optimization.** If every other button in a flow says "Create" and this one says "Make," align with the pattern.

When making a tradeoff, flag it briefly — note what was prioritized and why.

---

## Step 1: Understand the Request

Accept input flexibly. The user might:
- Describe the feature and context conversationally
- Paste a Jira ticket or product brief
- Paste existing copy they want reviewed
- Share a screenshot or Figma link
- Point you to a file, component, or PR in the codebase

If the content type isn't obvious, ask. If you need more context to write well, ask — but keep it to 1-2 focused questions, not an interrogation.

Key things to establish:
- **Content type** (UI copy, SYBG, /updates, help doc)
- **Where it appears** (which screen, surface, or page)
- **What the user is doing** when they see this content
- **What the user needs to understand or do next**
- **Severity/emotional context** (especially for errors and alerts)

## Step 2: Investigate Context Before Writing

Copy doesn't exist in a vacuum. A tooltip on a button means nothing until you understand what the button does, what happened before the user got there, what happens after they click it, and what could go wrong. The difference between good and great copy is the depth of understanding behind it.

### What to investigate

**Look at the surrounding code.** When the request involves in-product copy (strings, error messages, tooltips, modals, empty states), look at the component and its neighbors:
- What component renders this copy? What props does it receive? What state triggers it?
- What's the user flow — what screen or action came before this, and what comes after?
- Are there related strings nearby (other error states, loading states, success states) that this copy should be consistent with?
- Is this copy conditional? What are the different states it could appear in?
- Are there existing copy patterns in the same feature area you should match?

**Understand the job to be done.** For every piece of copy, ask: what does the user need to understand or do *right now*, in this exact moment? The answer shapes everything — length, tone, specificity, and what to leave out.

**Check the conversation and PR context.** Often the richest context is in the current conversation, the PR description, or linked Jira tickets. Look for the *why* behind the feature, edge cases, and design constraints (truncation limits, conditional rendering, etc.).

**Look at the user's journey holistically.** If you can, trace the path a user would take to reach this copy to avoid repeating information and match the tone progression of the flow.

### When to skip deep investigation
Not every request needs a full codebase audit. If someone says "write a SYBG for this feature, here's the brief" — you probably have enough. The more ambiguous or contextual the copy, the more investigation pays off. The more standalone the content, the less you need to dig.

## Step 3: Read the Relevant References

Before writing or auditing, read the reference files that apply to the content type.

**Always read:**
- `references/voice-and-tone.md` — The four voice dimensions and how to apply them
- `references/grammar-mechanics.md` — Capitalization, punctuation, pronouns, verb tenses, numbers, and more

**Read based on content type:**
- For **UI copy**: read `references/content-patterns.md` (Section 1), `references/content-checklist.md`, and `references/components.md`
- For **SYBG**: read `references/content-patterns.md` (Section 2)
- For **/updates posts**: read `references/content-patterns.md` (Section 3)
- For **help docs**: read `references/content-patterns.md` (Section 4)

**Read when you need a terminology gut-check:**
- `references/terminology.md` — The Webflow A-Z for capitalization and usage of every product term

## Step 4: Write or Audit

### Writing Mode

Generate **2-3 variants** for the user to choose from. Each variant should:
- Follow all applicable guidelines from the reference files
- Reflect the context you gathered in Step 2 — the user's moment, emotional state, and job to be done should shape the copy, not just the guidelines
- Be labeled with a short description of its angle (e.g., "More concise," "Emphasizes user benefit," "Bolder tone")
- Be ready to ship — not a rough draft

For UI copy, output the exact strings (button text, headline, body, tooltip, etc.) organized by component. Don't write paragraphs explaining what the copy should say — write the actual copy. If your investigation in Step 2 revealed related strings that should be updated for consistency, flag them.

For longer-form content (SYBG, /updates, help docs), still provide 2-3 variants but it's fine if they share the same structure and differ mainly in tone, phrasing, or emphasis.

### Audit Mode

When the user pastes existing copy:
1. Return a **corrected version** — the copy as it should read
2. Below it, include a **brief changelog** — a short bulleted list of what you changed and why, referencing the specific guideline (e.g., "Changed to sentence case per Webflow capitalization standards," "Rewrote to active voice," "Replaced 'please' — can undermine authority in error messages")

Don't lecture. Keep the changelog tight and useful.

---

## Component Quick-Reference

When a user shares a Figma prototype or mentions a component name, identify the Spring component and read the full reference at `references/components.md`.

| Component | Max length | Key rule |
|-----------|-----------|----------|
| **Button** | 3 words | Describe exactly what happens on click. No articles. |
| **Badge** | 1–2 words | Concise attention-grabbing. No "alpha" tags. |
| **Banner** | 2 sentences | Must communicate both the problem AND the solution. |
| **Toast** | A few words | Never truncate. Drop "successfully." |
| **Tooltip** | ~2 lines | No interactive elements. Ancillary info only. |
| **Modal heading** | Short | Confirmations can be questions. Others: declarative. No period. |
| **Modal body** | 3 lines max | Focus on consequences. Don't repeat heading as question. |
| **Tab** | 1–2 words | Same part of speech across all tabs. |
| **Tag** | 1–2 words | Metadata labels — concise and descriptive. |
| **Form label** | 1–2 words | Describe what to input. Label visible above field. |
| **Menu item** | 1–2 words (with desc) or 2 lines (without) | User should know exactly what happens on click. |
| **Link** | Brief standalone sentence | Describe where the user goes. Avoid generic "Learn more." No trailing period. |
| **Error message** | Concise | State problem + resolution. No "please." Don't blame the user. |
| **Empty state** | Short | Don't point out the obvious. Direct to actions that populate. |
| **Accordion label** | Concise | Describe what's inside. Don't repeat in expanded content. |

---

## Worked Examples

### Generating copy: confirmation modal

**Prompt:** "I'm designing a confirmation modal for when someone tries to delete a Workspace."

**Output:**

| Slot | Copy |
|------|------|
| Title | Delete this Workspace? |
| Body | This will permanently remove the Workspace, all its sites, and member access. This can't be undone. |
| Secondary button | Cancel |
| Primary button | Delete Workspace |

Guidelines applied: Sentence case, "Workspace" capitalized, title is a question (confirmation modal), body focuses on consequences, buttons ≤3 words and clearly differentiated, no "Are you sure?" pattern.

### Reviewing copy: empty state audit

**Prompt:** "Review this empty state — Heading: 'There's Nothing Here Yet!' / Body: 'You haven't created any activity. Click below to start.' / Button: 'Start Creating Activity Now'"

**Review:**
- **Heading** — three issues: title case (should be sentence case), exclamation point (not appropriate for empty state), points out the obvious. → **"Start tracking site changes"**
- **Body** — two issues: "Click below" not accessible (assumes mouse), blames user for automatic activity. → **"Activity will appear here as changes are made to this site."**
- **Button** — exceeds 3-word max, "Creating Activity" doesn't make sense (activity is automatic). → **"Open Designer"** or remove CTA entirely.

---

## After Writing

Once you've delivered variants or an audit, be ready for:
- "Can you make it shorter / punchier / more empathetic?"
- "Which one do you recommend?"
- "Can you write the tooltip too?"
- "Now write the SYBG for this same feature"

The user might work through multiple content types for the same feature in one session. That's the ideal workflow — keep context and stay consistent across surfaces.

---

## Flagging

Two situations require flagging:

**1. Guideline deviation.** When copy conflicts with these guidelines (wrong case, missing Oxford comma, "please" in an error, wrong terminology, etc.), correct it and explain the specific rule. No escalation needed for straightforward corrections.

**2. New patterns or genuine ambiguity.** When a content decision can't be resolved by these guidelines — a new component pattern, a tradeoff with no clear winner, a terminology question not in the A-Z, or a deviation the user insists on keeping — surface this message:

> 💬 **This might need a human eye.** This decision goes beyond what the content guidelines cover. Reach out to the Content Design team on **#content-design** in Slack — they can help confirm the right direction.
