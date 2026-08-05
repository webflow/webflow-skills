# Component Writing Guidance

Detailed content rules for each UI component, mapped to the Spring design system. Each section includes the component's **Spring anatomy** (the structural slots where content lives) and the **content rules** for writing within those slots.

When reviewing a Figma prototype, identify the Spring component name (e.g., `Toast`, `Note`, `EmptyState`) and use the anatomy below to understand which slots need copy and what constraints apply.

## Table of contents
- [Accordion](#accordion) | [Buttons](#buttons) | [Badges](#badges) | [Banner](#banner)
- [Empty state & Loading state](#empty-state--loading-state) | [Error messages](#error-messages)
- [Form labels](#form-labels) | [Links](#links) | [List boxes](#list-boxes) | [Menus](#menus)
- [Modal (Dialog)](#modal-dialog) | [Note](#note) | [Notifications](#notifications)
- [Onboarding Popover](#onboarding-popover) | [Popover](#popover)
- [Radio card](#radio-card) | [Switch box](#switch-box) | [Tabs](#tabs) | [Tables](#tables)
- [Tag](#tag) | [Toast](#toast) | [Tooltip](#tooltip) | [Upsell banner](#upsell-banner)

---

## Accordion

### Spring anatomy
Spring name: `Accordion`, `AccordionHeader`
Density variants: `compact`, `comfortable`
States: open, closed, focus, suffix icon button

| Slot | Location | Type |
|------|----------|------|
| **Label text** | AccordionHeader → "Icon + Text" → heading text | Semibold, primary color |
| **Prefix icon** | AccordionHeader → leading icon (optional) | 16px icon |
| **Suffix** | AccordionHeader → trailing area | Chevron indicator or icon button |
| **Content items** | Accordion body → RowItem(s) | Regular text per row item |

### Content rules
- Keep labels as concise as possible. Long labels may truncate.
- Use the label to clearly describe what the user will find when expanded.
- Build a connection between label and description — but avoid repetition. The description should feel like an *expansion* of the label.

**Example:**
- ✅ Label: "Custom domains" → Description explains how to configure them
- ❌ Label: "About custom domains" → Description: "Custom domains allow you to…" (repetitive)

---

## Buttons

### Spring anatomy
Spring name: `Button`
Density variants: `compact`, `comfortable`
Hierarchy: primary, secondary, tertiary
States: default, hover, active, focus, disabled, loading

| Slot | Location | Type |
|------|----------|------|
| **Label text** | Button → center text | Regular weight, centered |
| **Prefix icon** | Button → leading icon (optional) | 16px icon, before label |
| **Suffix icon** | Button → trailing icon (optional) | 16px icon, after label |

### Content rules
- **3 words maximum.**
- No articles ("a", "the") — they waste space.
- Describe exactly what happens on click. Avoid generic text.
- Never describe 2 actions with "&" — that signals the workflow needs a separate step.
- Use **"show"** instead of "view" for accessibility. Use **"go to"** if the user is navigating to a different area.
- Use **"create"** for generating net-new resources. Use **"add"** for adding existing resources.
- **Primary buttons** → creative or destructive actions (add, create, delete).
- **Secondary buttons** → regressive or supportive actions (learn more, go back, cancel).
- **"Got it"** is acceptable for strict acknowledgement. Use it instead of "ok."

**Examples:**
- ✅ "Create site" / "Delete Workspace" / "Add member"
- ❌ "Create a new site" / "Click here to delete" / "Add & invite member"

---

## Badges

### Spring anatomy
Spring name: `Badge`
Variants: color-based (e.g., default, info, success)

| Slot | Location | Type |
|------|----------|------|
| **Label text** | Badge → text content | Short, attention-grabbing |

### Content rules
- **1 word ideal, 2 words max.** Best for concise attention-grabbing (e.g., "New").
- Never use an "alpha" tag — alpha products are mostly internal.
- "Beta" tags are fine for products visible to external users.

**Examples:**
- ✅ "New" / "Beta"
- ❌ "New feature" / "Alpha release" / "Coming soon to all users"

---

## Banner

### Spring anatomy
Spring name: `Banner`
Color variants: `default`, `primary` (blue), `success` (green), `warning` (yellow), `danger` (red)
States: default, with title, with icon, with control, with status indicator, wrapping (multiline)

| Slot | Location | Type |
|------|----------|------|
| **Label text** | Banner → primary text area | Regular weight, primary color. The main message. |
| **Title** | Banner → title area (optional) | Semibold, appears above or inline with label |
| **Prefix icon** | Banner → leading icon (optional) | Status/context icon |
| **Control** | Banner → trailing area (optional) | Button or action, follows Button guidelines |
| **Status indicator** | Banner → leading indicator (optional) | Visual signal paired with color variant |

### Content rules
- Use for urgent, critical messages or messages requiring user action.
- **2 concise sentences max.**
- Must communicate both the **problem** and the **solution**.
- Buttons on banners follow standard Button guidelines.

**How to distinguish from Note:** Banners are full-width, persistent bars typically anchored to the top of a page or section. Notes are inline, contained blocks that sit within content flow. If it stretches edge-to-edge and demands attention, it's a Banner. If it's an inline callout, it's a Note.

**Examples:**
- ✅ "Your site plan expires tomorrow. Update your billing to avoid interruption."
- ❌ "Hey! Just wanted to let you know something might be wrong. You should probably check it out when you get a chance."

---

## Empty state & Loading state

### Spring anatomy
Spring name: `EmptyState`
Boolean variants: `isDisabled`, `isDropTarget`
States: text only, with link, with button, drop target, disabled

| Slot | Location | Type |
|------|----------|------|
| **Illustration** | EmptyState → "Icon" area (64px) | Decorative illustration, not a content slot |
| **Heading text** | EmptyState → "content" → heading | Semibold, primary color. The key message. |
| **Description text** | EmptyState → "content" → body | Regular weight, secondary color. Supporting detail. |
| **CTA** | EmptyState → "controls" → Button (optional) | Follows Button guidelines |

### Content rules

**Empty states** (feature previously used, no data):
- Orient users to an interface with no populated data.
- Don't point out the obvious ("There's nothing here").
- Direct users to take actions that will populate the state.
- Don't need to be as guided as start states — assume the user has experience.

**Loading states:**
- Explain exactly what's happening on the backend to build trust.
- Ellipses can connote an action currently happening (e.g., "Loading your sites …").

**Start states** (first-time use):
- More guided and helpful than empty states.
- Avoid pointing out the obvious, but offer more guidance than a traditional empty state.

**Examples:**
- ✅ Empty: "Create a Collection to start organizing your content."
- ❌ Empty: "You don't have any Collections yet."
- ✅ Loading: "Setting up your Workspace …"
- ❌ Loading: "Loading…" (too vague)

---

## Error messages

### Spring anatomy
Error messages can appear in multiple Spring components: `Banner` (danger variant), `Toast` (danger variant), `Note` (danger variant), or inline validation text near form fields. Identify the component first, then apply both the error content rules and that component's structural constraints.

### Content rules
- State the **problem + resolution** as concisely as possible.
- Tell users what to do — **not what they did wrong.**
- **Never use "please."** Write the message as a productive action.
- Always strive to provide a resolution or helpful next step.
- If no resolution exists, "Refresh and try again" or similar is acceptable.

**Examples:**
- ✅ "Enter a valid email address to continue."
- ❌ "Please enter a valid email. You entered an invalid email address."
- ✅ "Something went wrong. Refresh and try again."
- ❌ "Error 500: An unexpected server error occurred. Please contact support."

---

## Form labels

### Spring anatomy
Spring name: `FormLabel`, `FormField`, `Input`
Related components: `FormHelperText`, placeholder text

| Slot | Location | Type |
|------|----------|------|
| **Label** | FormLabel → text above field | Persistent, visible when user types |
| **Placeholder** | Input → ghost text inside field | Disappears on focus/input |
| **Helper text** | FormHelperText → below field (optional) | Additional clarification |

### Content rules
- **2 words max.** Describe exactly what the user needs to input.
- Label must remain visible above the field when the user starts typing.
- Placeholders can provide examples but should never replace the label or convey important info.
- Helper text goes below the field — one concise sentence for further clarification.

**Examples:**
- ✅ "Email address" (with placeholder: "name@company.com")
- ❌ "Enter your billing email address" (too long for a label — move detail to helper text)

---

## Links

### Spring anatomy
Spring name: `Link`
Color/style variants: default, primary, danger, and more
States: default, hover, focus, disabled

| Slot | Location | Type |
|------|----------|------|
| **Label text** | Link → text content | Single text string, typically underlined or colored |

### Content rules
- Use as secondary, text-based CTAs embedded in or after sentences.
- Describe where the user is going as clearly as possible.
- Links must make sense **out of context** for screen readers. Avoid generic "Learn more."
  - If "Learn more" is necessary for space, engineering should add a descriptive `aria-label`.
- Keep links as a brief, standalone sentence at the end of body text. Avoid mixing hyperlinks into sentences (localization concern).
- **No period** at the end of standalone links.
- Ideally only 1 hyperlink per piece of content. Multiple links are rare exceptions.
- **Diagonal arrows** (↗) only when the link opens a new tab. Never use horizontal arrows in links.

**Examples:**
- ✅ "Learn more about bandwidth"
- ❌ "Click here" / "Learn more" (without aria-label)

---

## List boxes

### Spring anatomy
Spring name: `ListBox`, `ListBoxItem`

| Slot | Location | Type |
|------|----------|------|
| **Item label** | ListBoxItem → primary text | Main selectable text |
| **Item description** | ListBoxItem → secondary text (optional) | Supporting detail below label |

### Content rules
- Items should be concise. Ideally they don't truncate — they wrap instead.
- All items should be the **same part of speech** (all nouns OR all verbs).
- Descriptions should be additive to the main item, not repetitive.

---

## Menus

### Spring anatomy
Spring name: `Menu`, `MenuItem`
Related: `MenuSection`, `MenuDivider`

| Slot | Location | Type |
|------|----------|------|
| **Item label** | MenuItem → primary text | Main clickable text |
| **Item description** | MenuItem → secondary text (optional) | Supporting context |
| **Prefix icon** | MenuItem → leading icon (optional) | Context icon |
| **Suffix** | MenuItem → trailing area (optional) | Keyboard shortcut, badge, or arrow |

### Content rules
- Space-constrained — be as concise as possible.
- Users should know exactly what happens or where they'll go on click.
- Unlike lists, menu items do **not** all need the same part of speech.
- **With description:** Main item 1–2 words (1 line), description within 2 lines.
- **Without description:** Up to 2 lines.

---

## Modal (Dialog)

### Spring anatomy
Spring name: `Dialog` (called "Dialog" in Spring, "Modal" in content guidelines)
Related components: `ModalMask` (backdrop overlay)
Private sub-components: `modal-title`, `modal-header`, `modal-body`, `modal-footer`
Variants: default/action panel, multi-path context, with/without footer, with close button + icon

| Slot | Location | Type |
|------|----------|------|
| **Title** | modal-header → title text | Semibold. The headline. |
| **Icon** | modal-header → leading icon (optional) | Contextual icon before title |
| **Close button** | modal-header → trailing X (optional) | IconButton with CloseDefault icon |
| **Body content** | modal-body → freeform content area | Regular text. The main message area. |
| **Footer link** | modal-footer → leading text/link (optional) | Secondary action as text |
| **Secondary button** | modal-footer → secondary action (optional) | e.g., "Cancel", "Discard" |
| **Primary button** | modal-footer → primary action | e.g., "Delete", "Confirm", "Save" |

### Content rules

**Heading:**
- Confirmation modals: Heading can be a question.
- Non-confirmation modals: Use declarative statements.
- Avoid generic language like "Are you sure?" — personalize to the action.
- No period at the end.

**Body:**
- Don't frame both heading and body as questions.
- Confirmation body: Focus on consequences/implications of the action.
- **3 lines max.** More text may indicate a design problem — a modal might not be the right component.

**Buttons:**
- Follow standard Button guidelines.
- Pay extra attention to clarity — every action should be unique and clearly differentiated.
- Avoid having both "Back" and "Cancel" next to each other.

**Examples:**
- ✅ Heading: "Delete this site?" / Body: "This will permanently remove the site and all its content. This can't be undone."
- ❌ Heading: "Are you sure?" / Body: "Are you sure you want to delete this? It can't be undone."

---

## Note

### Spring anatomy
Spring name: `Note`
Boolean variants: `isInline`, `isTinted`, `isGhost`, `isSeamless`
Color variants: `primary`, `default`, `success`, `danger`, `warning`, `urgent`
States: default, has close button, has control (in-line), is tinted, is ghost, is seamless, multi line, has button, has secondary button, has link, has icon

| Slot | Location | Type |
|------|----------|------|
| **Icon** | Note → leading icon (optional) | Contextual/status icon, 16px |
| **Headline text** | Note → heading area | Semibold, primary color |
| **Body text** | Note → description area | Regular weight, secondary color |
| **Close button** | Note → trailing IconButton (optional) | Dismiss action |
| **In-line control** | Note → trailing control (optional) | Button or link |
| **Button** | Note → below body text (optional) | Primary or secondary action |
| **Link** | Note → below body text (optional) | Text link CTA |

### Content rules
- **Headline** is the most important text. Clear, summarizes the key issue, suggests a possible action.
  - For Enterprise handraisers: frame with the main user benefit.
  - May include question marks or exclamation points. No periods unless multiple sentences.
- **Body text:** 2 lines max.
- **Max 2 CTAs** (including inline hyperlinks). Too many CTAs confuse users.

**How to distinguish from Banner:** Notes are inline, contained blocks within content flow. Banners are full-width persistent bars. If it sits within a section as a callout, it's a Note. If it stretches across the top demanding attention, it's a Banner.

**How to distinguish from Toast:** Notes are persistent and positioned inline. Toasts are transient (they auto-dismiss) and float above the UI. If the message stays, it's a Note. If it appears briefly and disappears, it's a Toast.

**Spring-specific note:** `isSeamless` should only be used with `isGhost`. Secondary buttons are currently only supported for multiline notes. Links don't work as well with colored (tinted) backgrounds.

---

## Notifications

Notifications have specialized content guidelines depending on placement. Consult the Figma file for the specific notification type you're working with.

---

## Onboarding Popover

### Spring anatomy
Spring name: `OnboardingPopover`
Position variants: top, bottom, left, right (with arrow pointing to target element)

| Slot | Location | Type |
|------|----------|------|
| **Title** | OnboardingPopover → heading area | Semibold/bold. The feature or concept name. |
| **Body text** | OnboardingPopover → description area | Regular weight. Explains the feature. |
| **Image/media** | OnboardingPopover → media area (optional) | Screenshot, illustration, or video |
| **CTA** | OnboardingPopover → action area | Link or button (e.g., "Get started", "Next", "Got it") |
| **Close button** | OnboardingPopover → trailing X | IconButton to dismiss |
| **Progress indicator** | OnboardingPopover → footer area (optional) | e.g., "3 of 4" for multi-step flows |

### Content rules
- Follow a logical progression — especially for multi-step onboarding flows.
- Be as concise as possible (space-constrained).
- If the popover contains rich elements (links, videos), ensure all accessibility needs (alt text, etc.) are addressed.
- Progress indicators help users understand where they are in a flow — always include them for multi-step sequences.

**How to distinguish from Popover:** Onboarding Popovers are specifically for onboarding/education flows — they have a distinct visual style (typically blue/branded background), progress indicators, and are part of a guided sequence. Regular Popovers are for drilling into UI details on demand.

---

## Popover

### Spring anatomy
Spring name: `Popover`
Complex component with many sub-component configurations
Position variants: top, bottom, left, right

| Slot | Location | Type |
|------|----------|------|
| **Title** | Popover → header area (optional) | Context for the popover content |
| **Body content** | Popover → main content area | Flexible: text, lists, controls, inputs |
| **Footer actions** | Popover → footer area (optional) | Buttons or links |

### Content rules
- Usually appears as a longer flow of content that helps users drill down into finer details of a UI.
- Should always follow a logical progression.
- Be as concise as possible (space-constrained).
- If the popover contains rich elements (links, videos), ensure all accessibility needs (alt text, etc.) are addressed.

---

## Radio card

### Spring anatomy
Spring name: `RadioCard`

| Slot | Location | Type |
|------|----------|------|
| **Headline** | RadioCard → heading area | Semibold. The choice name. |
| **Body text** | RadioCard → description area (optional) | Regular weight. Expands the choice. |
| **Icon/illustration** | RadioCard → media area (optional) | Visual representation of the choice |

### Content rules
- Present mutually exclusive choices as clearly and distinctly as possible.
- **Headlines:** Encapsulate the choice in as few words as possible. Use parallel structure (all nouns or all verbs).
- **Body copy:** Expand nuance behind a choice. 2 sentences max.
- If choices can't be written in parallel, concise way — consider whether a radio card is the right component.

---

## Switch box

### Spring anatomy
Spring name: `SwitchBox`, `Switch`

| Slot | Location | Type |
|------|----------|------|
| **Label** | SwitchBox → text next to toggle | Describes what is being toggled |
| **Description** | SwitchBox → secondary text (optional) | Additional context |

### Content rules
- Binary input: turns a setting on or off.
- Label should reflect the binary nature: "on/off," "enable/disable," "turn on/turn off."
- Surrounding content should explain what's being toggled — the switch label is too space-constrained for explanations.
- Write content in the affirmative for clarity.

---

## Tabs

### Spring anatomy
Spring name: `Tabs`, `Tab`

| Slot | Location | Type |
|------|----------|------|
| **Tab label** | Tab → text content | Short text identifying the tab's content |
| **Tab icon** | Tab → leading icon (optional) | Contextual icon before label |

### Content rules
- **1 word ideal, 2 words max.**
- Label should set expectations about what appears in the tabbed area.
- Tabs should be thematically similar to each other.
- Ideally the **same part of speech** across all tabs (all nouns, all verbs, etc.).

**Examples:**
- ✅ "Style" / "Settings" / "Interactions"
- ❌ "Style settings" / "Settings" / "Interactions" (inconsistent structure)

---

## Tables

### Spring anatomy
Spring name: `Table`, `TableRow`, `TableCell`, `TableHeader`

| Slot | Location | Type |
|------|----------|------|
| **Column header** | TableHeader → text | Labels the column |
| **Row header** | First cell in row (optional) | Labels the row |
| **Cell content** | TableCell → freeform | Data or text |

### Content rules
- Column and row labels: **2 words max.**
- Labels should always **wrap, never truncate.** Truncation inhibits usability.
- Labels must be declarative statements — no questions, no exclamation points.

---

## Tag

### Spring anatomy
Spring name: `Tag`
Can be interactive (clickable as button or link) or static

| Slot | Location | Type |
|------|----------|------|
| **Label text** | Tag → text content | Metadata label |
| **Prefix icon** | Tag → leading icon (optional) | Contextual icon |
| **Dismiss button** | Tag → trailing X (optional) | Removes the tag |

### Content rules
- Metadata elements — concise and descriptive.
- **1 word ideal, 2 words max.**
- Tags can be clickable (as button or link). When clickable, also follow Button/Link guidelines.
- **Tag vs. Badge:**
  - Badge = highlights new or altered features. Not selectable or interactive (can have tooltip).
  - Tag = labels, categorizes, or organizes items with keywords. Can be dismissible.

---

## Toast

### Spring anatomy
Spring name: `Toast`
Boolean variants: `isInline` (floating vs. embedded)
Color variants: `default`, `primary` (blue), `success` (green), `danger` (red), `warning` (yellow)
States: default, without icon, multiline, with control

| Slot | Location | Type |
|------|----------|------|
| **Icon** | Toast → leading icon (optional, toggle: `hasIcon`) | Status/context icon, 16px |
| **Title** | Toast → heading text (optional, toggle: `hasTitle`) | Semibold, primary color |
| **Body text** | Toast → description text (always present) | Regular weight, secondary color |
| **CTA Button** | Toast → action button (optional, toggle: `hasControl`) | Follows Button guidelines |
| **Close button** | Toast → trailing IconButton | CloseDefault icon to dismiss |

### Content rules
- Transient messages — **conciseness is key.** Never so long they truncate.
- Can contain 1 optional CTA for a logical next step.
- Can be styled with or without a heading.
- **Drop unnecessary fluff.** Classic example: "successfully" is redundant when paired with strong verbiage and a green background.

**How to distinguish from Note:** Toasts are transient — they float above the UI and auto-dismiss. Notes are persistent inline blocks. If it disappears on its own, it's a Toast.

**How to distinguish from Banner:** Toasts float in a corner or edge of the viewport. Banners are anchored full-width bars. If it's a floating notification, it's a Toast.

**Examples:**
- ✅ "Site published" / "Changes saved"
- ❌ "Your site has been successfully published!" / "Your changes have been saved successfully."

---

## Tooltip

### Spring anatomy
Spring name: `Tooltip`
Position variants: top, bottom, left, right (with arrow pointing to trigger element)

| Slot | Location | Type |
|------|----------|------|
| **Title** | Tooltip → heading text (optional) | Bold/semibold. Short label. |
| **Description** | Tooltip → body text | Regular weight. The main helper text. |
| **Slot content** | Tooltip → custom content area (optional) | Can contain breadcrumbs or other structured content |

### Content rules
- Ancillary, helpful information about a UI element.
- **~2 lines recommended.** Can be longer if necessary, but keep it tight.
- Assume tooltip content may never be read — or only by attentive power users. Use that to decide what belongs in the tooltip vs. core UI.
- **No interactive elements** (links, buttons) per WCAG 2.0.
- Overly lengthy tooltips often signal the core UI isn't self-explanatory. If you observe this, scrutinize the design.

---

## Upsell banner

### Spring anatomy
Upsell banners are visually designed versions of `Note` components. They follow the same Spring anatomy as Note but with brand-specific styling.

### Content rules
- Follow all content guidelines under **Note** — upsell banners are more specific, visually designed versions of notes.

---

## Component identification guide

When looking at a Figma prototype, use these distinguishing characteristics to identify the right component:

| If you see... | It's likely a... |
|---------------|-----------------|
| Full-width bar anchored to top of page/section | **Banner** |
| Inline callout box within content flow | **Note** |
| Floating notification that auto-dismisses | **Toast** |
| Overlay dialog with backdrop mask | **Modal (Dialog)** |
| Small text bubble on hover near a UI element | **Tooltip** |
| Branded blue card with progress indicator (e.g., "2 of 4") | **Onboarding Popover** |
| Dropdown-style panel for drilling into details | **Popover** |
| Centered illustration + heading + CTA in an empty area | **Empty state** |
| Mutually exclusive cards arranged side-by-side | **Radio card** |
| Toggle with a label | **Switch box** |
| Horizontal row of short labels switching content below | **Tabs** |
| Short colored pill/chip on or near a UI element | **Badge** (if static) or **Tag** (if interactive/dismissible) |
