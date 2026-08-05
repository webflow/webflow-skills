# Content Patterns by Type

## Table of Contents
1. In-Product UI Copy
2. SYBG Modal Content
3. webflow.com/updates Posts
4. Help Documentation / University Articles

---

## 1. In-Product UI Copy

### General Principles
- Conversational: use contractions, simplest/shortest word, "you" to address the user, ~6th grade reading level
- Concise but clear: short + confusing helps no one, so go longer if it's useful
- Accessible: explain complex features in plain language the first time they appear
- Universal: avoid idioms and hard-to-translate phrases
- Sentence case everywhere
- Active voice (passive only to avoid blaming the user)

### By Component

#### Buttons and CTAs
- 1-2 words preferred
- Use imperative verbs: "Save," "Remove," "Create" — not "Okay" or "Submit"
- Sentence case
- Include an option to dismiss or cancel so users can opt out

#### Tooltips
- Focus on the most important info the user needs to achieve their goal
- Be clear about the job to be done (JTBD)
- Full sentences get periods
- Don't shy away from industry jargon — but explain it in plain language

#### Error Messages
Structure: What happened → Why → What to do next

**Title:**
- Sentence case, ~3-4 words
- Communicate the result of the error
- Be informative and scannable
- Don't explain what to do (save that for body)
- Don't ask questions
- Example: "That page doesn't exist" not "Invalid"

**Body:**
- 1-2 sentences
- Don't repeat the title
- Include: reason for error + what to do next + consequences of inaction
- Use "Learn more" link for anything over 2 sentences
- Example: "The template you chose has been removed — return to Marketplace to choose a new one."

**Tone guidance:**
- Avoid "please" — can undermine authority and make required steps seem optional
- Avoid "sorry" — can make errors feel more severe than they are (only apologize for severe, irreparable consequences)
- Use "we" instead of "you" to avoid blaming: "We lost the connection" not "Something's wrong with your connection"
- When multiple solutions exist: simplest solution first, alternative in second sentence

#### Empty States
- Focus on user benefit and encourage progress toward a goal
- Make it clear exactly what action fills the empty state
- Give an indication of what data/content will eventually appear there

#### Dialogs/Modals
- Headline: single clear question or single concise message
- Primary button: unambiguous action that indicates what happens on click
- Body: clarify consequences and explain options in simple terms

#### Onboarding (First-Use)
- Show users how to experience value ASAP
- Focus on user benefits, not features or technical details
- Match selling points from marketing
- Convey only essential info needed to inspire action
- Answer the user's most pressing questions and remove doubt
- Explain why before asking for permissions or data access

#### Notifications and Alerts
- Front-load: most important words first (in case of truncation)
- Start with user benefit, not work required
- Match tone to user context
- Prioritize user needs over sales/marketing/product team needs

#### Dashboards
- Clear visual emphasis on important stats and recommended actions
- Logically grouped and labeled data
- Tooltips or links to help articles for complex terms
- Clear which actions are mandatory, recommended, or optional

#### Forms
- Group similar fields into sections
- Clear, consistent labels in plain language
- Field labels and helper text serve separate purposes (no redundancy)
- Helper text prevents errors with examples or formatting instructions
- Tooltips for fields where users need reassurance

#### Transactional Emails
- Subject line: ~40 characters, required action/urgency clear
- Front-load: most important idea or action obvious from heading
- Body: short, scannable, useful subheadings
- CTA easy to find, near top
- Tone: respectful, positive, solution-oriented
- Tell users how to get more info or contact support

---

## 2. SYBG Modal Content

The SYBG ("Since You've Been Gone") modal appears on the Webflow Dashboard when users log in. It highlights new features and updates they may have missed. Content is managed through Knock Guides.

### Fields to Write

| Field | What to Write | Guidelines |
|-------|--------------|------------|
| **Full Title** | The release/feature name | Sentence case. Clear, scannable. Should make sense as a standalone headline. |
| **Condensed Title** | Same as Full Title | Keep identical to Full Title for consistency. |
| **Image Alt Text** | Short description of the image | For accessibility. Describe what's shown, not what it means. |
| **Content** | Description of the release | 2-3 sentences. What it is, why it matters to the user, what they can do with it. Empowering and user-centered. |
| **Primary Button Text** | Usually "Learn more" | Keep as "Learn more" unless there's a more specific action. |
| **Primary Button URL** | Link to /updates page | Use full URL with https://www. |

### Writing Tips for SYBG
- Lead with the user benefit, not the feature name
- Be specific about what changed — vague announcements don't build trust
- Match the celebratory but grounded tone: exciting, not hype-y
- Keep the Content field tight — users are scanning, not reading deeply
- The modal shows multiple features in a list, so each entry competes for attention. Make yours count in 2-3 sentences.

### Example Structure for Content Field
"[What it does in one sentence — focused on user benefit]. [How it works or what's new, briefly]. [Where to find it or what to do next — optional]."

---

## 3. webflow.com/updates Posts

These are public-facing release announcements. They should be polished, on-brand, and serve both existing users (who want to know what changed) and prospective users (who are evaluating Webflow).

### Recommended Structure

**Title**
- Feature or update name, sentence case
- Clear and descriptive — searchable and scannable

**Hero Visual**
- Screenshot, GIF, or illustration showing the feature in action

**Intro Paragraph (2-3 sentences)**
- What this update is and why it matters
- Lead with user benefit
- Set context for who this helps

**What's New Section**
- Walk through the key changes or capabilities
- Use short paragraphs (2-3 sentences each)
- Use headings to break up sections if there are multiple sub-features
- Include visuals (screenshots or GIFs) to show, not just tell

**How to Use It**
- Brief instructions or pointers to get started
- Use breadcrumbs for navigation: "Open Project settings > Hosting > 301 redirects"
- Link to relevant University articles for deeper guidance

**CTA**
- Clear next step: "Try it now," "Learn more in Webflow University," etc.
- Link to the relevant product surface or help article

### Tone for /updates
- Celebratory but grounded — the Bold dimension dialed up slightly
- Empowering: center what the user can now do, not what Webflow built
- Specific: "You can now set breakpoints on individual elements" not "We've improved the design experience"
- Professional but warm — these posts represent Webflow to the world

### Length
- Aim for 300-600 words depending on complexity
- Simple feature: shorter, punchier
- Major release: longer, more detailed, possibly with sub-sections

---

## 4. Help Documentation / University Articles

### General Principles
- Write as if speaking with someone, not at them
- Imagine the reader sitting next to you as you walk them through the Webflow interface
- Users are likely intimidated — write with empathy and patience
- Use the shortest, most common words
- Read your writing aloud — if it doesn't sound natural, change it

### Article Structure

**Title**
- Guides (general feature descriptions): use the feature name — "Sliders" not "Learn about sliders"
- Tutorials (walkthroughs): [Verb] + [result] + [feature/tech] — "Build a pricing grid with Flexbox"
- Never include "how to" or "Webflow" in titles
- Never phrase as questions
- Never use first person

**Body structure:**
1. Clear title
2. Companion video embed (if exists)
3. Brief subtitle/explanation
4. Intro text (sometimes not necessary)
5. Numbered outline of the lesson (acts as table of contents)
6. Lesson body with H2s matching the outline

### Writing Rules
- **Sentence case** everywhere
- **Breadcrumbs** for navigation steps: "Open Project settings > Hosting > 301 redirects"
- **Descriptive headings** that help skim/scan
- **Short sections** — break up dense paragraphs
- **Short sentences** — one idea per sentence
- **Present tense** — more direct and easier to understand
- **Contractions** where natural
- **Active voice** — "Update your SEO setting in the Pages panel"
- **Address readers directly** with "you"
- **Numerals** — "Enter two 3s" / "Add 3 rows"
- **Bold** UI elements, menu names, tab names, command names
- **Lists** to simplify complex material
- **Callouts** for important info: Note: / Good to know: (blue) / Important: (orange)
- **Links** embedded in descriptive text, never "click here" or "learn more" alone
- External links open in new tab

### Visuals
- Use to clarify complex UI descriptions
- Skip if instructions are standard and text suffices
- Screenshots for static UI callouts
- GIFs sparingly for multi-step sequences
- Always include alt text
