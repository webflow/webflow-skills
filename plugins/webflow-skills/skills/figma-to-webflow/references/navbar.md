# Navbar

Read this before building a navigation bar.

Webflow's native Navbar component cannot be created via API/WHTML. WHTML can produce generic blocks with `w-*` class names, but not the real component JS/CSS. Build a semantic custom nav or ask the user to add the native element in Designer.

## Required Prompt

Ask which breakpoint should collapse to hamburger:

- 3-4 short links, no/short CTA: recommend mobile landscape (`767`) or mobile portrait (`479`).
- 5+ links, long labels, or prominent CTA: recommend tablet (`991`) so the bar does not crowd.

State the recommendation and reason, then use the user's choice.

## Structure

Build with custom tags so it is semantic and Designer-editable:

```html
<nav class="nav">
  <div class="nav-inner">
    <a class="nav-brand" href="/">...</a>
    <input type="checkbox" id="nav-toggle" class="nav-cb">
    <label for="nav-toggle" class="nav-burger">
      <span class="nav-burger-bar"></span>
      <span class="nav-burger-bar"></span>
      <span class="nav-burger-bar"></span>
    </label>
    <div class="nav-menu">
      <a class="nav-link" href="#">...</a>
      <a class="btn" href="#">CTA</a>
    </div>
  </div>
</nav>
```

The checkbox must be a previous sibling of `.nav-menu` so `:checked ~ .nav-menu` works. Order: brand, checkbox, burger, menu.

Make `.nav` or `.nav-inner` `position:relative` so the dropdown anchors to the bar. Use custom-tag `input` / `label`, not the Form Checkbox element, because Webflow's `.w-checkbox` wrapper breaks the sibling chain.

## Behavior

Keep desktop visual styling as normal Webflow classes. Put CSS-only responsive/toggle behavior in one component-scoped HtmlEmbed inside the nav root, so it travels if converted to a component. Do **not** use JavaScript for custom navbar behavior.

```html
<style>
  .nav-cb{ position:absolute; width:1px; height:1px; opacity:0; pointer-events:none; }
  .nav-burger{ display:none; }
  @media screen and (max-width:{BP}px){
    .nav-burger{ display:flex; flex-direction:column; row-gap:5px; cursor:pointer; }
    .nav-menu{
      display:none; position:absolute; top:100%; left:0; right:0;
      flex-direction:column; align-items:flex-start; row-gap:4px;
      padding:16px 24px; background:#fff; box-shadow:0 10px 24px rgba(0,0,0,.10);
    }
    .nav-cb:checked ~ .nav-menu{ display:flex; }
  }
</style>
```

Pure CSS is zero-JS and publish-safe. It does not set `aria-expanded` or close on outside click; tell the user that tradeoff rather than adding JavaScript.
