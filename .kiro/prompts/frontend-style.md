Using [Zero-Latency Design System] as context, set up [Frontend Styling] for our project.

Documentation to read: 
- Current `frontend/tailwind.config.js`
- Current `frontend/src/App.css`
- Current `frontend/index.html` (for fonts)

First, install dependencies:
npm install clsx tailwind-merge lucide-react tailwindcss-animate
npm install -D tailwindcss postcss autoprefixer

Then create/modify these files:

1. UPDATE `frontend/index.html` with:
   - Google Fonts: 'Inter' (Sans) and 'Merriweather' (Serif)
   - `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">`

2. CREATE/OVERWRITE `frontend/tailwind.config.js` with:
   - `darkMode: ["class"]`
   - Extend `fontFamily`: `sans` ("Inter"), `serif` ("Merriweather")
   - Extend `colors`: mapped to CSS variables (background, foreground, card, primary, secondary, etc.)
   - Extend `borderRadius`: `lg: "0.75rem"`
   - Plugin: `tailwindcss-animate`

3. CREATE/OVERWRITE `frontend/src/App.css` with:
   - `@tailwind` directives
   - `:root` variables (Light Mode):
     - `--background`: 0 0% 100%
     - `--foreground`: 240 10% 3.9%
     - Standard shadcn/ui zinc palette for other tokens
   - `.dark` variables (Warm Charcoal Mode):
     - `--background`: 60 4% 15% (#262624)
     - `--foreground`: 50 8% 74% (#C2C0B6)
     - `--card`: 60 4% 17%
     - `--card-foreground`: 50 8% 74%
     - `--primary`: 32 60% 77% (Warm accent)
     - `--h2-foreground`: 50 6% 72% (#BEBCB2 - Highlight Color)
   - `@layer base` rules:
     - Global reset (`border-border`, `bg-background`, `text-foreground`)
     - Dark mode heading overrides: `.dark h1`...`.dark h6` { color: hsl(var(--h2-foreground)) }

4. CREATE `frontend/src/lib/utils.ts` with:
   - `cn` utility using `clsx` and `tailwind-merge`

5. CREATE/UPDATE Components (ui/card.tsx, ui/button.tsx, etc.):
   - Use `bg-secondary/50` for card backgrounds instead of `bg-white` to map correctly in dark mode.
   - Use `shadow-none` for a matte look.
   - Ensure text colors use `dark:text-[hsl(var(--h2-foreground))]` for highlighted headers/labels if not covered by global rules.
   - Ensure secondary text uses `text-gray-600 dark:text-gray-300` for readability.

Test requirements:

Unit tests (no external dependencies):
- None required for styling, rely on build verification.

Integration tests:
- None required.

E2E/Manual testing:
- Run `npm run dev`
- Toggle dark mode: Verify background is #262624, text is #C2C0B6.
- Check Headings: Verify serif font and #BEBCB2 color.
- Check Cards: Verify matte finish (no shadow) and distinct background from body.

All linting (npm run lint) must pass

When everything is green, let the user know we are ready to commit

Output format:
Summary: Scaffolded Zero-Latency Design System with Warm Charcoal Dark Mode.
Files created/modified: [list]
