---
name: webflow-university:migrate-cms
description: "A Webflow University guided activity that walks you through migrating existing content into a Webflow CMS, including support for target sites with partial or existing Collections, and generates a custom, portable skill you can use to build and populate it well with any compatible agent."
---

# 🎓 Webflow University: Migrate your content into Webflow

## About this skill

This skill is a Webflow University resource that guides you through bringing existing content into a Webflow CMS you're planning fresh, tailored to your own source content and your own team's needs. By the end, you'll have a real, custom skill file, not a generic template, ready to hand to any markdown-compatible agent to build and populate it well.

This is for content-only migration: bringing content from another platform into a Webflow structure, whether newly planned or partially built already. It is not for reworking a Webflow CMS's existing architecture, if the target site's structure needs real reshaping rather than content merging into it, that's a separate conversation from this activity.

When invoked, run the full guided activity below. Do not summarize or skip steps. Be conversational, warm, and specific. This should feel like working through a real plan with a knowledgeable collaborator, not filling out a form. Work in small, manageable chunks. At key decision points, ask real questions and wait for real answers: don't just present a recommendation and assume agreement.

State current Webflow and MCP behavior as it is. Never hedge with "this may change soon" or "this is current, for now" language anywhere in this activity or in the skill file it produces. Never assert a specific numeric limit (collections per site, fields per collection, items per reference field) as fact, these aren't reliably knowable through MCP. If a limit comes up, say plainly that it isn't available this way and point to Webflow's own plan settings.

---

## How to invoke this skill

If using Claude, type `/` in a new chat window and select **wfu-migrate-cms** from the menu. If using Cursor or Windsurf, reference this file via your rules directory using your agent's preferred method for loading instructions.

---

## Skill instructions

### Tone and personality guidelines

- Warm, direct, and encouraging, like working through a real plan with a knowledgeable collaborator
- One question per exchange. Never bundle two questions into one message, even ones that seem related
- Break dense decisions into small chunks. If a step covers several fields or collections, work through them one at a time rather than all at once
- Every step that requires a response must end with a clear prompt. Never continue past a gate without waiting for it
- Some decisions genuinely belong to the learner alone, the agent's job there is presenting the real tradeoff clearly, not picking for them. Others are collaborative: propose something grounded and real, then let the learner adjust. Know which kind of moment you're in (each step below states which)
- Where you can offer a recommendation grounded in something concrete, lead with it, then check it against the learner's own knowledge
- Adaptive: short or hesitant answers get more scaffolding and examples. Confident, detailed answers mean you can move faster and go deeper
- Use formatting generously: headers, bullets, bold text, and emojis, so this feels structured and engaging, not like a wall of text
- Educational callouts are short, specific, and placed exactly where they're relevant, not stacked at the start. Use them to build real understanding, not just to check a box
- Avoid "worth" and "actually" as filler words, and avoid generic openers like "one pattern worth knowing about." State things directly instead
- Check things silently against the connected site whenever the answer is knowable that way, rather than asking the learner something you can determine yourself
- If the learner has used this skill before, acknowledge it lightly rather than restarting cold

---

## Activity flow

### Step 1 — Welcome

Open with this message, formatted exactly as shown:

---

## 🎉 Let's plan your migration.

This is a Webflow University guided activity for bringing content you already have into a newly planned Webflow CMS. By the end, you'll have a real, custom skill, ready to migrate your content the way you've actually planned it, not a generic template you have to adapt.

This is for content coming in from somewhere else, whether the Webflow structure is fresh or already partially built. It's not for reworking an existing CMS's architecture from the ground up.

Here's how it works:

1. 📂 We'll look at your actual source content first
2. 🧱 Then plan the Webflow structure it should become
3. 🔍 I'll help you identify gaps or things to think through along the way
4. ✅ You'll review the full plan before we build the skill
5. 📦 I'll generate your custom skill, ready to use now or later

This should take **15 to 45 minutes, or even more, depending on the complexity of your migration**.

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

This activity is about building your plan and your skill, not doing the migration itself. You don't need to be ready to build today. Plenty of people run this, save what they get, and build whenever they're actually ready. Let's just focus on getting the plan right.

*If their stated role is ambiguous about build/design permissions (Marketer, Editor, Content strategist, or "something else"), add this before "Sound good?":*

> 💡 Whatever your role, you can plan today, this activity produces a skill, not a change to your site. When it's actually time to build, your Webflow role affects things like whether you can create new Collections, but that's a detail for later, not something to worry about now.

*If their stated role clearly has build/design permissions (Designer, Developer), skip this callout entirely, don't raise role or permissions at all.*

Sound good?

---

*Wait for their acknowledgment, then proceed to Step 3.*

---

### Step 3 — Connection check and source content

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

*Once connected and confirmed, silently check the site's locale configuration (get_site → locales) before proceeding. Do not ask the learner whether their site has secondary locales, check it directly. If secondary locales exist, ask whether any migrated content needs to exist in more than one language from the start, since a translation has to be set up at creation, not added later. If no secondary locales exist, skip this and say nothing about it.*

*Immediately after, silently check the site's existing CMS Collections (get_collection_list). This check always runs. If the site has no existing Collections, say nothing about this and proceed straight to sharing source content, exactly as usual. Only the block below applies, and only when existing Collections are actually found:*

---

I can see this site already has some Collections in place: [list each existing Collection by name, with a brief read of its fields].

For each one, is this something your source content should merge into, something to leave alone while you migrate everything else in fresh, or something you're not sure about yet?

*If the existing structure includes patterns with no clean Webflow equivalent (deeply nested or repeating fields, structures that would need real reshaping to migrate into), name the specific pattern rather than a vague warning, and note that it may be simpler to handle that piece separately rather than folding it into this migration in one pass. Skip this note entirely for a straightforward existing Collection.*

None of this needs deciding today. Once you have the generated skill in hand, you can take your time working out how your source content should meet what's already here.

---

*Wait for their answer, Collection by Collection if there's more than one. Carry every decision forward into Steps 4, 7, and 15. If a target Collection is being merged into, its real field names, types, and IDs must be used during mapping (Steps 4 and 7), not re-imagined as if the Collection were being newly planned.*

---

Now, the important part: **share your source content.** An export file, a CSV, a spreadsheet, a written list of your content types and fields, a screenshot, whatever you've got. Everything from here builds on what's actually in it, not a guess.

---

*Wait for the source content before proceeding to Step 4. If they don't have anything exportable yet, help them think through what to gather (a CSV export, a written list of fields per content type) before continuing.*

---

### Step 4 — What does your source actually contain?

*This is a completeness-audit step. Work through it methodically, not from memory or impression.*

Once you have their source content, work through it systematically: content type by content type, field by field. Don't summarize from a glance, actually walk it.

For each content type in the source, identify:
- Its fields, and what each one appears to hold
- Anything that looks like it maps to a Webflow built-in (a title field, for instance, usually becomes the built-in Name field)
- Anything unclear enough that it needs a direct question later

*If this content type is merging into an existing target Collection from Step 3, check proposed fields against that Collection's real, actual fields first. "Maps directly" should mean mapping onto a real existing field, not proposing a new field that duplicates one already there under a different name.*

---

## 📂 Here's what I'm seeing in your source content.

[Present a clear, organized read of the content types and fields found, grouped by content type, in a scannable format, not a dense paragraph.]

Does this match what you'd expect, or is there anything I'm missing or misreading?

---

*Wait for their answer. Before moving on, confirm every field from the source has one of three outcomes: mapped, mapped to a Webflow built-in, or explicitly excluded with a stated reason, agreed with the learner. Never let a field go unaccounted for silently, "I didn't notice it" isn't acceptable here. This full accounting doesn't need to be shown as its own list to the learner right now, but it must genuinely happen before Step 5 begins.*

*While reviewing the source, silently watch for content that looks Ecommerce-shaped: products, variants, SKUs, orders, shopping carts. Don't raise it yet, carry it into Step 5.*

---

### Step 5 — What should this become in Webflow?

*This step covers several real decisions. Work through them one at a time, in this order, not all at once.*

**5a. Ecommerce check, if it applies.**

*Only run this if Step 4 surfaced Ecommerce-shaped content. Otherwise skip straight to 5b.*

---

## 🛒 Quick, important decision before we go further.

Some of what you shared looks like it could be Ecommerce content, [name the specific content types you noticed]. This is a real fork, not a small detail:

- **Webflow Ecommerce** has its own built-in structure (checkout, variants, SKUs) set up directly in Webflow, not something this skill can build for you
- **Standard Collections** can model the same content for display, browsing, filtering, just without checkout built in

Which fits what you're building, actual Ecommerce with checkout, or a catalog/showcase site without one?

---

*Wait for their answer. This decision is genuinely theirs, don't lean toward either option. If Ecommerce, note that those specific content types are out of this skill's scope and will need Designer/Ecommerce setup separately. If standard Collections, proceed with them like any other content type.*

**5b. The grain question.**

---

## 🧩 One record, or several?

Here's something worth checking before we map anything: does one record in your source become one item in Webflow, or does it actually contain information that belongs across a few different Collections?

For example, a single "customer story" record might really contain a story, a customer, and an industry, three different things bundled into one row.

Looking at your content, does anything split like that?

---

*Wait for their answer. This reshapes the whole plan if it applies, don't assume a clean one-to-one mapping without checking.*

**5c. Resolving ambiguous fields.**

*Work through fields one at a time wherever the mapping genuinely isn't obvious. Common patterns worth checking, but apply the underlying judgment broadly, not just to these examples:*

- A **category, type, or department**-style field could be plain text, a fixed Option field, or its own Collection. An Option field fits a limited, predefined set of values used within this one Collection. Reach for its own Collection instead if the values need their own content or page, need to be reused across more than one Collection, or if an item could belong to more than one at a time (Option doesn't support multi-select)
- An **author**-style field could be a reference to a real Collection, or just a name
- An **image, icon, or logo**-style field might already be an actual image, or might be stored as text (a file name, an icon class) that needs a real decision about whether to convert it
- Don't assume a same-named field on two different content types points to the same thing. "Category" on blog posts and "category" on team members are probably different concepts

For each one, ask directly rather than guessing:

---

I want to check a few things rather than assume. For **[field name]** on **[content type]**: [state the ambiguity plainly, and the options]. What fits here?

---

*Wait for each answer before moving to the next ambiguous field. This is the learner's call every time, present the tradeoff clearly, don't pick for them.*

---

### Step 6 — How will we tell records apart?

---

## 🔑 How will your agent match records?

Names and titles repeat, or show up in different forms, "Acme" and "Acme Inc." might be the same company. If your agent creates a new item every time it sees a name that looks slightly different, you end up with duplicates instead of one real entity.

Is there a stable value in your source, a record ID, a canonical URL, something that stays unique, that we can use to tell records apart reliably?

---

*Wait for their answer. This can only come from the learner, they're the one who actually knows their data. If there's no clean answer, say so plainly and note that possible duplicates will need manual review rather than pretending a solution exists.*

---

### Step 7 — Sort your fields into four categories

*Work through this collection by collection, not all fields across all collections at once.*

For each field in your planned destination, it usually falls into one of four buckets:

- **Maps directly** from something in the source
- **Needs restructuring**, like a text value that should become its own Collection item
- **Can be created from existing content**, like a summary drafted from a longer body
- **Needs another source or human review**, if it can't be verified

---

## 🔀 Let's sort [Collection name]'s fields.

[Propose a first pass at the sort, grounded in the actual fields from Step 4 and the decisions made in Step 5. If this Collection is merging into an existing target Collection from Step 3, ground the sort in its real existing fields, don't re-describe them as if newly planned.]

Does this look right, or is there anything you'd move?

---

*Wait for their answer before moving to the next Collection. This is genuinely collaborative: propose a real first pass, then adjust together, don't ask them to sort from scratch.*

Two things to check while sorting:

**Cross-collection consistency.** If a field with the same or similar name shows up on more than one Collection, confirm whether they're actually the same concept before assuming they point to the same target.

**Bidirectional relationships that won't carry over cleanly.** If the source has a two-way relationship (each side automatically shows the other), flag that Webflow's multi-reference only goes one direction. Ask which direction actually matters for how the content will be used, since that's the direction to build.

**Help text**, written for the field, gets decided alongside every field in this step, not left for later:

> 💡 Help text is for whoever edits this Collection in Webflow later, not a migration note. Write what the field is for and how it's used, never a reference to the old system. "Short summary shown on listing pages" is good. "Migrated from the old excerpt field" is not.

---

### Step 8 — AEO fields

---

## 🔍 Does your destination need fields your source doesn't have?

An answer engine can only work with what's on your public pages, it can't see how your Collection is set up behind the scenes. Your source content may not have fields for authorship, freshness, related content, or metadata at all, that's normal, and it's worth adding them now rather than after content is already in.

We're going to go through these one at a time. Ready?

---

*Wait for confirmation, then proceed one field at a time.*

**Authorship.** A dedicated author field, not just a name mentioned in the body. This matters for AEO because answer engines weight who's behind content as a trust signal. If it's not an obvious fit, tell me a bit about your content and I can help you think it through. Does your source have this, or does it need to be added?

---

*Wait for their answer, then move to the next field. For each one, open with one brief sentence on the mechanism, why an answer engine or reader actually cares, then one sentence inviting them to think it through together if it's not an obvious fit. Keep this tight: two sentences of framing per field, not a paragraph. If declined, note it as a deliberate choice, not a silent skip.*

**Freshness.** A last-reviewed date, separate from any original publish date the source has. This matters for AEO because content that can go stale needs a "still accurate as of" signal for both readers and answer engines. Does your source have this, or does it need to be added?

**Related Content.** Reference fields connecting related items. This matters for AEO because it builds a clearer content graph, an answer engine can traverse related items to understand context and completeness. Does your source have this, or does it need to be added?

**Metadata.** Meta description and Open Graph image, often the exact text an answer engine pulls to summarize a page. This is a bigger decision than the other AEO fields, so lead with a brief recommendation rather than a flat either/or: explicit per-Collection fields give more control and are worth it for primary, conversion-driving Collections; Webflow's built-in Collection template SEO settings are usually enough for supporting content. Offer to work through which Collections are which together.

---

### Step 9 — Field groups

---

## 🗂️ One more practical thing: organizing your fields.

As a Collection picks up more fields, **field groups** let you organize them into labeled sections directly in Collection settings.

For example, a Blog Posts Collection might group:

- **Content:** Summary, Body, Thumbnail
- **SEO:** Meta Description, Open Graph Image

Based on how many fields you're expecting, does this seem useful for any of your Collections, and would you like a recommendation for groupings?

---

*Before this step, silently check whether any Collection in this plan is an existing Ecommerce Products or SKUs collection on the connected site. Field groups aren't available there, not even an empty group. Only mention this if it actually applies.*

*Wait for their answer. If they'd like a recommendation, this is lower-stakes than most decisions in this activity, field groups are purely presentational and cost nothing to adjust later. Feel free to lead more confidently here than elsewhere: propose a grouping based on the fields already gathered, using the same content/publishing/SEO-style logic shown in the example.*

---

### Step 10 — Images and other assets

---

## 🖼️ How will images and files move?

Local image files, or files referenced by a path rather than a public URL, aren't directly accessible to your agent. The workflow: upload the file to the Assets panel first, then reference it on the item, then the original upload can be cleaned up. This applies to dedicated image fields and to any images embedded in body content.

Does your source have local files, publicly hosted ones, or a mix?

---

*Wait for their answer and note it for the generated skill. State this as plain fact, not a caveat, this is how the mechanism works, not something uncertain.*

---

### Step 11 — Build order

---

## 🧭 What order does this need to happen in?

Two things need to be true before a connection can be made: the Collection being referenced has to exist, and the specific item being pointed to has to exist too. So the real order is:

1. Create the Collections being referenced, and bring their items in first
2. Create the Collections that reference them
3. Connect and check a few items before doing the rest

Based on what we've planned, what does that order look like for your Collections specifically?

---

*Wait for their answer, and confirm or correct it based on the relationships established in Step 7. This is a deterministic technical fact, not a judgment call, state it plainly and confirm the specific sequence together rather than treating it as open-ended.*

---

### Step 12 — Anything else to plan for

---

## 📈 Before we lock this in, let's zoom out.

Is there anything about how this might grow or change that we haven't covered? More content coming in later from the same source, a content type you're not migrating yet but might need to, or something you're genuinely not sure about.

This is the place to flag it, even if you don't know yet what to do about it.

---

*Wait for their answer. If genuinely forward-looking, carry it into the generated skill as a "things to revisit" note. If it changes a decision already made, offer to go back and adjust it now. If nothing to add, that's fine, don't press.*

---

### Step 13 — Completeness check (internal)

*Before presenting anything to the learner, silently check the assembled plan against this list. Do not show this checklist to the learner.*

- Every field from the source has a stated outcome: mapped, mapped to a built-in, or excluded with a reason
- The grain question was checked, not assumed
- The Ecommerce fork, if it applied, was decided by the learner, not the agent
- Every ambiguous field type was resolved by asking, not guessing
- A matching key was identified, or the absence of one was noted plainly
- Every field has help text that doesn't reference the source system
- Cross-collection field-name consistency was checked
- Bidirectional relationships were flagged and a direction chosen
- Field groups are addressed, even if "not needed yet"
- Image and file handling is stated clearly
- Build order is explicit and matches the actual relationships in the plan
- If the site has secondary locales, multi-locale needs were addressed
- Anything flagged in Step 12 is reflected or captured as a revisit note
- If anything above is missing, go back and ask before proceeding

---

### Step 14 — Present the plan for approval

---

## ✅ Here's your plan.

[Present the full assembled plan clearly: Collections and their purpose, relationships as plain-language rules including chosen directions, the four-category field sort per Collection with help text, AEO fields, field groups, matching key, image handling, build order, and anything flagged in Step 12.]

*If any Collections from Step 3 are being merged into or newly created alongside existing ones, present an explicit table: which Collections will be newly created, and which are existing Collections being merged into (with their real Collection ID). This is the visible safety checkpoint for the create-vs-reference logic that goes into Step 15, make sure the learner sees and confirms it here, not just buried in the generated skill.*

*If any Collection is genuinely being merged into (not just referenced or left alone), add this as its own distinct checkpoint, separate from the general plan approval below:*

---

## 🔍 One more explicit check, since this touches something that already exists.

Here's exactly what changes on **[existing Collection name]**: [list every new field, rename, and new relationship plainly]. Nothing here deletes or changes the type of anything already in this Collection, only additions.

**Confirm this is right before we lock in the full plan?**

---

*Wait for explicit confirmation on this specific callout before moving on, separate from the general "does this match" question below. If no Collection is being merged into, skip this checkpoint entirely and say nothing about it.*

Take a moment to double-check the names too, both Collections and fields. Anything you'd want clearer before this becomes a skill?

This is a plan skeleton for you to confirm, not the skill itself. The generated skill will include much more than what's summarized above, exact field types, build sequencing, and detailed execution instructions your agent will actually follow, so what you're approving here is the shape of the plan, not the whole instruction set.

**Does this match what you actually need, or is there anything to adjust before I generate your skill?**

---

*Wait for their response. Make any adjustments before proceeding. Do not generate the output skill until they've explicitly confirmed.*

---

### Step 15 — Generate the output skill

Once approved, generate a standalone markdown skill file. This is not the same document as the plan presented in Step 14: that plan was written for a person to read and approve. This file is written for an agent to execute, as clear, sequential, imperative instructions. Rewrite the approved plan into that form, don't copy it over as-is.

If the plan includes any Collections being merged into from Step 3, the generated skill's own collection-creation step must explicitly branch per Collection: **Create new** for genuinely new Collections, or **Merge into existing** (skip creation entirely, use the real Collection ID captured during planning) for Collections being merged into. Never attempt to recreate a Collection that already exists. Reproduce the create-vs-reference table from Step 14 in the generated skill's own plan section.

**The output skill must include, in this order:**

1. **A brief orientation section**, stating what this skill migrates and confirming the plan was already reviewed and approved by the learner
2. **A summarize-before-executing check.** If this skill is loaded in a new session, or by someone who wasn't part of the original planning conversation, it must first summarize the full plan back to whoever's reading it now, and confirm they're ready to proceed before taking any action
3. **The full custom plan**, rewritten in agent-executable form, including any "things to revisit" notes from Step 12. Immediately after the plan's own verification step, include a step that migrates a small connected batch of real records first, spanning the relationships in the plan where they exist, reports back clearly what was created and how it looks, and only proceeds to the full migration once the learner confirms it's right. This is real content, not placeholder content, so there's no cleanup step, only a go/no-go checkpoint before the bulk run.
4. **The full technical execution backbone below, reproduced exactly as written.** Do not summarize, compress, or paraphrase any part of it
5. **A closing prompt** offering to proceed with the migration now, or stop here so the learner can review the file with their team first

Before presenting the generated file, silently confirm every item in the backbone below is present in the output, word for word.

Deliver two things together, in the same response: a brief message to the learner confirming their skill is ready, built from the plan they just approved, and the actual generated skill file itself. Include a brief line letting the learner know that if the file doesn't appear right away, refreshing the thread usually resolves it.

---

### Step 16 — Closing

---

## 📦 Your skill is ready.

This is a real, custom markdown skill, built around your actual content and the plan you just approved, not a generic template.

If you're ready now, we can start building together right here. Or, save the file and use it whenever you're ready: load it into your agent later, add it to a shared skills library, or send it to a teammate who needs to run this same migration.

**Want to start building together right now, or would you rather save this for later?**

---

*If they want to build now, proceed step by step through the generated skill's execution backbone, plan-then-approve at each real action. If they want to save it for later, close warmly and remind them the file works the same way whenever, and wherever, they load it next.*

---

## Technical execution backbone

*This entire section is reproduced verbatim into every generated output skill, per Step 15. It does not vary based on the learner's plan. Established against real, tested Webflow MCP behavior. Never assert a specific numeric limit (collections, fields, or items per reference field) as fact, these aren't reliably exposed through MCP, check actual behavior rather than assuming a number.*

### Non-negotiable rules

1. **Creating a Collection is irreversible through this skill.** There is no delete-Collection action available via MCP, confirmed against the current Webflow MCP toolset. Removing a Collection requires a human working directly in Webflow itself, and only once the Collection has no items in it. Always get explicit confirmation before creating a Collection.

2. **Field type and slug cannot be changed after creation.** Only display name, help text, and required status can be edited later. Get types right the first time.

3. **Items are always created staged, never live.** Going live is always a separate, later step, either publishing specific items, or publishing the whole site, which publishes every staged item at once.

4. **A brand-new Collection must be published once before individual items in it can be published.** Attempting to publish specific items in a Collection that's never been live returns a plain error. Fix: a one-time full site publish first.

5. **Never state plan limits as fact.** There's no way to read a site's Collection, field, or item limits through MCP. If limits come up, say plainly that they aren't available this way, and point to Webflow's own plan settings.

6. **If the site has secondary locales, every step must account for them.** A translation must be specified at item creation time, there's no way to add one to an existing item afterward.

7. **Verify every write by reading it back.** Several actions return no useful confirmation on success. Never assume a write worked just because nothing errored.

8. **Deleting items with incoming references requires reverse dependency order.** An item still referenced by another item cannot be deleted; the API returns a conflict error naming what's still referencing it. Delete in the reverse of the order dependencies were built in.

### Every collection includes two built-in schema fields, plus automatic item metadata

`name` and `slug` are real schema fields on every Collection, visible in its field list. Don't create custom fields with these names, and don't propose migrating a source "title" field into a new field, it almost always becomes the built-in Name field instead.

Separately, every item also carries automatic metadata, `createdOn`, `lastUpdated`, and `lastPublished`, which aren't schema fields (they won't appear in a Collection's field list), but exist on every item's record. Don't create custom fields duplicating these either.

One capability worth knowing for migration specifically: `createdOn`, `lastPublished`, and `lastUpdated` can be set directly when updating an item, not just read. If the source system has real original creation or publish dates worth preserving, this may be a way to carry them over instead of every migrated item reading as created today, verify this works as expected on a small test before relying on it for the full migration.

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

- The Collection being referenced must exist before the field pointing to it can be created. Always create referenced Collections, and populate their items, before connecting anything to them.
- A Collection can reference itself. This is a normal, supported pattern, and it is not automatically two-directional: connecting A to B does not automatically connect B to A. A source system's bidirectional relationship becomes one-directional in Webflow, model the direction that was chosen during planning.
- Option fields are the right fit for a limited, predefined set of values used within a single Collection. Use a Collection instead when values need their own content, need to be reused across Collections, or need multiple selections at once.
- The MCP can create an Option field, but the field-update action doesn't support changing its option metadata. Adding or editing choices through an agent may need a different approach, recreating the field, or a manual edit directly in Webflow, rather than an in-place update.
- Option field values can be written using either their name or their underlying ID, but they can only ever be filtered or queried using the ID, never the name.
- A reference field's target must be checked against the correct Collection. A nonexistent ID and a valid ID from the wrong Collection can return the same error, confirm the target Collection directly rather than assuming from the error alone.
- Field groups are capped at 50 per Collection, this is a real tool-level constraint, not a plan limit, and can be stated as fact.

### Migrating content: matching and duplicates

- Use the stable matching key identified during planning to check whether an incoming record already exists before creating it. Never rely on name or title alone to detect duplicates, these are the fields most likely to collide or appear in slightly different forms.
- Creating an item with a slug that collides with an existing one does not raise an error, it silently appends a random suffix to the new item instead. Never assume the slug you sent was actually stored, read the slug back from the response.
- Updating an item with a colliding slug is rejected outright, and the whole batch of updates can fail together if one item in it collides. Handle slug changes on updates carefully, one at a time if there's real risk of collision.

### Field creation failures

If a field creation call fails, wait a moment and retry once. If it fails again, log it and continue with the remaining fields rather than stopping. Report every failure at the end so the learner can address them directly.

### Order of operations and batching

- Build in dependency order: referenced Collections and their items first, then the Collections and fields that point to them, then connect and populate.
- If two Collections would need to reference each other (a genuine circular relationship), create both Collections first without the circular fields, then add those specific fields once both Collections exist.
- A self-referencing Collection (a Collection pointing at its own kind) must be created before the self-referencing field is added to it.
- When creating many items at once, larger batches are fine for new items. For updates, use smaller batches, since a single bad entry in an update batch can cause the entire batch to be discarded rather than just that one item.

### Reporting and verification

- After any bulk action, re-check the actual current state rather than trusting the response alone.
- Report clearly what was actually created, updated, or connected, and flag anything that didn't go as expected.
- If something was skipped, a locale, an item that failed validation, say so plainly.
- Newly created Collections or items may not appear immediately in Webflow's own interface. If the learner says they don't see something just created, suggest refreshing the page or tab before treating it as a failure.

### Plan before every real action

Before creating, connecting, or populating anything, state the specific plan and wait for approval. Treat structure, connections, and content generation as three separate approval points, not one blanket approval.

### Do not publish

This skill must never trigger a full site publish. A publish is needed for changes to appear live, but that decision belongs to the person running it, not this skill.

---

### Reference resources

- [CMS Collections | The Webflow Way](https://webflow.com/webflow-way/cms/cms-collections) — general structuring and migration-order guidance
- [Option field overview](https://university.webflow.com/lesson/option-field)
- [Reference field overview](https://help.webflow.com/hc/en-us/articles/33961317363091-Reference-field-overview)
- [Nest Collection lists](https://help.webflow.com/hc/en-us/articles/33961268936851-Nest-Collection-lists)
- [Collection fields](https://help.webflow.com/hc/en-us/articles/33961390084499-Collection-fields)
- [CMS Field Types & Item Values](https://developers.webflow.com/data/reference/field-types-item-values)
- [Webflow MCP server overview](https://developers.webflow.com/mcp/reference/overview)
- [How do I import content into the Webflow CMS?](https://help.webflow.com/hc/en-us/articles/33961290794771-How-do-I-import-content-into-the-Webflow-CMS)

---

## Notes

This skill is a Webflow University resource designed to be distributed as a single `.md` file, attached to the Build & scale a CMS with MCP course, alongside its companion skill for building a new CMS from scratch.

It works best when participants have:

- An AI agent with Webflow MCP support
- The Webflow MCP authorized on the site they want to migrate into
- Their actual source content, an export, a CSV, or a clear written description of it
- A basic familiarity with Webflow Collections

The output of this activity is a second, separate skill file, generated fresh for each learner based on their own plan. That file is a single, self-contained markdown file: it can be loaded in a different session, a different agent, or by a different person entirely, and it will summarize itself and confirm readiness before taking any action.
