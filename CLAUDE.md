# hksaperstein.github.io

Harrison's personal portfolio site (Astro 5 + Tailwind CSS 4, deployed to GitHub Pages
via GitHub Actions).

Before writing or editing any content that ships on the site — project write-ups in
`src/content/projects/`, homepage copy in `src/components/`, or similar — read `VOICE.md`
and match it. Site copy should read as something Harrison wrote, not AI-generated text.

## Layout

- `src/content/projects/*.md` — project write-ups (content collection; schema in
  `src/content.config.ts`)
- `src/pages/index.astro` — single-page homepage (hero, featured project, about, grid, skills)
- `src/pages/projects/[slug].astro` — project detail pages
- `public/assets/` — images, videos, models, schematics, resume (URLs are `/assets/...`)
- `scripts/` — CAD/SPICE asset-generation utilities (not part of the site build)

## Build

Node 26 (matches `.nvmrc` and the deploy workflow); on the Mac it's Homebrew's `node`.
Run `npm ci` after a fresh clone.

- `npm run build` — must pass before committing site changes
- `npm run dev` — local dev server
