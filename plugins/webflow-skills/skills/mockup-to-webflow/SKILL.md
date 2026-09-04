---
name: webflow-mcp:mockup-to-webflow
description: Guide a user through building a Webflow site from scratch using a visual mockup as reference. Use when recreating a design, translating a mockup or wireframe into Webflow, asking how to build layouts, styling questions, responsive design, breakpoint optimization, mobile-first design, or general Webflow beginner questions. Requires Webflow Designer connection.
---

# Mockup to Webflow

Guide a beginner through translating a visual mockup into a live Webflow site, with responsive and breakpoint optimization.

## Important Note

ALWAYS use Webflow MCP tools for all operations:

- Use Webflow MCP's `webflow_guide_tool` to get best practices before any other tool call
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify the target site
- Use Webflow MCP's `de_page_tool` to get current page, switch pages, or create pages
- Use Webflow MCP's `element_tool` with action `get_all_elements` to retrieve page structure
- Use Webflow MCP's `element_builder` to create new elements
- Use Webflow MCP's `element_snapshot_tool` to get visual previews before and after changes
- Use Webflow MCP's `style_tool` to create and update styles, including breakpoint-specific styles
- Use Webflow MCP's `de_learn_more_about_styles` to check supported style properties and breakpoint syntax
- Use Webflow MCP's `data_components_tool` to inspect or update reusable components
- DO NOT use any other tools or methods for Webflow operations
- All tool calls must include the required context parameter (15-25 words, third-person perspective)
- Designer connection required -- user must have Webflow Designer open and connected

## Instructions

### Phase 1: Understand the Mockup

1. Call `webflow_guide_tool` first -- always the first MCP tool call in any workflow
2. Ask the user to describe or share their mockup (sections, layout, content, fonts, colors)
3. Break the mockup into sections (e.g. Navbar, Hero, Features, Footer) and confirm with the user
4. Ask about target devices: desktop-first or mobile-first?
5. Identify the Webflow breakpoints to target:
   - Desktop (default, 992px+)
      - Tablet (991px and below)
         - Mobile Landscape (767px and below)
            - Mobile Portrait (479px and below)

            ### Phase 2: Site & Page Setup

            6. Call `data_sites_tool` with `list_sites` to identify the target site
            7. Call `de_page_tool` to confirm the active page, or create a new page if needed
            8. Confirm page settings with user (slug, title, SEO basics if relevant)

            ### Phase 3: Section-by-Section Build Planning

            9. For each section in the mockup, present a build plan before touching anything:
               - Element type (Section, Container, Grid, Flexbox Div, etc.)
                  - Layout approach (Flexbox vs Grid, column count, alignment)
                     - Content (headings, text, images, buttons, links)
                        - Styles (spacing, colors, typography)
                        10. Ask: "Shall I build the [section name] section now?" before proceeding
                        11. Explain Webflow concepts in plain language when introducing unfamiliar tools (e.g. "A Flexbox Div is a box that arranges its children in a row or column automatically")

                        ### Phase 4: Build Execution (after confirmation only)

                        12. Call `element_snapshot_tool` to capture current page state
                        13. Call `element_builder` to create the section structure (max 3 levels per call -- build deeper structures in stages)
                        14. Call `style_tool` to apply desktop styles first (default breakpoint)
                        15. After desktop styles are confirmed, apply responsive styles per breakpoint (tablet -> mobile landscape -> mobile portrait)
                        16. Call `element_snapshot_tool` after each major section to show the result

                        ### Phase 5: Responsive & Breakpoint Optimization

                        17. After each section is built at desktop, walk through responsive behavior:
                            - Identify elements that need layout changes at smaller breakpoints (e.g. stacked columns, hidden elements, resized text)
                                - Use `de_learn_more_about_styles` to confirm breakpoint-specific style syntax
                                    - Apply breakpoint overrides using `style_tool` for each target breakpoint
                                        - Snapshot the result at each breakpoint
                                        18. Explain what each responsive change does in plain English (e.g. "On tablet, the two-column grid becomes a single column so it doesn't feel cramped")

                                        ### Phase 6: Beginner Q&A

                                        19. At any point, if the user asks a "how do I" or "what is" question about Webflow:
                                            - Answer in plain, jargon-free language
                                                - Use `webflow_guide_tool` to pull in best practices where relevant
                                                    - Offer a concrete next step or example after explaining
                                                    20. Common beginner topics to handle proactively:
                                                        - Classes vs inline styles (always use classes)
                                                            - When to use Grid vs Flexbox
                                                                - How Webflow inheritance works (desktop styles cascade down to smaller breakpoints)
                                                                    - Symbols/Components vs one-off elements
                                                                        - What "combo classes" are and when to use them

                                                                        ### Phase 7: Final Review

                                                                        21. After all sections are built, do a full-page snapshot with `element_snapshot_tool`
                                                                        22. Present a checklist of what was built and what responsive breakpoints were addressed
                                                                        23. Flag any sections that still need attention or were skipped

                                                                        ## Examples

                                                                        ### Example 1: Starting from a mockup description

                                                                        **User:** "I have a mockup with a sticky navbar, a hero with a headline and button, a 3-column features section, and a footer. Help me build it."

                                                                        1. Call `webflow_guide_tool`
                                                                        2. Confirm breakdown: Navbar -> Hero -> Features (3-col) -> Footer
                                                                        3. Ask: "Are you designing desktop-first or mobile-first?"
                                                                        4. Call `data_sites_tool` with `list_sites`
                                                                        5. Call `de_page_tool` to confirm active page
                                                                        6. Present plan for Navbar: "I'll create a Navbar element with a logo div on the left and nav links on the right using Flexbox. Shall I proceed?"
                                                                        7. After confirmation, call `element_snapshot_tool`, then `element_builder`, then `style_tool`
                                                                        8. Repeat for each section

                                                                        ### Example 2: Responsive optimization

                                                                        **User:** "The 3-column features section looks squished on mobile. How do I fix it?"

                                                                        1. Call `webflow_guide_tool`
                                                                        2. Explain: "On mobile, a 3-column grid is too narrow. We'll switch it to a 1-column stack on Mobile Portrait."
                                                                        3. Call `element_tool` with `get_all_elements` to locate the features grid
                                                                        4. Call `de_learn_more_about_styles` to confirm breakpoint grid syntax
                                                                        5. Present plan: "I'll override the grid to 1 column at the Mobile Portrait breakpoint. Shall I proceed?"
                                                                        6. After confirmation, call `style_tool` with the mobile breakpoint override
                                                                        7. Call `element_snapshot_tool` to show the result

                                                                        ### Example 3: Beginner question mid-build

                                                                        **User:** "What's the difference between a class and a combo class?"

                                                                        Answer: "A class in Webflow is a reusable style you give to an element -- like 'Button'. A combo class adds extra styles on top of an existing class without changing the original -- like 'Button' + 'Button--primary'. This lets you have variations of the same element without duplicating styles. In general, start with a base class and add combo classes for variations."

                                                                        Then offer: "Want me to apply this approach to the buttons in your mockup?"

                                                                        ### Example 4: Building a hero section

                                                                        **User:** "Build the hero -- it has a background image, a large headline, a subheading, and a CTA button centered on the page."

                                                                        1. Call `webflow_guide_tool`
                                                                        2. Call `element_snapshot_tool` to capture current state
                                                                        3. Present plan: "I'll create a Section with a background image style, a centered Flexbox Container inside, and a Heading, Paragraph, and Button stacked vertically. Shall I proceed?"
                                                                        4. After confirmation, call `element_builder` with the Section -> Container -> [Heading, Paragraph, Button] structure
                                                                        5. Call `style_tool` to set background image, min-height, Flexbox centering, and typography
                                                                        6. Call `element_snapshot_tool` to show the result

                                                                        ## Guidelines

                                                                        - `webflow_guide_tool` always first -- before any other MCP tool in every workflow
                                                                        - Desktop styles first, then breakpoints -- Webflow styles cascade from desktop down; always set desktop before overriding at smaller sizes
                                                                        - Snapshot before and after every section -- use `element_snapshot_tool` to show progress
                                                                        - Never silently mutate -- every write operation requires explicit user confirmation
                                                                        - Explain before building -- always describe what you're about to create in plain English before calling any builder tools
                                                                        - Use native layout tools -- prefer Webflow's Grid and Flexbox over manual positioning or fixed widths
                                                                        - One section at a time -- don't batch-build multiple sections without confirming each; beginners need to follow along
                                                                        - Jargon-free explanations -- when using Webflow-specific terms (combo class, symbol, breakpoint, cascade), explain them briefly on first use
                                                                        - Classes over inline styles -- always apply styles via named classes, never inline; explain this to the user if they ask why
                                                                        - Flag complexity early -- if a mockup element is complex (e.g. sticky scroll effects, custom interactions), flag it before starting and ask if the user wants to tackle it now or later
