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
- `src/components/ProjectDialog.astro` — each project's full write-up, shown as a modal on the
  homepage; link to `/#<slug>` to open one. `src/pages/projects/` only holds redirect stubs
  so old `/projects/<slug>/` URLs land on the right modal.
- `public/assets/` — images, videos, models, schematics, resume (URLs are `/assets/...`)
- `scripts/` — CAD/SPICE asset-generation utilities (not part of the site build)

## Branches

- `main` is live: every push deploys. Only finished projects live here.
- Each unfinished project has its own branch, `project/<slug>`, cut from `main` with just
  that project's write-up (and any links to it) added back. Work on the project there;
  when it's done, merge the branch into `main`. Pull `main` into the project branch now and
  then so the eventual merge stays small.

## Build

Node 26 (matches `.nvmrc` and the deploy workflow); on the Mac it's Homebrew's `node`.
Run `npm ci` after a fresh clone.

- `npm run build` — must pass before committing site changes
- `npm run dev` — local dev server
