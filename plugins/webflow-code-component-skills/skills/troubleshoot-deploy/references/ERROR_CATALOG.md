# Error Catalog

Detailed solutions for common deployment errors.

## Authentication Errors

### "Authentication failed"

**Error:**
```
Error: Authentication failed. Please check your API token.
```

**Causes:**
1. Invalid API token
2. Expired token
3. Token from wrong workspace
4. Missing token

**Solution:**
```
🔧 Fix: Authentication Failed

**Step 1: Regenerate API Token**

1. Go to Webflow Dashboard
2. Navigate to Workspace Settings
3. Find "Apps & Integrations" → "Manage"
4. Under "Workspace API Access":
   - Revoke existing token (if any)
   - Click "Generate API Token"
   - Copy the new token

**Step 2: Update Token**

Option A - Environment variable:
```bash
export WEBFLOW_WORKSPACE_API_TOKEN=your-new-token
```

Option B - .env file:
```
WEBFLOW_WORKSPACE_API_TOKEN=your-new-token
```

**Step 3: Retry Deploy**
```bash
npx webflow library share
```

**Verification:**
Token should start with something like `wf_...`
```

---

### "Insufficient permissions"

**Error:**
```
Error: Insufficient permissions to access this workspace.
```

**Solution:**
```
🔧 Fix: Insufficient Permissions

Your API token doesn't have the required permissions.

**Check:**
1. Token is from the correct workspace
2. You have admin/editor role in that workspace
3. Token hasn't been revoked

**If you're not the workspace owner:**
Contact your workspace admin to either:
- Generate a token for you
- Give you the appropriate role

**Generate new token with correct workspace:**
1. Make sure you're in the right workspace in Webflow
2. Go to Workspace Settings → Apps & Integrations
3. Generate new API token
```

---

## Build Errors

### "Module not found"

**Error:**
```
Module not found: Error: Can't resolve '@webflow/react'
```

**Solution:**
```
🔧 Fix: Module Not Found

Missing required dependency.

**Install missing package:**
```bash
npm install --save-dev @webflow/react
```

**If still failing, install all Webflow packages:**
```bash
npm install --save-dev @webflow/webflow-cli @webflow/data-types @webflow/react
```

**Then retry:**
```bash
npx webflow library share
```
```

---

### "TypeScript errors"

**Error:**
```
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'.
```

**Solution:**
```
🔧 Fix: TypeScript Error

There's a type mismatch in your code.

**Common causes:**

1. **Wrong prop type:**
   ```typescript
   // ❌ Passing string when number expected
   <Component count="5" />

   // ✅ Correct type
   <Component count={5} />
   ```

2. **Missing prop:**
   ```typescript
   // ❌ Missing required prop
   <Component />

   // ✅ Include required prop
   <Component title="Hello" />
   ```

3. **Incorrect import:**
   ```typescript
   // ❌ Wrong import
   import { props } from "@webflow/react";

   // ✅ Correct import
   import { props } from "@webflow/data-types";
   ```

**To find the error:**
```bash
npx tsc --noEmit
```

This will show you exactly which file and line has the issue.
```

---

### "Unexpected token"

**Error:**
```
SyntaxError: Unexpected token '<'
```

**Solution:**
```
🔧 Fix: Syntax Error

Usually means JSX in a file that doesn't support it.

**Check:**

1. **File extension is correct:**
   - `.tsx` for TypeScript + JSX
   - `.jsx` for JavaScript + JSX
   - `.ts` for TypeScript (no JSX)

2. **tsconfig.json has JSX support:**
   ```json
   {
     "compilerOptions": {
       "jsx": "react-jsx"
     }
   }
   ```

3. **No syntax errors in JSX:**
   ```typescript
   // ❌ Common mistake - missing closing tag
   <div>
     <span>Hello
   </div>

   // ✅ Correct
   <div>
     <span>Hello</span>
   </div>
   ```
```

---

## Bundle Errors

### "Bundle size exceeds limit"

**Error:**
```
Error: Bundle size (62MB) exceeds the 50MB limit.
```

**Solution:**
```
🔧 Fix: Bundle Too Large

Your component library is over the 50MB limit.

**Step 1: Identify large dependencies**
```bash
npx webpack-bundle-analyzer dist/stats.json
```

Or check manually:
```bash
du -sh node_modules/* | sort -rh | head -20
```

**Step 2: Optimize**

Common culprits and alternatives:

| Heavy Package | Size | Alternative |
|--------------|------|-------------|
| moment | ~300KB | date-fns (~30KB) |
| lodash | ~530KB | lodash-es (tree-shakeable) |
| three.js | ~600KB | Dynamic import |
| @mui/material | ~500KB | Individual imports |

**Step 3: Tree-shake imports**

```typescript
// ❌ Imports entire library
import { Button, Card } from "@mui/material";

// ✅ Tree-shakeable
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
```

**Step 4: Lazy load heavy components**

```typescript
import { lazy, Suspense } from "react";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

export const MyComponent = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <HeavyComponent />
  </Suspense>
);
```

**Step 5: Remove unused dependencies**

```bash
npx depcheck
```
```

---

## Runtime Errors

### "Component not rendering"

**Problem:** Component appears in Designer but shows nothing

**Solution:**
```
🔧 Fix: Component Not Rendering

**Check 1: Build errors**
```bash
npx webflow library bundle --public-path http://localhost:4000/
```
Look for any errors in output.

**Check 2: Console errors**
1. Open Designer
2. Open browser DevTools (F12)
3. Check Console tab for errors

**Check 3: SSR issues**
If using browser APIs without guards:

```typescript
// ❌ Will break during SSR
export const Component = () => {
  const width = window.innerWidth;
  return <div>{width}</div>;
};

// ✅ SSR-safe
export const Component = () => {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    setWidth(window.innerWidth);
  }, []);

  return <div>{width || "Loading..."}</div>;
};
```

Or disable SSR:
```typescript
declareComponent(Component, {
  options: { ssr: false }
});
```

**Check 4: Missing root element**
Component must return a single root:

```typescript
// ❌ Multiple roots
export const Component = () => (
  <>
    <div>One</div>
    <div>Two</div>
  </>
);

// ✅ Single root
export const Component = () => (
  <div>
    <div>One</div>
    <div>Two</div>
  </div>
);
```
```

---

### "Styles not appearing"

**Problem:** Component renders but has no styling

**Solution:**
```
🔧 Fix: Missing Styles

**Cause:** Styles not imported in .webflow.tsx file

**Check 1: Import styles in definition file**

```typescript
// Button.webflow.tsx
import { declareComponent } from "@webflow/react";
import { Button } from "./Button";
import "./Button.module.css";  // ← Must be here!

declareComponent(Button, { ... });
```

**Check 2: Not using site classes**
Site classes don't work in Shadow DOM:

```css
/* ❌ Won't work */
.w-button { }

/* ✅ Use your own classes */
.my-button { }
```

**Check 3: CSS-in-JS needs decorator**

For styled-components:
```typescript
// globals.ts
import { styledComponentsShadowDomDecorator } from "@webflow/styled-components-utils";
export const decorators = [styledComponentsShadowDomDecorator];
```

```json
// webflow.json
{
  "library": {
    "globals": "./src/globals.ts"
  }
}
```
```

---

## Configuration Errors

### "webflow.json not found"

**Solution:**
```
🔧 Fix: Missing webflow.json

Create webflow.json in your project root:

```json
{
  "library": {
    "name": "My Component Library",
    "components": ["./src/**/*.webflow.tsx"]
  }
}
```

**Full configuration options:**

```json
{
  "library": {
    "name": "My Component Library",
    "components": ["./src/**/*.webflow.tsx"],
    "globals": "./src/globals.ts",
    "bundleConfig": "./webpack.webflow.js"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Library name in Designer |
| components | Yes | Glob pattern for .webflow.tsx files |
| globals | No | Path to globals/decorators |
| bundleConfig | No | Custom webpack config |
```

---

### "No components found"

**Error:**
```
Warning: No components found matching pattern "./src/**/*.webflow.tsx"
```

**Solution:**
```
🔧 Fix: No Components Found

**Check 1: File extension**
Files must end with `.webflow.tsx` (not `.webflow.ts` or `.tsx`)

**Check 2: File location**
Files must match the glob pattern in webflow.json

Example pattern: `"./src/**/*.webflow.tsx"`
Valid locations:
- ./src/Button.webflow.tsx ✅
- ./src/components/Button.webflow.tsx ✅
- ./components/Button.webflow.tsx ❌ (not in src/)

**Check 3: declareComponent is called**
Each file must call declareComponent:

```typescript
import { declareComponent } from "@webflow/react";
import { Button } from "./Button";

declareComponent(Button, {  // ← Required!
  name: "Button"
});
```

**Check 4: List your files**
```bash
find . -name "*.webflow.tsx"
```
```
