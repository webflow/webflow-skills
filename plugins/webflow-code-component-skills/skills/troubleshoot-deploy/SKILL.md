---
name: troubleshoot-deploy
description: Debug deployment failures for Webflow Code Components. Analyzes error messages, identifies root causes, and provides specific fixes for common issues.
compatibility: Node.js 18+, React 18+, TypeScript, @webflow/webflow-cli
metadata:
  author: webflow
  version: "1.0"
---

# Troubleshoot Deploy

Debug and fix deployment issues for Webflow Code Components.

## When to Use This Skill

**Use when:**
- `webflow library share` failed with an error
- Components deployed but aren't working correctly
- User shares an error message from deployment
- Bundle or compilation errors occurred

**Do NOT use when:**
- Deployment hasn't been attempted yet (use deploy-guide instead)
- Validating before deployment (use build-validate instead)
- General code quality issues (use component-audit instead)

## Instructions

### Phase 1: Gather Information

1. **Get error details**:
   - Ask for exact error message
   - Request output from `npx webflow library share`
   - Check if `npx webflow library log` has additional info

2. **Understand context**:
   - First deploy or update?
   - Recent changes made?
   - Working previously?

### Phase 2: Diagnose

3. **Identify error category**:
   - Authentication errors
   - Build/compilation errors
   - Bundle size errors
   - Network/upload errors
   - Configuration errors

4. **Analyze root cause**:
   - Parse error message
   - Check common causes
   - Identify specific issue

### Phase 3: Provide Solution

5. **Give specific fix**:
   - Step-by-step resolution
   - Code examples if needed
   - Verification steps

6. **Prevent recurrence**:
   - Explain why it happened
   - Suggest preventive measures

## Common Error Reference

For detailed solutions to each error, see [references/ERROR_CATALOG.md](references/ERROR_CATALOG.md).

### Quick Reference

| Error | Category | Quick Fix |
|-------|----------|-----------|
| "Authentication failed" | Auth | Regenerate API token in Workspace Settings |
| "Insufficient permissions" | Auth | Check workspace role and token |
| "Module not found" | Build | `npm install --save-dev @webflow/react` |
| "TypeScript errors" | Build | Run `npx tsc --noEmit` to find error |
| "Unexpected token" | Build | Check file extension is `.tsx` |
| "Bundle size exceeds limit" | Bundle | Tree-shake imports, lazy load heavy components |
| "Component not rendering" | Runtime | Check SSR issues, browser console |
| "Styles not appearing" | Runtime | Import CSS in .webflow.tsx file |
| "webflow.json not found" | Config | Create webflow.json in project root |
| "No components found" | Config | Check glob pattern and file extension |

### Most Common Fixes

**Authentication:**
```bash
# Regenerate token, then:
export WEBFLOW_WORKSPACE_API_TOKEN=your-new-token
npx webflow library share
```

**Missing Dependencies:**
```bash
npm install --save-dev @webflow/webflow-cli @webflow/data-types @webflow/react
```

**SSR Issues:**
```typescript
// Wrap browser APIs in useEffect or disable SSR:
declareComponent(Component, { options: { ssr: false } });
```

**Missing Styles:**
```typescript
// In .webflow.tsx, import styles:
import "./Component.module.css";
```

## Debugging Commands

```bash
# Check recent deploy logs
npx webflow library log

# Verbose deploy output (shows detailed errors)
npx webflow library share --verbose

# Type check without deploying
npx tsc --noEmit
```

## Guidelines

### Error Analysis Process

1. **Read the full error message** - Often contains the solution
2. **Check the error category** - Auth, build, bundle, or runtime
3. **Look for file paths** - Points to exact location
4. **Check line numbers** - For code errors
5. **Search error message** - May be a known issue

### When to Escalate

If none of the solutions work:

1. Run `npx webflow library log` and save output
2. Check Webflow status page for outages
3. Gather: error message, webflow.json, package.json
4. Contact Webflow support with details
