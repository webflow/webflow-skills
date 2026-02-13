---
name: build-validate
description: Pre-deployment validation for Webflow Code Components. Checks bundle size, dependencies, prop configurations, SSR compatibility, and common issues before running webflow library share.
compatibility: Node.js 18+, React 18+, TypeScript, @webflow/webflow-cli
metadata:
  author: webflow
  version: "1.0"
---

# Build Validate

Validate code components before deployment to catch issues early.

## When to Use This Skill

**Use when:**
- User is about to deploy and wants to check for issues first
- Proactively before running `webflow library share`
- User asks to validate, check, or verify their components
- After making significant changes to components

**Do NOT use when:**
- Deployment already failed (use troubleshoot-deploy instead)
- Just building for local development
- Auditing code quality (use component-audit instead)

## Instructions

### Phase 1: Project Structure Check

1. **Verify webflow.json exists**:
   - Check for required fields (library.name, library.components)
   - Validate glob pattern matches component files
   - Check globals path if specified

2. **Check dependencies**:
   - Verify @webflow/webflow-cli installed
   - Verify @webflow/data-types installed
   - Verify @webflow/react installed
   - Check for version compatibility

3. **Verify component files**:
   - Find all `.webflow.tsx` files
   - Ensure matching React components exist
   - Check for orphaned definition files

### Phase 2: Component Analysis

4. **For each component, check**:
   - `declareComponent` is called
   - Component name is provided
   - All props have names and defaultValues
   - Prop types are valid

5. **Check for SSR issues**:
   - Scan for `window`, `document`, `localStorage` usage
   - Flag usage outside of `useEffect`
   - Suggest `ssr: false` if appropriate

6. **Check styling**:
   - Verify styles are imported in `.webflow.tsx`
   - Check for site class usage (won't work)
   - Validate CSS-in-JS setup if used

### Phase 3: Build Test

7. **Run TypeScript/build check**:
   - Check for TypeScript compilation errors
   - Verify all imports resolve correctly
   - Identify any build-time issues

### Phase 4: Report Results

8. **Generate validation report**:
   - List all checks performed
   - Show passed/failed status
   - Provide fix suggestions for failures
   - Indicate deployment readiness

## Validation Checks

### Required Checks

| Check | Severity | Description |
|-------|----------|-------------|
| webflow.json exists | Error | Required for CLI |
| Dependencies installed | Error | Required packages |
| Component files exist | Error | React + definition files |
| declareComponent called | Error | Required in .webflow.tsx |
| Build succeeds | Error | No compilation errors |

### Warning Checks

| Check | Severity | Description |
|-------|----------|-------------|
| Props have defaults | Warning | Better designer experience |
| SSR compatibility | Warning | May cause hydration issues |
| Styles imported | Warning | Styles may not appear |

### Info Checks

| Check | Severity | Description |
|-------|----------|-------------|
| Component count | Info | Number of components |
| Prop count | Info | Props per component |

## Examples

**User prompt:**
```
Check if my components are ready to deploy
```

**Response:**
```
🔍 Build Validation: My Component Library

Running pre-deployment checks...

---

## Project Structure

✅ webflow.json found
✅ library.name: "My Component Library"
✅ library.components: "./src/**/*.webflow.tsx"
✅ globals: "./src/globals.ts"

---

## Dependencies

✅ @webflow/webflow-cli: ^1.12.0
✅ @webflow/data-types: ^1.2.0
✅ @webflow/react: ^1.2.0
✅ react: ^18.2.0
✅ typescript: ^5.0.0

---

## Components Found (4)

### 1. Button ✅
- File: src/components/Button/Button.webflow.tsx
- Props: label (text), variant (variant), disabled (boolean)
- All props have defaults ✅
- SSR compatible ✅
- Styles imported ✅

### 2. Card ✅
- File: src/components/Card/Card.webflow.tsx
- Props: title (text), image (image), content (richText)
- All props have defaults ✅
- SSR compatible ✅
- Styles imported ✅

### 3. Modal ⚠️
- File: src/components/Modal/Modal.webflow.tsx
- Props: title (text), isOpen (boolean), content (slot)
- All props have defaults ✅
- ⚠️ SSR Issue: Uses `document.body` in render
  → Suggestion: Add `ssr: false` to options or wrap in useEffect
- Styles imported ✅

### 4. CartIcon ⚠️
- File: src/components/CartIcon/CartIcon.webflow.tsx
- Props: none
- ⚠️ Missing props - component has no editable properties
  → Suggestion: Consider adding props for designer customization
- ⚠️ Uses localStorage without SSR guard
  → Suggestion: Wrap in useEffect or useState initializer
- Styles imported ✅

---

## Build Test

✅ Build completed successfully
✅ No TypeScript errors
✅ No webpack errors

---

## Summary

| Category | Status |
|----------|--------|
| Project Structure | ✅ Pass |
| Dependencies | ✅ Pass |
| Components | ⚠️ 2 warnings |
| Build | ✅ Pass |

---

## Ready to Deploy: ⚠️ WITH WARNINGS

You can deploy, but consider fixing these issues:

1. **Modal SSR Issue**
   Add to Modal.webflow.tsx:
   ```typescript
   options: {
     ssr: false
   }
   ```

2. **CartIcon localStorage Usage**
   Update CartIcon.tsx:
   ```typescript
   const [count, setCount] = useState(() => {
     if (typeof window === "undefined") return 0;
     return parseInt(localStorage.getItem("cartCount") || "0");
   });
   ```

---

💡 To deploy: `npx webflow library share`
```

---

**Example: Build Failure**

```
🔍 Build Validation: My Component Library

Running pre-deployment checks...

---

## Project Structure

✅ webflow.json found

---

## Dependencies

❌ Missing: @webflow/react
   Fix: npm install --save-dev @webflow/react

---

## Build Test

❌ Build Failed

Error in src/components/Button/Button.webflow.tsx:
```
Module not found: Error: Can't resolve '@webflow/react'
```

---

## Summary

| Category | Status |
|----------|--------|
| Dependencies | ❌ 1 error |
| Build | ❌ Failed |

---

## Ready to Deploy: ❌ NO

Fix the following before deployment:

1. **Install missing dependency**
   ```bash
   npm install --save-dev @webflow/react
   ```

2. **Re-run validation**
   After installing, run this check again.
```

---

**Example: Bundle Too Large**

```
🔍 Build Validation: My Component Library

---


## Guidelines

### Validation Order

Run checks in this order for efficiency:

1. Project structure (fast, catches obvious issues)
2. Dependencies (medium, required for build)
3. Component analysis (medium, catches code issues)
4. Build test (slow, but required)

### SSR Detection Patterns

Look for these patterns that indicate SSR issues:

```typescript
// Direct usage (will break SSR)
window.innerWidth
document.getElementById
localStorage.getItem
navigator.userAgent
sessionStorage

// Safe patterns (in useEffect or state initializer)
useEffect(() => {
  // Browser APIs here are fine
}, []);

useState(() => {
  if (typeof window === "undefined") return default;
  return window.innerWidth;
});
```

### Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Can't resolve '@webflow/react'" | Missing dependency | `npm i -D @webflow/react` |
| "Cannot find module './Component'" | Wrong import path | Check relative paths |
| "Type 'X' is not assignable" | TypeScript error | Fix type mismatch |
| "Unexpected token" | Syntax error | Check JSX/TS syntax |
| "Maximum call stack" | Circular import | Break dependency cycle |

### Bundle Size Optimization

Quick wins for reducing bundle size:

1. **Use production build**: Ensure minification is enabled
2. **Tree-shake imports**: Import specific exports
3. **Replace heavy libraries**: moment → date-fns, lodash → lodash-es
4. **Lazy load**: Dynamic imports for heavy components
5. **Check for duplicates**: Multiple React versions, etc.
