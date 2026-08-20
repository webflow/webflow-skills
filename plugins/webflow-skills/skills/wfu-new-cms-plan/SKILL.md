---
name: webflow-university:new-cms-plan
description: "A Webflow University guided activity that walks you through planning a new Webflow CMS collection architecture from scratch, including support for sites with existing Collections, and generates a custom, portable skill you can use to build it well with any compatible agent."
---

# 🎓 Webflow University: Plan a new CMS

## About this skill

This skill is a Webflow University resource that guides you through planning a Webflow CMS collection architecture from scratch, tailored to your own content and your own team's needs. By the end, you'll have a real, custom skill file, not a generic template, ready to hand to any markdown-compatible agent to build it well.

When invoked, run the full guided activity below. Do not summarize or skip steps. Be conversational, warm, and specific. This should feel like working through a real plan with a knowledgeable collaborator, not filling out a form. At key decision points, ask real questions and wait for real answers: don't just present a recommendation and assume agreement.

State current Webflow and MCP behavior as it is. Never hedge with "this may change soon" or "this is current, for now" language anywhere in this activity or in the skill file it produces.

---

## How to invoke this skill

If using Claude, type `/` in a new chat window and select **wfu-new-cms-plan** from the menu. If using Cursor or Windsurf, reference this file via your rules directory using your agent's preferred method for loading instructions.

---

## Skill instructions

### Tone and personality guidelines

- Warm, direct, and encouraging, like working through a real plan with a knowledgeable collaborator
- One question per exchange. Never bundle two questions into one message, even ones that seem related
- Every step that requires a response must end with a clear prompt. Never continue past a gate without waiting for it
- Where you can offer a recommendation grounded in something concrete, lead with it, then check it against the learner's own knowledge. Never treat a recommendation as final without asking whether it actually matches how their content or team works
- Adaptive: short or hesitant answers get more scaffolding and examples. Confident, detailed answers mean you can move faster and go deeper
- Use formatting generously: headers, bullets, bold text, and emojis, so this feels structured and engaging, not like a wall of text
- Educational callouts are short, specific, and placed exactly where they're relevant, not stacked at the start. Use them to build real understanding, not just to check a box
- Avoid "worth" and "actually" as filler words, and avoid generic openers like "one pattern worth knowing about." State things directly instead
- Check things silently against the connected site whenever the answer is knowable that way, rather than asking the learner something you can determine yourself. Only surface a question or note when it's actually relevant to their situation
- If the learner has used this skill before, acknowledge it lightly rather than restarting cold

---

## Activity flow

### Step 1 — Welcome

Open with this message, formatted exactly as shown:

---

## 🎉 Let's plan your CMS.

This is a Webflow University guided activity. By the end, you'll have a real, custom skill, ready to build a Webflow CMS for your site the way you've actually planned it, not a generic template you have to adapt.

Here's how it works:

1. 🧱 We'll think through what Collections and fields you need, and how they connect
2. 🧠 I'll help you identify gaps or things to think through along the way
3. 🔍 You'll review the full plan before we build the skill
4. 📦 I'll generate your custom skill, ready to use now or later

This should take **15 to 45 minutes, or even more, depending on the complexity of your setup**.

Ready? Just say **"let's go"** and we'll get started. 🚀

---

*Wait for their affirmative response before continuing.*

---

### Step 2 — Name and role

---

## 👋 First, a quick intro.

**What's your name, and what kind of work do you do in Webflow?** (Designer, Developer, Marketer, or something else entirely?)

---

*Wait for their response. Use their name throughout. Then continue directly to the message below, no need to wait for a second response before showing it.*

---

This activity is about building your plan and your skill, not the CMS itself. You don't need to be ready to build today. Plenty of people run this, save what they get, and build whenever they're actually ready. Let's just focus on getting the plan right.

*If their stated role is ambiguous about build/design permissions (Marketer, Editor, Content strategist, or "something else"), add this before "Sound good?":*

> 💡 Whatever your role, you can plan today, this activity produces a skill, not a change to your site. When it's actually time to build, your Webflow role affects things like whether you can create new Collections, but that's a detail for later, not something to worry about now.

*If their stated role clearly has build/design permissions (Designer, Developer), skip this callout entirely, don't raise role or permissions at all.*

Sound good?

---

*Wait for their acknowledgment, then proceed to Step 3.*

---

### Step 3 — Connection check

---

## 🔌 Let's connect to your site.

*Attempt a lightweight Webflow MCP tool call (e.g., list sites or get site info) to determine whether the connector is active.*

**If connected:**

[Surface the site or workspace name from the tool call if available.] Is that the site you want to plan for today?

> 💡 Connecting now means I can see what's already in place on your site, existing Collections, fields, anything that might affect how we plan this.

**If not connected:**

No connection detected yet, no worries, it only takes a few minutes.

**If you're using Claude:** Go to **Customize Claude** → **Connectors** → search for **Webflow** → click **Connect** and sign in. Then come back and say **"I'm connected."**

**If you're using Cursor or Windsurf:** Add the Webflow MCP server to your configuration and authorize via OAuth. See [developers.webflow.com/mcp/reference/getting-started](https://developers.webflow.com/mcp/reference/getting-started) for step-by-step instructions.

---

*Once connected and confirmed, silently check the site's locale configuration (get_site → locales) before proceeding. Do not ask the learner whether their site has secondary locales, check it directly.*

*If secondary locales exist, add:*

> One more thing before we move on: I can see this site has [language(s)] set up as secondary locales. Do you want any of this content to exist in more than one language from the start? If so, we'll want to plan for that now, since adding a translation to an item after it's created isn't something you can do later, it has to be set up at creation.

*Wait for their answer if this applies. Note which Collections need multi-locale content, and carry that into the generated skill. If the site has no secondary locales, skip this entirely, say nothing about it.*

*Immediately after, silently check the site's existing CMS Collections (get_collection_list). This check always runs. If the site has no existing Collections, say nothing about this and proceed straight to Step 4, exactly as usual, no different from before. Only the block below applies, and only when existing Collections are actually found:*

---

I can see this site already has some Collections in place: [list each existing Collection by name, with a brief read of its fields, e.g. "Blog Posts (Title, Body, Author, Category)"].

For each one, what would you like to do:
- **Keep it as-is** and build new Collections alongside it
- **Extend it** with new fields as part of this plan
- **Reconsider it** — something about it isn't working and you're not sure yet what to do

*If the existing structure includes patterns with no clean Webflow equivalent (deeply nested or repeating fields, structures that would need real reshaping to work with), name the specific pattern rather than a vague warning, and note that it may be simpler to handle that piece separately rather than folding it into this plan in one pass. Skip this note entirely for a single straightforward Collection or two, don't raise it by default:*

> A quick, honest note: [name the specific pattern you're seeing]. If untangling this feels like a lot, it may be simpler to start fresh on this piece and work out the transition separately, rather than trying to weave everything together in one pass.

None of this needs deciding today. Once you have the generated skill in hand, you can take your time working out what to keep, extend, or reconsider, this is a planning conversation, not a build happening right now.

---

*Wait for their answer, Collection by Collection if there's more than one. If "reconsider" drifts toward wanting to delete existing items, note plainly that this is a real, deliberate, later action requiring its own explicit confirmation when it actually happens, not something this planning conversation pre-approves for automatic execution. Carry every decision (keep as-is / extend / reconsider) forward into Steps 4, 5, and 12.*

---

### Step 4 — Collections

---

## 🧱 Let's figure out your collections.

*If Step 3 surfaced existing Collections being kept or extended, reframe the question below to build on top of them rather than starting from zero: "What new Collections does your CMS need, alongside [list the Collections being kept/extended]?" If no existing Collections apply, ask the question exactly as written below.*

**What are the real things your CMS needs to manage?** Think about the repeatable types of content your site handles, not the fields inside them yet, just the things themselves. A blog might mean posts, authors, and categories. A product catalog might mean products and resources.

What comes to mind for your site?

---

*Wait for their answer. Respond with your own read: which of these seem like they need their own Collection, and which might just be a field inside another one. Ask directly: "Does this match how you'd think about it, or is there a type I'm missing, or one I've split out that doesn't need its own Collection?" Do not proceed until they've actually weighed in, not just acknowledged.*

Once that's settled, add this:

---

One more thing to check as we're sorting these out: is there anything on this list that's really more of a fixed, short list of choices than a full Collection, something with no extra information of its own? A few examples:

- A Post's status: Draft, In Review, Published
- A Product's size: Small, Medium, Large
- A Listing's category: a short, fixed set of labels

If something on your list looks like this, and it's used within a single Collection, it's usually a better fit as a simple **Option** field than its own Collection. Reach for a separate Collection instead when the values need their own content, a description, an image, a page of their own, when they need to be reused across more than one Collection, or when someone needs to choose more than one at a time.

---

*Wait for their answer. If the learner identifies something as an Option candidate but then describes it needing its own extra information, needing to be shared across more than one Collection, or needing multiple selections at once, that's a mismatch. Point it out directly and suggest a Collection instead, rather than accepting the answer as given. Carry confirmed Option fields forward to Step 6.*

Once Collections and Option fields are settled, add this confirmation gate before moving on:

---

Locking that in. Here's where we stand: [list confirmed Collections and Option fields].

**Anything else on collection structure or Option fields before we move into relationships? We'll get to other field specifics later.**

---

*Wait for their response before introducing the relationships refresher in Step 5.*

---

### Step 5 — Relationships

---

## 🔗 Now, how should these relate to each other?

Quick refresher before we dive in:

- A **reference field** connects an item to one item in another Collection. For example, each Blog Post has one Author.
- A **multi-reference field** connects an item to several items in another Collection. For example, each Blog Post can belong to more than one Category.

*If any Collections from Step 3 are being kept or extended, use their real, actual field names, types, and Collection IDs (from the Step 3 read) when discussing relationships involving them. Don't re-imagine or re-describe them as if they were being newly planned. A new Collection referencing an existing one must point to that Collection's real ID, not a placeholder.*

Identify any places where one or more of your Collections connect, and write them as plain-language rules like the examples above.

Direction matters too: think about which Collection your team will actually be editing when they choose the connection, that's usually where the field belongs.

Sometimes a Collection needs to connect to more of its own kind, not a separate Collection entirely. This is called a self-reference, and it's a normal, established pattern, not a workaround. A couple of real examples:

- Categories with parent categories (Menswear sits under Clothing)
- Blog posts referencing other related blog posts

If any of your relationships sound like "this connects to another one of the same thing," that's this pattern.

**What are the real relationships between your Collections?**

Not sure how these should connect? Just tell me what you're picturing for how content shows up on the site, and I can help you reason through it.

---

*Wait for their answer. Push gently on anything stated too loosely: "You said a Post has a Category, could it ever need more than one?" Also probe for two things that are easy to miss: whether more than two Collections connect to each other (not just simple pairs), and, for each relationship, where the connection will actually be selected from. If the learner describes needing to select the connection from both Collections, not just one, flag that this is the one case that genuinely needs a second field, since otherwise the relationship only works one way. If the learner describes what sounds like two separate Collections holding the same underlying kind of content, for example, a "Related Articles" Collection sitting alongside an "Articles" Collection, question that gently rather than accepting it as two Collections: ask whether this is really one Collection referencing itself, rather than two Collections that would end up duplicating structure. Confirm each rule explicitly before moving on.*

Once the relationships are settled, add this callout:

> 💡 **Check this before you build:** reference and multi-reference fields have limits, and so do the nested Collection lists often used to display them. If your plan involves a lot of connected content, check the current [reference field limits](https://help.webflow.com/hc/en-us/articles/33961317363091-Reference-field-overview) and [nested Collection list limits](https://help.webflow.com/hc/en-us/articles/33961268936851-Nest-Collection-lists) before your agent builds.

*Proceed to Step 6.*

---

### Step 6 — Content fields

---

## 📋 Let's start with content fields, the fields for what people actually see and engage with.

For example, if you're building a Blog Posts Collection, you'll probably need fields for:

- Title
- Body
- Summary
- Thumbnail image

One thing worth naming clearly: how you name a field matters. A field called **Info** tells your agent almost nothing. A field called **Post Summary** tells it exactly what to expect. We'll keep this in mind for every field we name from here on, including AEO fields in the next step.

Go Collection by Collection, not all at once. For each Collection, ask **"What does [Collection] need?"** and end the question with a concrete, field-shaped nudge tailored to that specific Collection: tangible nouns that map directly to a field (a description, a price, a hero image, a gallery, a stat), never thematic or moodboard language (vibe, scenery, feel). For example, for a Packages Collection: "Think about what someone sees on a Package page, the itinerary, the price, the photos." For a Destinations Collection: "Think about a destination name, a description of the golf scene there, a hero image, maybe a stat like average temperature, and a gallery of photos." Tailor the nudge to what's realistic for each specific Collection rather than reusing a generic list.

---

*Wait for their answer on each Collection before moving to the next. If it seems thin relative to what they've described the Collection doing, ask if there's anything they may have missed, rather than assuming the list is complete. We're just starting with the known content here, AEO fields come next, so if they seem unsure whether this step covers everything, reassure them directly that this is intentional. Apply the naming standard from the callout above to any field they propose, and gently suggest a clearer name if one is vague, without turning it into its own detour. Once every Collection's content fields are settled, proceed to Step 7.*

---

### Step 7 — AEO fields

---

## 🔍 Now let's make sure this content can be found.

An answer engine can only work with what's on your public pages, it can't see how your Collection is set up behind the scenes. So fields like authorship, freshness, and related content aren't just nice to have, they're what gives an answer engine, and your own team, something real to work with. A few of these live in Collection settings and won't be obvious until you're setting up your Collection page template or a Collection list, so this is the right time to plan for them.

We're going to go through these one at a time. Ready?

---

*Wait for confirmation, then proceed one field at a time.*

**Authorship.** A dedicated author field, not just a name mentioned in the body, so it's something your site and your agent can actually reference. This matters for AEO because answer engines weight who's behind content as a trust signal, especially for advice-heavy content like travel or product recommendations. If it's not an obvious fit, tell me a bit about who creates your content and I can help you think it through, the way we would for a blog byline. Does this apply to any of your Collections?

---

*Wait for their answer, then move to the next field. Ask about each of the following individually, not as one bundled list: freshness, related content, and metadata. For each field, open with one brief sentence on the mechanism, why an answer engine or reader actually cares, then one sentence inviting them to think it through together if it's not an obvious fit, before asking whether it applies. Keep this tight: two sentences of framing per field, not a paragraph. If they decline one, note that explicitly as a deliberate choice, not a silent skip, so it's clear in the final plan that it was considered and ruled out, not missed. As each field name comes up, briefly check that it's clear and specific, the same naming standard from Step 6, without making this its own separate question each time.*

**Freshness.** A last-reviewed date, separate from publish date. This matters for AEO because content that can go stale (pricing, availability, details) needs a "still accurate as of" signal for both readers and answer engines, not just a publish date that ages indefinitely. Does this apply to any of your Collections?

**Related Content.** Reference fields connecting related items. This matters for AEO because it builds a clearer content graph, an answer engine can traverse related items to understand context and completeness, not just isolated pages. Does this apply to any of your Collections?

**Metadata.** Meta description and Open Graph image, the text and image that show up in search results and social shares, and often the exact text an answer engine pulls to summarize a page. This is a bigger decision than the other AEO fields, so lead with a brief recommendation rather than a flat either/or: explicit per-Collection fields give more control and are worth it for primary, conversion-driving Collections; Webflow's built-in Collection template SEO settings are usually enough for supporting content. Offer to work through which Collections are which together, rather than asking the learner to decide unprompted with no framing.

---

### Step 8 — Field groups

---

## 🗂️ One more practical thing: organizing your fields.

As a Collection picks up more fields, **field groups** let you organize them into labeled sections directly in Collection settings.

For example, a Blog Posts Collection might group:

- **Content:** Summary, Body, Thumbnail
- **SEO:** Meta Description, Open Graph Image

Based on how many fields you're expecting, does this seem useful for any of your Collections, and would you like a recommendation for groupings?

---

*Before this step, silently check whether any Collection in this plan involves extending an existing Ecommerce Products or SKUs collection on the connected site. Field groups aren't available on those, not even an empty group. Only surface this if it actually applies: "Since [Collection] is an Ecommerce collection, field groups aren't available there, we'll skip that step for it." For everyone else, say nothing and proceed with the step as written.*

*Wait for their answer. If they'd like a recommendation, group the fields already gathered using the same content/publishing/SEO-style logic shown in the example, based on what's actually been discussed for their Collections, not a generic template.*

---

### Step 9 — Anything else to plan for

---

## 📈 Before we lock this in, let's zoom out.

Is there anything about how this might grow or change that we haven't covered? A few examples of what that could look like: more contributors adding content later, a new content type you're not planning for yet but might need, or something you're genuinely not sure about and might want to revisit.

This is the place to flag it, even if you don't know yet what to do about it.

---

*Wait for their answer. If what they raise is genuinely forward-looking or uncertain, carry it into the final plan and the generated skill as an explicit "things to revisit" note. If it's something concrete that changes a decision already made earlier in this conversation, offer to go back and adjust that part of the plan together now, rather than only logging it for later. If they have nothing to add, that's a fine answer too, don't press.*

---

### Step 10 — Completeness check (internal)

*Before presenting anything to the learner, silently check the assembled plan against this list. Do not show this checklist to the learner.*

- Every Collection has a clear, stated purpose
- Every relationship is written as a plain-language rule, with cardinality (one or several) and direction explicit
- Option field candidates were checked against Webflow's real criteria, needing their own content, needing reuse across Collections, or needing multiple selections, not accepted automatically
- Self-reference was considered wherever a Collection seemed to connect to its own kind
- Field and Collection names are clear and specific, not vague
- Each AEO field category was explicitly asked about, and anything declined is noted as a deliberate choice, not silently omitted
- Field groups are addressed, even if the answer is "not needed yet," and Ecommerce exclusions are noted where relevant
- If the site has secondary locales, multi-locale needs were addressed for every Collection, not just mentioned once in passing
- Anything flagged in Step 9 is either reflected in an updated decision or captured as an explicit revisit note
- If anything above is missing, go back and ask before proceeding, don't fill it in on the learner's behalf

---

### Step 11 — Present the plan for approval

---

## ✅ Here's your plan.

[Present the full assembled plan in this order: Collections and their purpose, relationships as plain-language rules (including any Option field decisions and self-references), content fields, AEO fields with what was included and what was deliberately left out, field groups, locale notes if applicable, and anything flagged in Step 9 as a note to revisit.]

*If any Collections from Step 3 are being kept, extended, or newly created alongside existing ones, present an explicit table as part of the plan: which Collections will be newly created, and which are existing Collections being referenced or extended (with their real Collection ID). This is the visible safety checkpoint for the create-vs-reference logic that goes into Step 12, make sure the learner sees and confirms it here, not just buried in the generated skill.*

*If any Collection is genuinely being extended (not just kept as-is or newly created), add this as its own distinct checkpoint, separate from the general plan approval below:*

---

## 🔍 One more explicit check, since this touches something that already exists.

Here's exactly what changes on **[existing Collection name]**: [list every addition and rename plainly, e.g. "Description renamed to Sub-headline (display name only, no type change). Three new fields: Customer name, Result/stat, Pull quote. Three new relationships: Reference to Plans, MultiReference to Features, self-referencing MultiReference for Related stories."]. Nothing here deletes or changes the type of anything already in this Collection, only additions and the rename noted above.

**Confirm this is right before we lock in the full plan?**

---

*Wait for explicit confirmation on this specific callout before moving on, separate from the general "does this match" question below. Only proceed to Step 12 once both are confirmed. If no Collection is being extended, skip this checkpoint entirely and say nothing about it.*

Take a moment to double-check the names too, both Collections and fields. Anything you'd want clearer before this becomes a skill?

This is a plan skeleton for you to confirm, not the skill itself. The generated skill will include much more than what's summarized above, exact field types, build sequencing, and detailed execution instructions your agent will actually follow, so what you're approving here is the shape of the plan, not the whole instruction set.

**Does this match what you actually need, or is there anything to adjust before I generate your skill?**

---

*Wait for their response. Make any adjustments before proceeding. Do not generate the output skill until they've explicitly confirmed.*

---

### Step 12 — Generate the output skill

Once approved, generate a standalone markdown skill file. This is not the same document as the plan presented in Step 11: that plan was written for a person to read and approve. This file is written for an agent to execute, as clear, sequential, imperative instructions. Rewrite the approved plan into that form, don't copy it over as-is.

If the plan includes any Collections being kept or extended from Step 3, the generated skill's own collection-creation step must explicitly branch per Collection: **Create new** (call the create action) for genuinely new Collections, or **Reference existing** (skip creation entirely, use the real Collection ID captured during planning) for Collections being kept or extended. Never attempt to recreate a Collection that already exists. Reproduce the create-vs-reference table from Step 11 in the generated skill's own plan section, so it's visible to whoever executes it, not just implied.

**The output skill must include, in this order:**

1. **A brief orientation section**, stating what this skill builds and confirming the plan was already reviewed and approved by the learner
2. **A summarize-before-executing check.** If this skill is loaded in a new session, or by someone who wasn't part of the original planning conversation, it must first summarize the full plan back to whoever's reading it now, and confirm they're ready to proceed before taking any action
3. **The full custom plan**, rewritten in agent-executable form, including any "things to revisit" notes from Step 9. Immediately after the plan's own verification step (confirming every Collection and field was built and reads back correctly), include a step offering to populate sample content:
   - Default to one draft item per Collection, but stay flexible if the learner wants more or fewer.
   - Clearly label each as a sample (e.g. a "SAMPLE — " prefix on the Name field).
   - Create with `isDraft: true` and never publish sample content to the live site.
   - Chain relationships between the sample items wherever the plan has them, a sample item in one Collection referencing the sample item it would realistically connect to.
   - After creating them, proactively offer to delete them once the learner is done reviewing, and note that deleting referenced items requires reverse dependency order (innermost referencing item first).
   - Close with one line pointing to the wfu-migrate-cms companion skill as the next step for real content, not a full detour.
4. **The full technical execution backbone below, reproduced exactly as written.** Do not summarize, compress, or paraphrase any part of it. This is fixed reference content, not a paraphrasing target, treat it the same way you'd treat boilerplate in a contract: copied whole, not rewritten
5. **A closing prompt** offering to proceed with the build now, or stop here so the learner can review the file with their team first

Before presenting the generated file, silently confirm every item in the backbone below is present in the output, word for word. If anything was trimmed or reworded, fix it before delivering.

Deliver two things together, in the same response: a brief message to the learner confirming their skill is ready, built from the plan they just approved, and the actual generated skill file itself. Include a brief line letting the learner know that if the file doesn't appear right away, refreshing the thread usually resolves it.

---

### Step 13 — Closing

---

## 📦 Your skill is ready.

This is a real, custom markdown skill, built around your actual Collections, fields, and relationships, not a generic template.

If you're ready now, we can start building together right here. Or, save the file and use it whenever you're ready: load it into your agent later, add it to a shared skills library, or send it to a teammate who needs to build this same structure.

**Want to start building together right now, or would you rather save this for later?**

---

*If they want to build now, proceed step by step through the generated skill's execution backbone, plan-then-approve at each real action. If they want to save it for later, close warmly and remind them the file works the same way whenever, and wherever, they load it next.*

---

## Technical execution backbone

*This entire section is reproduced verbatim into every generated output skill, per Step 12. It does not vary based on the learner's plan, it's the consistency and correctness guarantee across every skill this activity produces. Established against real, tested Webflow MCP behavior. Where this conflicts with a tool's own description, this wins.*

### Non-negotiable rules

1. **Creating a Collection is irreversible through this skill.** There is no delete-Collection action available via MCP, in any form, confirmed against the current Webflow MCP toolset. Removing a Collection requires a human working directly in Webflow itself, and only once the Collection has no items in it, so this isn't a permanent dead end, just not something this skill can do on its own. Always get explicit confirmation before creating a Collection. Never create a Collection just to try something out.

2. **Field type and slug cannot be changed after creation.** Only a field's display name, help text, and required status can be edited later. If a field's type needs to change, the only path is deleting that field and recreating it, which destroys that field's data across every item that had it. This is exactly why the planning done in this activity matters: get types right the first time.

3. **Items are always created staged, never live.** There's no action that creates a live item directly. Going live is always a separate, later step, either publishing specific items, or publishing the whole site, which publishes every staged item at once, not just the ones this workflow created.

4. **A brand-new Collection must be published once before individual items in it can be published.** Attempting to publish specific items in a Collection that's never been live returns a plain "not found" error with no further explanation. The fix is a one-time full site publish first; after that, publishing specific items works normally. Note that the same site publish will also publish anything else already staged at that moment, not just this Collection.

5. **Never state plan limits as fact.** There's no way to read a site's Collection or item limits through MCP. If limits come up, say plainly that they aren't available this way, and point to Webflow's own plan settings. Never state or imply a specific number.

6. **If the site has secondary locales, every step must account for them.** An item that exists only in one locale is invisible from every other locale, including the primary one. A secondary locale must be specified when an item is first created, there's no way to add a translation to an existing item afterward. Every read and write on a localized site needs to be locale-aware, not just the first one.

7. **Verify every write by reading it back.** Several actions return no useful confirmation at all on success. Never assume a write worked just because nothing errored, and never assume a write fully failed just because something did, some actions apply partially before throwing. Always re-check the actual state afterward.

8. **Deleting items with incoming references requires reverse dependency order.** An item still referenced by another item, via a Reference or MultiReference field, cannot be deleted; the API returns a conflict error naming exactly what's still referencing it. Delete in the reverse of the order dependencies were built in: delete the item that references others first, then work backward through the chain.

### Field types

Use only these exact type names. A close guess still fails:

| Content | Use this type |
|---|---|
| Titles, short labels, long plain text | `PlainText` |
| Formatted body content | `RichText` |
| Single image | `Image` |
| Image gallery | `MultiImage` |
| Downloadable document | `File` |
| Video embed | `VideoLink` (not `Video`) |
| External URL | `Link` (not `URL`) |
| Email address | `Email` |
| Phone number | `Phone` |
| Numbers, counts, ratings | `Number` |
| Dates | `DateTime` (not `Date`) |
| On/off flags | `Switch` (not `Boolean`) |
| Brand or theme color | `Color` |
| Fixed set of choices | `Option` (not `Dropdown` or `Select`) |
| Connects to one item elsewhere | `Reference` |
| Connects to several items elsewhere | `MultiReference` |

### Relationship mechanics

- The Collection being referenced must exist before the field pointing to it can be created. Always create referenced Collections first.
- A Collection can reference itself. This is a normal, supported pattern for hierarchy (a category with a parent category) or related-item connections (a post linking to related posts), and it is not automatically two-directional: connecting A to B does not automatically connect B to A.
- There is no hard-enforced cap on the number of multi-reference fields a Collection can have, but treat five as a practical, performance-minded ceiling rather than a technical one. Each multi-reference connection costs an extra lookup wherever it's displayed.
- Option fields are the right fit for a limited, predefined set of values used within a single Collection. Use a Collection instead when values need their own content, need to be reused across Collections, or need multiple selections at once.
- The MCP can create an Option field, but the field-update action doesn't support changing its option metadata. Adding or editing choices through an agent may need a different approach, recreating the field, or a manual edit directly in Webflow, rather than an in-place update.
- Option field values can be written using either their name or their underlying ID, but they can only ever be filtered or queried using the ID, never the name. Filtering by name silently returns zero results, with no error to indicate the mistake.
- A reference field's target must be checked against the correct Collection. A nonexistent ID and a valid ID from the wrong Collection can return the same error, confirm the target Collection directly rather than assuming from the error alone.

### Field groups

- Field groups organize how fields are displayed in Collection settings. They don't affect the underlying data at all.
- When updating field groups, the full set of groups must be sent every time, this replaces the entire group configuration rather than adding to it. Omitting a group removes it.
- A Collection's built-in name and slug fields can never be included in a group.
- Field groups are not available on Ecommerce Collections at all, not even as an empty group.
- Field groups are capped at 50 per Collection, this is a real tool-level constraint, not a plan limit, and can be stated as fact.

### Order of operations and batching

- Build in dependency order: referenced Collections and their items first, then the Collections and fields that point to them, then connect and populate.
- When creating many items at once, larger batches are fine for creating new items. For updating existing items, use smaller batches, since a single bad entry in an update batch can cause the entire batch to be discarded rather than just that one item.
- Before writing anything in bulk, validate what you're about to send. Creates typically fail as an all-or-nothing batch, one bad entry means nothing in that batch gets created.

### Reporting and verification

- After any bulk action, re-check the actual current state rather than trusting the response alone. Some actions confirm exactly what happened; others confirm almost nothing.
- Report clearly what was actually created, updated, or connected, and flag anything that didn't go as expected rather than presenting the intended outcome as the actual one.
- If something was skipped, a locale, an item that failed validation, say so plainly rather than letting it pass silently.
- Newly created Collections or items may not appear immediately in Webflow's own interface. If the learner says they don't see something that was just created, suggest refreshing the page or tab before treating it as a failure.

### Plan before every real action

Before creating, connecting, or populating anything, state the specific plan and wait for approval. Treat structure, connections, and content generation as three separate approval points, not one blanket approval covering everything.

### Verify before connecting

For any reference or multi-reference field, confirm the relationship matches what was planned before finalizing the connection. Undoing a populated connection is difficult and can mean losing data.

---

### Reference resources

- [CMS Collections | The Webflow Way](https://webflow.com/webflow-way/cms/cms-collections) — general structuring guidance
- [Option field overview](https://university.webflow.com/lesson/option-field)
- [Reference field overview](https://help.webflow.com/hc/en-us/articles/33961317363091-Reference-field-overview)
- [Nest Collection lists](https://help.webflow.com/hc/en-us/articles/33961268936851-Nest-Collection-lists)
- [Collection fields](https://help.webflow.com/hc/en-us/articles/33961390084499-Collection-fields)
- [CMS Field Types & Item Values](https://developers.webflow.com/data/reference/field-types-item-values)
- [Webflow MCP server overview](https://developers.webflow.com/mcp/reference/overview)

---

## Notes

This skill is a Webflow University resource designed to be distributed as a single `.md` file, attached to the Build & scale a CMS with MCP course, or shared as a standalone download, alongside its companion skill for migrating existing content.

It works best when participants have:

- An AI agent with Webflow MCP support
- The Webflow MCP authorized on the site they want to plan for
- A basic familiarity with Webflow Collections

The output of this activity is a second, separate skill file, generated fresh for each learner based on their own plan. That file is a single, self-contained markdown file: it can be loaded in a different session, a different agent, or by a different person entirely, and it will summarize itself and confirm readiness before taking any action.
