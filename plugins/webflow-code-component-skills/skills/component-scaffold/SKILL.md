---
name: component-scaffold
description: Generate new Webflow Code Component boilerplate with React component, definition file, and optional styling. Automatically checks prerequisites and can set up missing config/dependencies.
compatibility: Node.js 18+, React 18+, TypeScript, @webflow/webflow-cli
metadata:
  author: webflow
  version: "1.0"
---

# Component Scaffold

Generate a new Webflow Code Component with proper file structure, React component, and `.webflow.tsx` definition file.

## When to Use This Skill

**Use when:**
- Creating a new code component from scratch
- User asks to scaffold, generate, or create a component
- Starting a new component with proper Webflow file structure

**Do NOT use when:**
- Converting an existing React component (use convert-component skill)
- Modifying existing components (answer directly or use component-audit)
- Just asking questions about components (answer directly)
- Setting up a complex project with custom bundler config (use local-dev-setup instead)

**Note:** This skill can handle basic setup (webflow.json + dependencies) automatically. Use local-dev-setup only for complex setups requiring Tailwind, custom webpack config, or monorepo configurations.

## Instructions

### Phase 0: Prerequisites Check (Run First)

Before gathering any requirements, verify the project is set up for Webflow Code Components:

1. **Check for webflow.json**:
   ```bash
   # Look for webflow.json in project root
   ```
   - If missing: Offer to create it or invoke local-dev-setup skill

2. **Check for required dependencies** in package.json:
   ```json
   {
     "devDependencies": {
       "@webflow/webflow-cli": "...",
       "@webflow/data-types": "...",
       "@webflow/react": "..."
     }
   }
   ```
   - If missing: Offer to install them:
     ```bash
     npm i --save-dev @webflow/webflow-cli @webflow/data-types @webflow/react
     ```

3. **Check for components directory**:
   - Look for existing pattern (e.g., `src/components/`)
   - If no components exist, determine where to create them based on webflow.json config

4. **Report setup status**:

   **If all prerequisites met:**
   ```
   ✅ Project ready for code components
   - webflow.json: Found
   - Dependencies: Installed
   - Components path: src/components/

   Let's create your component...
   ```

   **If prerequisites missing:**
   ```
   ⚠️ Project Setup Required

   Missing:
   - [ ] webflow.json configuration file
   - [ ] @webflow/webflow-cli dependency
   - [ ] @webflow/data-types dependency
   - [ ] @webflow/react dependency

   Would you like me to:
   1. Set up the missing items now (quick setup)
   2. Run full project initialization (local-dev-setup skill)

   Choose an option:
   ```

   **Quick setup** creates minimal config:
   ```json
   // webflow.json
   {
     "library": {
       "name": "My Component Library",
       "components": ["./src/components/**/*.webflow.tsx"]
     }
   }
   ```
   And installs dependencies.

**Only proceed to Phase 1 after prerequisites are confirmed.**

---

### Phase 1: Gather Requirements

1. **Get component name**: Ask user for the component name
   - Must be PascalCase (e.g., "Accordion", "ProductCard")
   - Suggest name if user provides description instead

2. **Determine component type**: Ask what kind of component
   - Interactive (buttons, forms, accordions)
   - Display (cards, banners, testimonials)
   - Layout (grids, containers, sections)
   - Data-driven (lists, tables, charts)

3. **Identify props needed**: Based on component type, suggest props
   - Text content → `props.Text()` or `props.RichText()`
   - Images → `props.Image()`
   - Links → `props.Link()`
   - Variants/styles → `props.Variant()`
   - Nested content → `props.Slot()`
   - Toggles → `props.Boolean()`

4. **Styling approach**: Ask preferred styling method
   - CSS Modules (default, recommended)
   - Tailwind CSS
   - styled-components
   - Plain CSS

5. **SSR requirements**: Determine if component needs client-only features
   - Uses browser APIs? → `ssr: false`
   - Pure presentation? → `ssr: true` (default)

### Phase 2: Validate Project Setup

6. **Check project structure**:
   - Verify `webflow.json` exists
   - Check for required dependencies
   - Identify components directory pattern

7. **Check for conflicts**:
   - Ensure component name doesn't already exist
   - Verify no `.webflow.tsx` file with same name

### Phase 3: Generate Files

8. **Create directory structure**:
```
src/components/[ComponentName]/
├── [ComponentName].tsx
├── [ComponentName].webflow.tsx
└── [ComponentName].module.css (if CSS Modules)
```

9. **Generate React component** (`[ComponentName].tsx`):
```typescript
import React from "react";
import styles from "./[ComponentName].module.css";

export interface [ComponentName]Props {
  // Props interface based on user requirements
}

export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  // Destructured props with defaults
}) => {
  return (
    <div className={styles.container}>
      {/* Component JSX */}
    </div>
  );
};
```

10. **Generate definition file** (`[ComponentName].webflow.tsx`):
```typescript
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { [ComponentName] } from "./[ComponentName]";
import "./[ComponentName].module.css";

declareComponent([ComponentName], {
  name: "[ComponentName]",
  description: "[User-provided or generated description]",
  group: "[Category]",
  props: {
    // Props configuration based on requirements
  },
  options: {
    applyTagSelectors: true,
    ssr: true // or false based on requirements
  }
});
```

11. **Generate styles** (if CSS Modules):
```css
.container {
  /* Base styles */
}
```

### Phase 4: Provide Guidance

12. **Show created files**: List all files created with paths

13. **Explain next steps**:
    - Implement component logic
    - Add styling
    - Test locally by running the React project (e.g., `npm run dev`)
    - Deploy to Webflow with `npx webflow library share`

14. **Warn about naming**:
```
⚠️ Important: Do not rename the .webflow.tsx file after deployment.
Renaming creates a new component and breaks existing instances.
```

## Examples

**User prompt:**
```
Create an accordion component
```

**Step 1: Requirements Gathering**
```
📦 New Component: Accordion

I'll create an accordion component. Let me confirm the requirements:

**Props to include:**
1. `title` (Text) - The accordion header text
2. `content` (Rich Text) - The expandable content
3. `defaultOpen` (Boolean) - Whether to start expanded
4. `icon` (Variant) - Chevron style: "arrow" | "plus" | "none"

**Styling:** CSS Modules (recommended for Shadow DOM)

**SSR:** Enabled (no browser-only APIs needed)

Does this look right? Any props to add or remove?
```

**Step 2: After User Confirms**
```
📁 Creating Component Files...

Created:
├── src/components/Accordion/Accordion.tsx
├── src/components/Accordion/Accordion.webflow.tsx
└── src/components/Accordion/Accordion.module.css

✅ Component scaffold complete!

---

**Accordion.tsx** - React component with:
- Props: title, content, defaultOpen, icon
- State management for open/closed
- Accessible keyboard navigation
- CSS Module classes

**Accordion.webflow.tsx** - Webflow definition with:
- All props configured for Designer editing
- Default values set
- SSR enabled

---

💡 Next Steps:
1. Review and customize the generated code
2. Test locally by running your React project (e.g., `npm run dev`)
3. Deploy to Webflow: `npx webflow library share`

⚠️ Remember: Don't rename .webflow.tsx files after deployment!
```

**Generated Accordion.tsx:**
```typescript
import React, { useState } from "react";
import styles from "./Accordion.module.css";

export interface AccordionProps {
  title: string;
  content: string;
  defaultOpen?: boolean;
  icon?: "arrow" | "plus" | "none";
}

export const Accordion: React.FC<AccordionProps> = ({
  title,
  content,
  defaultOpen = false,
  icon = "arrow"
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className={styles.accordion}>
      <button
        className={styles.header}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className={styles.title}>{title}</span>
        {icon !== "none" && (
          <span className={`${styles.icon} ${isOpen ? styles.open : ""}`}>
            {icon === "arrow" ? "▼" : "+"}
          </span>
        )}
      </button>
      {isOpen && (
        <div
          className={styles.content}
          dangerouslySetInnerHTML={{ __html: content }}
        />
      )}
    </div>
  );
};
```

**Generated Accordion.webflow.tsx:**
```typescript
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { Accordion } from "./Accordion";
import "./Accordion.module.css";

declareComponent(Accordion, {
  name: "Accordion",
  description: "Expandable content section with customizable header and icon",
  group: "Interactive",
  props: {
    title: props.Text({
      name: "Title",
      defaultValue: "Accordion Title"
    }),
    content: props.RichText({
      name: "Content",
      defaultValue: "<p>Accordion content goes here.</p>"
    }),
    defaultOpen: props.Boolean({
      name: "Start Expanded",
      defaultValue: false
    }),
    icon: props.Variant({
      name: "Icon Style",
      options: ["arrow", "plus", "none"],
      defaultValue: "arrow"
    })
  },
  options: {
    applyTagSelectors: true,
    ssr: true
  }
});
```

## Guidelines

### Prop Type Selection

| User Wants | Prop Type | Notes |
|------------|-----------|-------|
| Editable text | `props.Text()` | Single line, max 256 chars |
| Long formatted text | `props.RichText()` | HTML content |
| Canvas-editable text | `props.TextNode()` | Double-click to edit |
| Image upload | `props.Image()` | Returns image object |
| URL/link | `props.Link()` | Returns { href, target, preload } |
| Number input | `props.Number()` | Numeric values |
| Toggle/flag | `props.Boolean()` | true/false |
| Style options | `props.Variant()` | Dropdown selection |
| Nested content | `props.Slot()` | Other components inside |
| HTML ID | `props.Id()` | For accessibility |

### Component Categories (Groups)

- **Interactive**: Buttons, forms, accordions, tabs, modals
- **Display**: Cards, banners, testimonials, badges
- **Layout**: Grids, containers, sections, dividers
- **Navigation**: Menus, breadcrumbs, pagination
- **Media**: Galleries, video players, carousels
- **Data**: Tables, lists, charts, counters

### SSR Decision Tree

```
Does component use window, document, or localStorage?
├── Yes → Set ssr: false
└── No
    └── Does component use useEffect for initialization?
        ├── Yes (for browser APIs) → Set ssr: false
        └── No → Keep ssr: true (default)
```

### File Naming Rules

- Component name: PascalCase (`ProductCard`)
- Files use same name: `ProductCard.tsx`, `ProductCard.webflow.tsx`
- CSS modules: `ProductCard.module.css`
- Directory: `src/components/ProductCard/`

### Default Values Best Practice

Always provide meaningful defaults:
```typescript
props: {
  title: props.Text({
    name: "Title",
    defaultValue: "Card Title"  // ✅ Good
  }),
  count: props.Number({
    name: "Count",
    defaultValue: 0  // ✅ Good
  })
}
```

Not:
```typescript
props: {
  title: props.Text({
    name: "Title"
    // ❌ Missing defaultValue
  })
}
```

## Error Handling

**Component name already exists:**
```
⚠️ Component "Button" already exists at src/components/Button/

Options:
1. Choose a different name
2. Update existing component (use component-audit skill)
3. Delete existing and create new

Which would you like to do?
```

**Missing webflow.json:**
```
❌ No webflow.json found in project root

This file is required for code components. Would you like me to:
1. Create a basic webflow.json
2. Run local-dev-setup skill for full project initialization

Choose an option (1/2):
```

**Invalid component name:**
```
⚠️ Invalid component name: "my-button"

Component names must be:
- PascalCase (e.g., "MyButton")
- Start with a letter
- Contain only letters and numbers

Suggested name: "MyButton"

Use this name? (yes/no)
```
