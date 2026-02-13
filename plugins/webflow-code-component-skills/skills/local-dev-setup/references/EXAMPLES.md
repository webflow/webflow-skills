# Local Dev Setup Examples

Detailed setup examples for different scenarios.

## Example 1: New Project from Scratch

```
🛠️ Local Dev Setup: New Code Components Project

I'll set up a complete code components project for you.

---

## Step 1: Initialize Project

**Create project directory and initialize npm:**
```bash
mkdir my-webflow-components
cd my-webflow-components
npm init -y
```

---

## Step 2: Install Dependencies

**Core dependencies:**
```bash
npm install react react-dom
npm install -D typescript @types/react @types/react-dom
```

**Webflow dependencies:**
```bash
npm install -D @webflow/webflow-cli @webflow/data-types @webflow/react
```

---

## Step 3: Configure TypeScript

**Create tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Step 4: Create webflow.json

**Create webflow.json in project root:**
```json
{
  "library": {
    "name": "My Component Library",
    "components": ["./src/**/*.webflow.tsx"]
  }
}
```

---

## Step 5: Create Project Structure

```bash
mkdir -p src/components/Button
```

**Project structure:**
```
my-webflow-components/
├── src/
│   ├── components/
│   │   └── Button/
│   │       ├── Button.tsx
│   │       ├── Button.webflow.tsx
│   │       └── Button.module.css
│   └── declarations.d.ts
├── package.json
├── tsconfig.json
├── webflow.json
└── .gitignore
```

---

## Step 5.5: Create Type Declarations

**Create src/declarations.d.ts for CSS module support:**
```typescript
declare module "*.module.css" {
  const classes: { [key: string]: string };
  export default classes;
}

declare module "*.css" {
  const content: string;
  export default content;
}
```

This file tells TypeScript how to handle CSS module imports.

---

## Step 6: Create Example Component

**src/components/Button/Button.tsx:**
```typescript
import React from "react";
import styles from "./Button.module.css";

export interface ButtonProps {
  label: string;
  variant: "primary" | "secondary" | "outline";
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = "primary",
  disabled = false,
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      disabled={disabled}
    >
      {label}
    </button>
  );
};
```

**src/components/Button/Button.webflow.tsx:**
```typescript
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { Button } from "./Button";
import "./Button.module.css";

declareComponent(Button, {
  name: "Button",
  description: "A customizable button component",
  group: "Interactive",
  props: {
    label: props.Text({
      name: "Label",
      defaultValue: "Click me",
    }),
    variant: props.Variant({
      name: "Style",
      options: ["primary", "secondary", "outline"],
      defaultValue: "primary",
    }),
    disabled: props.Boolean({
      name: "Disabled",
      defaultValue: false,
    }),
  },
});
```

**src/components/Button/Button.module.css:**
```css
.button {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.secondary {
  background-color: #6b7280;
  color: white;
}

.secondary:hover:not(:disabled) {
  background-color: #4b5563;
}

.outline {
  background-color: transparent;
  border-color: #3b82f6;
  color: #3b82f6;
}

.outline:hover:not(:disabled) {
  background-color: #3b82f6;
  color: white;
}
```

---

## Step 7: Create .gitignore

**.gitignore:**
```
node_modules/
dist/
.env
*.log
```

---

## Step 8: Test Build

**Verify everything works:**
```bash
npx webflow library bundle --public-path http://localhost:4000/
```

Expected output:
```
✓ Bundling components...
✓ Found 1 component(s)
✓ Build complete
```

---

## ✅ Setup Complete!

**Your project is ready. Here's what you can do next:**

### Create More Components
```bash
mkdir src/components/Card
```
Then create Card.tsx, Card.webflow.tsx, and Card.module.css

### Deploy to Webflow
```bash
npx webflow library share
```

### Development Workflow
1. Make changes to components
2. Test build: `npx webflow library bundle --public-path http://localhost:4000/`
3. Deploy: `npx webflow library share`

---

💡 **Tips:**
- Use `component-scaffold` skill to quickly create new components
- Run `build-validate` skill before deploying
- Keep bundle under 50MB
```

---

## Example 2: Add to Existing React Project

```
🛠️ Adding Code Components to Existing Project

I see you have an existing React project. Let me add Webflow Code Components support.

---

## Step 1: Install Webflow Dependencies

```bash
npm install -D @webflow/webflow-cli @webflow/data-types @webflow/react
```

---

## Step 2: Create webflow.json

Add to your project root:

```json
{
  "library": {
    "name": "My Component Library",
    "components": ["./src/webflow-components/**/*.webflow.tsx"]
  }
}
```

I'm putting components in a separate folder to keep them organized.

---

## Step 3: Create Components Directory

```bash
mkdir -p src/webflow-components
```

---

## Step 4: Create Definition Files

For each component you want to export to Webflow, create a `.webflow.tsx` file:

**src/webflow-components/Button.webflow.tsx:**
```typescript
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
// Import your existing component
import { Button } from "../components/Button";

declareComponent(Button, {
  name: "Button",
  description: "Your existing button component",
  props: {
    // Map your component props to Webflow props
    children: props.Text({
      name: "Label",
      defaultValue: "Click me"
    }),
    variant: props.Variant({
      name: "Variant",
      options: ["primary", "secondary"],
      defaultValue: "primary"
    })
  }
});
```

---

## Step 5: Handle Styling

If your existing components use:

**CSS Modules:** Import in .webflow.tsx file
```typescript
import "../components/Button/Button.module.css";
```

**styled-components:** Add decorator
```typescript
// src/webflow-components/globals.ts
import { styledComponentsShadowDomDecorator } from "@webflow/styled-components-utils";
export const decorators = [styledComponentsShadowDomDecorator];
```

Update webflow.json:
```json
{
  "library": {
    "globals": "./src/webflow-components/globals.ts"
  }
}
```

---

## Step 6: Update .gitignore

Add:
```
.env
```

---

## Step 7: Test

```bash
npx webflow library bundle --public-path http://localhost:4000/
```

---

✅ **Integration complete!**

Your existing components can now be deployed to Webflow.
```

---

## Example 3: With Tailwind CSS

```
🛠️ Setup with Tailwind CSS

Setting up Code Components with Tailwind CSS support.

---

## Step 1: Initialize Project

```bash
mkdir my-tailwind-components
cd my-tailwind-components
npm init -y
```

---

## Step 2: Install Dependencies

```bash
# Core
npm install react react-dom
npm install -D typescript @types/react @types/react-dom

# Webflow
npm install -D @webflow/webflow-cli @webflow/data-types @webflow/react

# Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## Step 3: Configure Tailwind

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

---

## Step 4: Create Globals

**src/globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**src/globals.ts:**
```typescript
import "./globals.css";
```

---

## Step 5: Configure webflow.json

```json
{
  "library": {
    "name": "My Tailwind Library",
    "components": ["./src/**/*.webflow.tsx"],
    "globals": "./src/globals.ts"
  }
}
```

---

## Step 6: Create Example Component

**src/components/Card/Card.tsx:**
```typescript
import React from "react";

export interface CardProps {
  title: string;
  description: string;
  featured?: boolean;
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  featured = false,
}) => {
  return (
    <div className={`
      p-6 rounded-lg shadow-md
      ${featured ? "bg-blue-50 border-2 border-blue-500" : "bg-white"}
    `}>
      <h2 className="text-xl font-bold text-gray-900 mb-2">{title}</h2>
      <p className="text-gray-600">{description}</p>
      {featured && (
        <span className="inline-block mt-4 px-3 py-1 bg-blue-500 text-white text-sm rounded-full">
          Featured
        </span>
      )}
    </div>
  );
};
```

**src/components/Card/Card.webflow.tsx:**
```typescript
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { Card } from "./Card";

declareComponent(Card, {
  name: "Card",
  description: "A card with Tailwind styling",
  props: {
    title: props.Text({
      name: "Title",
      defaultValue: "Card Title",
    }),
    description: props.Text({
      name: "Description",
      defaultValue: "Card description goes here.",
    }),
    featured: props.Boolean({
      name: "Featured",
      defaultValue: false,
    }),
  },
});
```

---

## Step 7: Test

```bash
npx webflow library bundle --public-path http://localhost:4000/
```

---

✅ **Tailwind setup complete!**

All Tailwind utility classes are now available in your components.
```
