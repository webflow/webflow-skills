# Grammar & Mechanics Reference

## Table of Contents
1. AP Style
2. Active vs. Passive Voice
3. Contractions
4. Capitalization
5. Pronouns
6. Verb Tenses
7. Punctuation
8. Abbreviations
9. Numbers
10. Lists

---

## 1. AP Style

Webflow uses Associated Press (AP) style for in-product writing. When in doubt, check AP guidelines.

---

## 2. Active vs. Passive Voice

Use active voice by default. Switch to passive to soften a message or avoid blaming the user.

**Active (default):**
- YES: "You can update your payment info under the billing tab."
- NO: "Payment info can be updated under the billing tab."

**Passive (to soften):**
- YES: "Your payment was declined."
- NO: "We declined your payment."
- YES: "Your bill wasn't paid."
- NO: "You didn't pay your bill."

---

## 3. Contractions

Use contractions for a conversational tone. Avoid contractions that sound awkward or outdated.

**Use:** Can't, Don't, You're, Doesn't, Shouldn't, It's, Couldn't, I'm, Hasn't, Haven't, You've

**Avoid:** That'll, Would've, This'll, There're, Mustn't, Needn't, Who've, Gotta, It'd, Ain't, Ya'll

---

## 4. Capitalization

Webflow uses **sentence case everywhere** — lowercase everything unless it:
- Starts a sentence
- Starts a heading
- Starts a CTA
- Is a proper noun or product name

**Team names:** Capitalize the team name, lowercase "team" — e.g., Support team, Content team.

**YES:** "This is sentence case"
**NO:** "This Is Title Case"

See `terminology.md` for specific product/feature capitalization.

---

## 5. Pronouns

### Second person (you/your) — Use in most situations
- YES: "You can update your billing information on the settings page."
- NO: "I can update my billing information on the settings page."

### First person (I/me/my) — Only when:
- Users are answering a direct question
- Sensitivity or privacy are important
- Legal requires consent
- YES: "I agree to these terms of service."
- NO: "You agree to these terms of service."

### "They" — Use for inclusive, gender-neutral language
- YES: "Amrita accepted your invite — assign them a role."
- NO: "Amrita accepted your invite — assign him/her a role."

### "We" — Generally avoid in interface copy
Use "we" only if:
- Users are waiting for a response from us
- An error message needs to clarify who needs to take action
- YES: "We'll review your request and get back to you within 2 business days."
- YES: "We lost the connection. Try refreshing the page."
- NO: "We heard your feedback and now you can do all these awesome things."
- NO: "We'll get your billing info updated." (Use: "Update your billing info from the Settings tab.")

---

## 6. Verb Tenses

Use simple verb tenses — past, present, future — to keep things concise and scannable.

- YES: "You upgraded your Site plan." / NO: "You're upgrading your Site plan."
- YES: "You can't undo this action." / NO: "You're not undoing this action."
- YES: "Your credit card will be charged at the end of the month." / NO: "Your credit card will have been charged at the end of the month."

---

## 7. Punctuation

### Ampersand (&)
Avoid in body copy. Optional in links, buttons, and headings to reduce character count.

### Apostrophe
Don't use in place of quotation marks.

### At sign (@)
Don't replace the word "at" with @.

### Brackets/Parentheses
Avoid [] in product copy. Use () sparingly. Em dashes are often less visually noisy.
- If parenthetical is part of a sentence, period goes after closing parenthesis.
- (If parenthetical is its own sentence, period goes before closing parenthesis.)

### Comma (Oxford comma)
Always use the serial comma in lists of 3+ items.
- YES: "Save your file as a JPEG, PNG, or GIF."
- NO: "Save your file as a JPEG, PNG or GIF."

If a sentence has 3+ commas or wordy items, consider a bulleted list.

### Ellipsis (...)
Include a space before and after.
- YES: "Your Collection list is saving …"
- NO: "Your Collection list is saving…"

### Em dash (—)
Use with a space on each side for an aside or dramatic pause.
- "Drag, drop, design — and let Webflow take care of the code."
- Make: Option + Shift + Hyphen (Mac), or &mdash; in HTML

### En dash (–)
Use with no spaces in a range (times, dates).
- "12pm–2pm, April 12–13"
- Make: Option + Hyphen (Mac), or &ndash; in HTML

### Hyphen (-)
Between hyphenated words, no spaces.
- "View-only mode"

### Exclamation point
Use sparingly. Only exclaim about things users are likely excited about. Difficult to localize.

### Percent
Use the symbol (%) instead of spelling out the word.

### Period
Full sentences get periods — yes, even on tooltips and toasts.
- One space after a period, never two.
- No periods at the end of: headings (unless multiple sentences), short phrases, buttons, bulleted lists (unless one item needs a period, then use on all).

### Question mark
Avoid on alert headings or rhetorical questions.
- YES: "Delete template"
- NO: "Delete template?"

### Quotation marks
Use double quotes ("") for quoting text or referring to file/asset names.
- Place punctuation inside quotation marks — unless referring to typed commands.
- YES: Avoid words like "all," "every," or "most."
- YES: To remove this Collection list, type "DELETE".

### Semicolon
Avoid. Use periods, commas, or em dashes instead.

### Slash
Use "and" or "or" instead.

---

## 8. Abbreviations

### Amounts
Capitalized, no periods: K (thousands), M (millions), B (billions)

### Measurements
Use AP style abbreviations. Spell out in full sentences. Space between number and unit (e.g., 2 px, 3 MB).

### Months
First 3 letters, no periods: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec

### Days
First 3 letters, no periods: Sun, Mon, Tue, Wed, Thu, Fri, Sat

### Time
Space between number and unit, no period, no comma: Sec, Min, Hr
- E.g., "3 hr 42 min"
- Lowercase am/pm without space: 3pm (unless using 24-hour clock: 16:30)

---

## 9. Numbers

### Currency
Use number form without decimal unless cents are involved.
- YES: "$10 will be returned to your card."
- NO: "$10.00 will be returned to your card."
- YES: "You'll be charged $35.60 on the 5th of every month."
- Use international abbreviations: 100 CAD

### Large numbers
Comma-separate groups of 3 digits: 1,000 / 10,000 / 100,000 / 1,000,000

### Numerals
Always use numerals instead of number words.
- YES: "You have 3 member seats available."
- NO: "You have three member seats available."

---

## 10. Lists

- Use numbered lists for sequential steps
- Use bulleted lists when sequence doesn't matter
- Introduce with a colon or heading
- Capitalize the first letter of each item
- Use parallel construction (same word type, tense, voice, sentence type)

**Parallel example:**
- YES: Designer / Editor / Viewer
- NO: Being the Designer / Editor / And a Viewer
