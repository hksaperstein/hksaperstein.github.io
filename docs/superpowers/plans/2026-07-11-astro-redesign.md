# Jekyll → Astro Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Jekyll portfolio with an Astro 5 + Tailwind CSS 4 site: a single scrollable homepage (hero, about, featured project, project grid, skills) plus the six existing project write-ups as detail pages at their current URLs.

**Architecture:** Static Astro site, no client framework. Project write-ups live in an Astro content collection whose zod schema mirrors the existing Jekyll frontmatter, so the markdown files migrate nearly untouched. Client-side JS is limited to `@google/model-viewer` (on the three project pages with GLTF models) and a few lines pausing autoplay video under reduced motion. Deployed to GitHub Pages via GitHub Actions.

**Tech Stack:** Astro ^5, Tailwind CSS ^4 (via `@tailwindcss/vite`), `@tailwindcss/typography`, `@astrojs/sitemap`, `@google/model-viewer`. Node 22 (user-local install; system node is 18 and too old).

**Spec:** `docs/superpowers/specs/2026-07-11-site-redesign-design.md`

## Global Constraints

- **Node:** every `node`/`npm`/`npx` command in this plan MUST be prefixed with `export PATH="$HOME/.local/node22/bin:$PATH" &&` (installed in Task 1). System node is v18.19.1 and will fail.
- **Working directory:** repo root (`~/projects/hksaperstein.github.io`) for all commands.
- **Voice:** never rewrite the markdown body of any project write-up — migrate prose verbatim (`VOICE.md` rule). All new visitor-facing copy must be exactly the strings given in this plan; do not paraphrase or "improve" them.
- **No emoji in site copy. No Font Awesome.** Inline SVG only for GitHub/LinkedIn/Thingiverse marks.
- **Asset URLs:** everything stays under `/assets/...` — markdown and frontmatter reference these paths and must keep working unchanged.
- **`demo_url: "#"`** in frontmatter is a placeholder — render external links only when the value is present AND not `"#"`.
- Commit at the end of every task with the message given in the task.

---

### Task 1: Node 22 toolchain + Astro scaffold

**Files:**
- Create: `~/.local/node22/` (user-local Node, outside the repo)
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json`, `.nvmrc`, `src/styles/global.css`, `src/pages/index.astro` (placeholder)
- Modify: `.gitignore` (create if absent)

**Interfaces:**
- Produces: working `npm run build` → `dist/`; Tailwind theme tokens `bg-bg`, `text-fg`, `text-muted`, `bg-card`, `border-line`, `text-accent` (used by every later task); `src/styles/global.css` imported by layouts.

- [ ] **Step 1: Install user-local Node 22**

```bash
mkdir -p ~/.local/node22 && curl -fsSL https://nodejs.org/dist/v22.17.0/node-v22.17.0-linux-x64.tar.xz | tar -xJ --strip-components=1 -C ~/.local/node22
export PATH="$HOME/.local/node22/bin:$PATH" && node --version
```
Expected: `v22.17.0`

- [ ] **Step 2: Write `package.json`**

```json
{
  "name": "hksaperstein.github.io",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "@astrojs/sitemap": "^3.4.0",
    "@google/model-viewer": "^4.1.0",
    "@tailwindcss/typography": "^0.5.16",
    "@tailwindcss/vite": "^4.1.0",
    "astro": "^5.10.0",
    "tailwindcss": "^4.1.0"
  }
}
```

- [ ] **Step 3: Write `.nvmrc`** containing exactly `22`

- [ ] **Step 4: Append to `.gitignore`** (create if it doesn't exist):

```
node_modules/
dist/
.astro/
```

- [ ] **Step 5: Write `astro.config.mjs`**

```js
// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://hksaperstein.github.io',
  integrations: [sitemap()],
  redirects: {
    '/about': '/#about',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
```

(Note: the `/projects` index redirect is NOT here — Astro rejects a redirect that collides with the `/projects/[slug]` route tree on some versions; it's a static page in Task 7 instead.)

- [ ] **Step 6: Write `tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "src/**/*"],
  "exclude": ["dist"]
}
```

- [ ] **Step 7: Write `src/styles/global.css`**

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";

:root {
  --bg: #fafaf9;
  --fg: #1c1917;
  --muted: #57534e;
  --card: #ffffff;
  --line: #e7e5e4;
  --accent: #c05621;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #121110;
    --fg: #e7e5e4;
    --muted: #a8a29e;
    --card: #1c1a19;
    --line: #2e2b29;
    --accent: #e08a4f;
  }
}

@theme inline {
  --color-bg: var(--bg);
  --color-fg: var(--fg);
  --color-muted: var(--muted);
  --color-card: var(--card);
  --color-line: var(--line);
  --color-accent: var(--accent);
}

html {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}

body {
  background-color: var(--bg);
  color: var(--fg);
}
```

- [ ] **Step 8: Write placeholder `src/pages/index.astro`**

```astro
---
import '../styles/global.css';
---
<h1 class="text-fg">placeholder</h1>
```

- [ ] **Step 9: Install and build**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm install && npm run build
```
Expected: build completes; `ls dist/index.html` succeeds. (Jekyll's `index.md` at repo root is ignored — Astro only reads `src/pages/`.)

- [ ] **Step 10: Commit**

```bash
git add package.json package-lock.json astro.config.mjs tsconfig.json .nvmrc .gitignore src/
git commit -m "Scaffold Astro 5 + Tailwind 4 alongside existing Jekyll site"
```

---

### Task 2: Move assets under `public/`

**Files:**
- Move: `assets/` → `public/assets/` (entire tree)
- Create: `public/robots.txt`

**Interfaces:**
- Produces: every existing `/assets/...` URL resolves from the built site (Astro copies `public/` into `dist/` verbatim). Later tasks reference `/assets/images/personal/headshot.jpeg`, `/assets/resume/Harrison_Saperstein_Resume_26.pdf`, project images/videos/models/schematics at unchanged paths.

- [ ] **Step 1: Move the tree with git**

```bash
mkdir -p public && git mv assets public/assets
```

- [ ] **Step 2: Delete Jekyll-only asset subtrees** (referenced only by the old Liquid layouts):

```bash
git rm -r public/assets/css public/assets/js
```

- [ ] **Step 3: Write `public/robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://hksaperstein.github.io/sitemap-index.xml
```

(The old Jekyll `robots.txt` lives in `_site/` which is removed in Task 8.)

- [ ] **Step 4: Build and verify assets are served**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && ls dist/assets/images/personal/headshot.jpeg dist/assets/resume/Harrison_Saperstein_Resume_26.pdf dist/robots.txt
```
Expected: all three paths listed, no error.

- [ ] **Step 5: Commit**

```bash
git add -A public assets
git commit -m "Move static assets under public/ for Astro"
```

---

### Task 3: Content collection + project markdown migration + bare detail pages

**Files:**
- Create: `src/content.config.ts`
- Move: `_projects/*.md` → `src/content/projects/*.md` (6 files, same basenames)
- Create: `src/pages/projects/[slug].astro` (bare version — full layout in Task 6)

**Interfaces:**
- Produces: collection `projects`; entry `id` = filename without extension (`6dof-robotic-arm`, `agentic-ai-experiments`, `ar4-pickplace-rl`, `dice-detection`, `ender-3`, `rgbw-keyboard`); schema fields exactly as below; URLs `/projects/<id>/`. `ar4-pickplace-rl` has `featured: true`.

- [ ] **Step 1: Write `src/content.config.ts`**

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const mediaItem = z.object({
  file: z.string(),
  section: z.string().optional(),
  description: z.string().optional(),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    categories: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    featured_image: z.string().optional(),
    github_url: z.string().optional(),
    thingiverse_url: z.string().optional(),
    demo_url: z.string().optional(),
    gallery: z.array(mediaItem).optional(),
    models: z.array(mediaItem).optional(),
    schematics: z.array(mediaItem).optional(),
    components: z
      .array(
        z.object({
          name: z.string(),
          quantity: z.number().optional(),
          description: z.string().optional(),
          link: z.string().optional(),
        }),
      )
      .optional(),
  }),
});

export const collections = { projects };
```

- [ ] **Step 2: Move the markdown and strip Jekyll-only keys**

```bash
mkdir -p src/content/projects && git mv _projects/*.md src/content/projects/
sed -i '/^layout: /d; /^interactive_plot: /d' src/content/projects/*.md
```

- [ ] **Step 3: Mark the featured project** — in `src/content/projects/ar4-pickplace-rl.md`, add a line `featured: true` directly after the `date:` line. Do not change anything else in the file.

- [ ] **Step 4: Write bare `src/pages/projects/[slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import '../../styles/global.css';

export async function getStaticPaths() {
  const projects = await getCollection('projects');
  return projects.map((project) => ({
    params: { slug: project.id },
    props: { project },
  }));
}

const { project } = Astro.props;
const { Content } = await render(project);
---

<h1>{project.data.title}</h1>
<Content />
```

- [ ] **Step 5: Build and verify all six URLs + schema**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && ls dist/projects/6dof-robotic-arm/index.html dist/projects/agentic-ai-experiments/index.html dist/projects/ar4-pickplace-rl/index.html dist/projects/dice-detection/index.html dist/projects/ender-3/index.html dist/projects/rgbw-keyboard/index.html
```
Expected: all six files listed. A schema error here means a frontmatter key doesn't match `content.config.ts` — fix the schema (not the content) unless it's one of the two Jekyll-only keys.

- [ ] **Step 6: Commit**

```bash
git add -A _projects src/content src/pages/projects
git commit -m "Migrate project write-ups into Astro content collection"
```

---

### Task 4: Base layout, nav, footer, site data

**Files:**
- Create: `src/layouts/Base.astro`, `src/components/Nav.astro`, `src/components/Footer.astro`, `src/data/site.ts`

**Interfaces:**
- Consumes: theme tokens from Task 1.
- Produces: `Base.astro` with props `{ title: string; description: string; ogImage?: string }` wrapping content in nav + `<main>` + footer; `SITE` object from `src/data/site.ts`.

- [ ] **Step 1: Write `src/data/site.ts`**

```ts
export const SITE = {
  name: 'Harrison Saperstein',
  url: 'https://hksaperstein.github.io',
  email: 'harrison.saperstein@gmail.com',
  github: 'https://github.com/hksaperstein',
  linkedin: 'https://linkedin.com/in/harrison-saperstein',
  thingiverse: 'https://www.thingiverse.com/hksaperstein',
  resume: '/assets/resume/Harrison_Saperstein_Resume_26.pdf',
  resumeFilename: 'hksaperstein_resume.pdf',
};
```

- [ ] **Step 2: Write `src/components/Nav.astro`**

```astro
---
import { SITE } from '../data/site';

const links = [
  { href: '/#about', label: 'About' },
  { href: '/#projects', label: 'Projects' },
  { href: '/#skills', label: 'Skills' },
];
---

<header class="sticky top-0 z-50 border-b border-line bg-bg/85 backdrop-blur">
  <nav class="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
    <a href="/" class="font-semibold tracking-tight">Harrison Saperstein</a>
    <div class="flex items-center gap-5 text-sm">
      {links.map((link) => (
        <a href={link.href} class="hidden text-muted transition-colors hover:text-fg sm:inline">{link.label}</a>
      ))}
      <a
        href={SITE.resume}
        download={SITE.resumeFilename}
        class="rounded-md border border-line px-3 py-1.5 font-medium transition-colors hover:border-accent hover:text-accent"
      >Resume</a>
    </div>
  </nav>
</header>
```

- [ ] **Step 3: Write `src/components/Footer.astro`**

```astro
---
import { SITE } from '../data/site';

const links = [
  { href: SITE.github, label: 'GitHub' },
  { href: SITE.linkedin, label: 'LinkedIn' },
  { href: SITE.thingiverse, label: 'Thingiverse' },
  { href: `mailto:${SITE.email}`, label: 'Email' },
  { href: SITE.resume, label: 'Resume' },
];
---

<footer class="border-t border-line">
  <div class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-6 py-10 text-sm text-muted">
    <p>© {new Date().getFullYear()} Harrison Saperstein</p>
    <div class="flex flex-wrap gap-5">
      {links.map((link) => (
        <a href={link.href} class="transition-colors hover:text-fg">{link.label}</a>
      ))}
    </div>
  </div>
</footer>
```

- [ ] **Step 4: Write `src/layouts/Base.astro`**

```astro
---
import '../styles/global.css';
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';
import { SITE } from '../data/site';

interface Props {
  title: string;
  description: string;
  ogImage?: string;
}

const { title, description, ogImage } = Astro.props;
const canonical = new URL(Astro.url.pathname, SITE.url).href;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg" />
    <link rel="sitemap" href="/sitemap-index.xml" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    {ogImage && <meta property="og:image" content={new URL(ogImage, SITE.url).href} />}
  </head>
  <body class="min-h-screen antialiased">
    <Nav />
    <main>
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 5: Point the placeholder homepage at the layout** — replace `src/pages/index.astro` with:

```astro
---
import Base from '../layouts/Base.astro';
---

<Base title="Harrison Saperstein" description="A portfolio of my projects in robotics, machine learning, and 3D printing.">
  <h1 class="text-fg">placeholder</h1>
</Base>
```

- [ ] **Step 6: Build and verify**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && grep -c "Resume" dist/index.html && grep -c "og:title" dist/index.html
```
Expected: build succeeds; both grep counts ≥ 1.

- [ ] **Step 7: Commit**

```bash
git add src/layouts src/components src/data src/pages/index.astro
git commit -m "Add base layout with sticky nav, footer, and SEO head"
```

---

### Task 5: Homepage sections

**Files:**
- Create: `src/components/Hero.astro`, `src/components/AboutSection.astro`, `src/components/FeaturedProject.astro`, `src/components/ProjectCard.astro`, `src/components/ProjectGrid.astro`, `src/components/SkillsSection.astro`, `src/data/skills.ts`
- Modify: `src/pages/index.astro` (replace placeholder)

**Interfaces:**
- Consumes: `Base.astro` (Task 4), collection `projects` (Task 3), theme tokens (Task 1).
- Produces: the finished homepage. `ProjectCard.astro` takes prop `{ project: CollectionEntry<'projects'> }` and is reused nowhere else at launch.

**Copy rule reminder: the strings below ship verbatim.**

- [ ] **Step 1: Write `src/data/skills.ts`** (data copied exactly from the old homepage)

```ts
export const SKILLS = [
  { category: 'Robotics', tags: ['ROS', 'Kinematics', 'Path Planning', 'SLAM'] },
  { category: 'AI/ML', tags: ['TensorFlow', 'OpenCV', 'Agentic AI', 'Claude Code'] },
  { category: 'Programming', tags: ['Python', 'C/C++', 'MATLAB', 'JavaScript'] },
  { category: 'CAD/Design', tags: ['SolidWorks', 'Fusion 360', '3D Printing', 'KiCad'] },
  { category: 'Electronics', tags: ['Arduino', 'ESP32', 'PCB Design', 'Sensors'] },
];
```

- [ ] **Step 2: Write `src/components/Hero.astro`**

```astro
---
import { SITE } from '../data/site';
---

<section class="mx-auto max-w-5xl px-6 pt-24 pb-20 sm:pt-32">
  <p class="text-sm font-medium tracking-widest text-accent uppercase">Robotics Engineer</p>
  <h1 class="mt-3 text-4xl font-bold tracking-tight sm:text-6xl">Harrison Saperstein</h1>
  <p class="mt-4 max-w-xl text-lg text-muted">Projects and Problems</p>
  <div class="mt-8 flex flex-wrap gap-3">
    <a
      href={SITE.resume}
      download={SITE.resumeFilename}
      class="rounded-md bg-accent px-4 py-2 font-medium text-white transition-opacity hover:opacity-90"
    >Resume</a>
    <a href={SITE.github} class="rounded-md border border-line px-4 py-2 font-medium transition-colors hover:border-accent hover:text-accent">GitHub</a>
    <a href={SITE.linkedin} class="rounded-md border border-line px-4 py-2 font-medium transition-colors hover:border-accent hover:text-accent">LinkedIn</a>
  </div>
</section>
```

- [ ] **Step 3: Write `src/components/AboutSection.astro`** — the two paragraphs below are final copy (condensed from the old about page, reusing Harrison's own phrasing):

```astro
<section id="about" class="scroll-mt-16 border-t border-line">
  <div class="mx-auto grid max-w-5xl gap-10 px-6 py-20 sm:grid-cols-[1fr_240px]">
    <div>
      <h2 class="text-2xl font-bold tracking-tight">About</h2>
      <div class="mt-5 space-y-4 text-muted">
        <p>
          Hi, I'm Harrison (Harry) Saperstein. I graduated from WPI with my MS/BS in Robotics
          Engineering in 2021. WPI introduced me to what it means to be robotic, and somewhere
          between solving for the kinematics of serial manipulators and watching them actually
          move, I grew an itch that's been hard to satisfy ever since.
        </p>
        <p>
          When I step away from a project — stuck, hyperfocused to my own detriment, or just
          needing inspiration — I'm skiing, golfing, or watching Boston sports with a maker
          video queued up next. This site is where I scratch the itch: solving problems, making
          robots move, and continuing to grow as an engineer.
        </p>
      </div>
    </div>
    <img
      src="/assets/images/personal/headshot.jpeg"
      alt="Harrison Saperstein"
      width="240"
      height="240"
      loading="lazy"
      class="h-56 w-56 justify-self-center rounded-2xl object-cover sm:justify-self-end"
    />
  </div>
</section>
```

- [ ] **Step 4: Write `src/components/FeaturedProject.astro`**

```astro
---
import { getCollection } from 'astro:content';

const [featured] = await getCollection('projects', (p) => p.data.featured);
---

{
  featured && (
    <section class="mx-auto max-w-5xl px-6 pb-20">
      <div class="overflow-hidden rounded-2xl border border-line bg-card sm:grid sm:grid-cols-2">
        <video
          autoplay
          muted
          loop
          playsinline
          preload="metadata"
          class="h-full w-full object-cover"
          src="/assets/videos/projects/ar4-pickplace-rl/ar4_pickplace_perception.mp4"
        />
        <div class="p-8">
          <div class="flex flex-wrap gap-2">
            {featured.data.categories.map((category) => (
              <span class="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">{category}</span>
            ))}
          </div>
          <h3 class="mt-4 text-2xl font-bold tracking-tight">
            <a href={`/projects/${featured.id}/`} class="hover:text-accent">{featured.data.title}</a>
          </h3>
          <p class="mt-3 text-muted">{featured.data.description}</p>
          <a href={`/projects/${featured.id}/`} class="mt-6 inline-block font-medium text-accent hover:underline">
            Read the write-up →
          </a>
        </div>
      </div>
    </section>
  )
}

<script>
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll<HTMLVideoElement>('video[autoplay]').forEach((video) => {
      video.removeAttribute('autoplay');
      video.pause();
      video.setAttribute('controls', '');
    });
  }
</script>
```

- [ ] **Step 5: Write `src/components/ProjectCard.astro`**

```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  project: CollectionEntry<'projects'>;
}

const { project } = Astro.props;
const href = `/projects/${project.id}/`;
---

<a
  href={href}
  class="group overflow-hidden rounded-2xl border border-line bg-card transition-transform duration-150 hover:-translate-y-0.5 hover:border-accent motion-reduce:transition-none motion-reduce:hover:translate-y-0"
>
  {
    project.data.featured_image ? (
      <img
        src={project.data.featured_image}
        alt={project.data.title}
        loading="lazy"
        class="aspect-video w-full object-cover"
      />
    ) : (
      <div class="flex aspect-video w-full items-center justify-center bg-bg text-sm tracking-widest text-muted uppercase">
        {project.data.categories[0] ?? 'Project'}
      </div>
    )
  }
  <div class="p-5">
    <div class="flex flex-wrap gap-2">
      {project.data.categories.slice(0, 2).map((category) => (
        <span class="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">{category}</span>
      ))}
    </div>
    <h3 class="mt-3 font-semibold tracking-tight group-hover:text-accent">{project.data.title}</h3>
    <p class="mt-2 line-clamp-2 text-sm text-muted">{project.data.description}</p>
  </div>
</a>
```

- [ ] **Step 6: Write `src/components/ProjectGrid.astro`** (all non-featured projects, newest first)

```astro
---
import { getCollection } from 'astro:content';
import ProjectCard from './ProjectCard.astro';

const projects = (await getCollection('projects', (p) => !p.data.featured)).sort(
  (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
);
---

<section id="projects" class="scroll-mt-16 border-t border-line">
  <div class="mx-auto max-w-5xl px-6 py-20">
    <h2 class="text-2xl font-bold tracking-tight">Projects</h2>
    <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {projects.map((project) => <ProjectCard project={project} />)}
    </div>
  </div>
</section>
```

- [ ] **Step 7: Write `src/components/SkillsSection.astro`**

```astro
---
import { SKILLS } from '../data/skills';
---

<section id="skills" class="scroll-mt-16 border-t border-line">
  <div class="mx-auto max-w-5xl px-6 py-20">
    <h2 class="text-2xl font-bold tracking-tight">Skills</h2>
    <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {
        SKILLS.map((group) => (
          <div class="rounded-2xl border border-line bg-card p-5">
            <h3 class="font-semibold tracking-tight">{group.category}</h3>
            <div class="mt-3 flex flex-wrap gap-2">
              {group.tags.map((tag) => (
                <span class="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">{tag}</span>
              ))}
            </div>
          </div>
        ))
      }
    </div>
  </div>
</section>
```

- [ ] **Step 8: Replace `src/pages/index.astro`**

```astro
---
import Base from '../layouts/Base.astro';
import Hero from '../components/Hero.astro';
import AboutSection from '../components/AboutSection.astro';
import FeaturedProject from '../components/FeaturedProject.astro';
import ProjectGrid from '../components/ProjectGrid.astro';
import SkillsSection from '../components/SkillsSection.astro';
---

<Base
  title="Harrison Saperstein — Robotics Engineer"
  description="A portfolio of my projects in robotics, machine learning, and 3D printing."
  ogImage="/assets/images/projects/ar4-pickplace-rl/featured.jpg"
>
  <Hero />
  <FeaturedProject />
  <AboutSection />
  <ProjectGrid />
  <SkillsSection />
</Base>
```

(Order note: featured spotlight sits directly under the hero, about follows — the strongest work is visible within the first scroll.)

- [ ] **Step 9: Build and verify sections**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && grep -o 'id="about"\|id="projects"\|id="skills"\|ar4_pickplace_perception' dist/index.html | sort | uniq -c
```
Expected: each of the four patterns appears at least once; exactly one `<video` in `dist/index.html`; the project grid contains 5 cards (`grep -c 'class="group' dist/index.html` → 5).

- [ ] **Step 10: Commit**

```bash
git add src/components src/data src/pages/index.astro
git commit -m "Build single-page homepage: hero, featured spotlight, about, grid, skills"
```

---

### Task 6: Full project detail pages

**Files:**
- Create: `src/components/Gallery.astro`, `src/components/ModelsSection.astro`, `src/components/SchematicsSection.astro`, `src/components/ComponentsSection.astro`
- Modify: `src/pages/projects/[slug].astro` (replace bare version)

**Interfaces:**
- Consumes: `Base.astro`, collection schema from Task 3 (`gallery`/`models`/`schematics`/`components` shapes).
- Produces: finished `/projects/<slug>/` pages.

- [ ] **Step 1: Write `src/components/Gallery.astro`** — groups items by `section` (first-seen order, matching the old Jekyll grouping), videos for `.mp4`/`.webm`, figure captions:

```astro
---
interface GalleryItem {
  file: string;
  section?: string;
  description?: string;
}

interface Props {
  items: GalleryItem[];
}

const { items } = Astro.props;

const groups = new Map<string, GalleryItem[]>();
for (const item of items) {
  const key = item.section ?? '';
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key)!.push(item);
}

const isVideo = (file: string) => /\.(mp4|webm)$/i.test(file);
---

<section class="mt-12">
  <h2 class="text-2xl font-bold tracking-tight">Gallery</h2>
  {
    [...groups.entries()].map(([section, groupItems]) => (
      <div class="mt-8">
        {section && <h3 class="text-lg font-semibold tracking-tight">{section}</h3>}
        <div class="mt-4 grid gap-6 sm:grid-cols-2">
          {groupItems.map((item) => (
            <figure class="overflow-hidden rounded-2xl border border-line bg-card">
              {isVideo(item.file) ? (
                <video controls preload="metadata" class="w-full" src={item.file} />
              ) : (
                <img src={item.file} alt={item.description ?? ''} loading="lazy" class="w-full" />
              )}
              {item.description && (
                <figcaption class="border-t border-line p-4 text-sm text-muted">{item.description}</figcaption>
              )}
            </figure>
          ))}
        </div>
      </div>
    ))
  }
</section>
```

- [ ] **Step 2: Write `src/components/ModelsSection.astro`** (`@google/model-viewer` is imported in a client script here, so its JS only loads on pages that render this component):

```astro
---
interface Props {
  items: { file: string; description?: string }[];
}

const { items } = Astro.props;
---

<section class="mt-12">
  <h2 class="text-2xl font-bold tracking-tight">3D Models</h2>
  <div class="mt-4 grid gap-6 sm:grid-cols-2">
    {
      items.map((item) => (
        <figure class="overflow-hidden rounded-2xl border border-line bg-card">
          <model-viewer
            src={item.file}
            alt={item.description ?? '3D model'}
            camera-controls
            auto-rotate
            style="width: 100%; height: 300px;"
          />
          {item.description && (
            <figcaption class="border-t border-line p-4 text-sm text-muted">{item.description}</figcaption>
          )}
        </figure>
      ))
    }
  </div>
</section>

<script>
  import '@google/model-viewer';
</script>
```

Note: `model-viewer` is a custom element unknown to Astro's TS checker; if `npm run build` complains about the JSX type, add a `src/env.d.ts` declaration:

```ts
declare namespace astroHTML.JSX {
  interface IntrinsicElements {
    'model-viewer': any;
  }
}
```

(`astro build` does not typecheck by default, so this is only needed if the build actually fails.)

- [ ] **Step 3: Write `src/components/SchematicsSection.astro`**

```astro
---
interface Props {
  items: { file: string; description?: string }[];
}

const { items } = Astro.props;
---

<section class="mt-12">
  <h2 class="text-2xl font-bold tracking-tight">Schematics</h2>
  <div class="mt-4 grid gap-6 sm:grid-cols-2">
    {
      items.map((item) => (
        <figure class="overflow-hidden rounded-2xl border border-line bg-card">
          <img src={item.file} alt={item.description ?? 'Schematic'} loading="lazy" class="w-full bg-white" />
          {item.description && (
            <figcaption class="border-t border-line p-4 text-sm text-muted">{item.description}</figcaption>
          )}
        </figure>
      ))
    }
  </div>
</section>
```

- [ ] **Step 4: Write `src/components/ComponentsSection.astro`**

```astro
---
interface Props {
  items: { name: string; quantity?: number; description?: string; link?: string }[];
}

const { items } = Astro.props;
---

<section class="mt-12">
  <h2 class="text-2xl font-bold tracking-tight">Components</h2>
  <ul class="mt-4 divide-y divide-line rounded-2xl border border-line bg-card">
    {
      items.map((item) => (
        <li class="flex flex-wrap items-baseline gap-x-3 gap-y-1 p-4">
          <span class="font-medium">
            {item.link ? (
              <a href={item.link} class="hover:text-accent">{item.name}</a>
            ) : (
              item.name
            )}
          </span>
          {item.quantity && <span class="text-sm text-muted">×{item.quantity}</span>}
          {item.description && <span class="text-sm text-muted">{item.description}</span>}
        </li>
      ))
    }
  </ul>
</section>
```

- [ ] **Step 5: Replace `src/pages/projects/[slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import Base from '../../layouts/Base.astro';
import Gallery from '../../components/Gallery.astro';
import ModelsSection from '../../components/ModelsSection.astro';
import SchematicsSection from '../../components/SchematicsSection.astro';
import ComponentsSection from '../../components/ComponentsSection.astro';

export async function getStaticPaths() {
  const projects = await getCollection('projects');
  return projects.map((project) => ({
    params: { slug: project.id },
    props: { project },
  }));
}

const { project } = Astro.props;
const { Content } = await render(project);
const { data } = project;

const externalLinks = [
  { url: data.github_url, label: 'GitHub' },
  { url: data.thingiverse_url, label: 'Thingiverse' },
  { url: data.demo_url, label: 'Demo' },
].filter((link) => link.url && link.url !== '#');

const formattedDate = data.date.toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  timeZone: 'UTC',
});
---

<Base title={`${data.title} — Harrison Saperstein`} description={data.description} ogImage={data.featured_image}>
  <article class="mx-auto max-w-3xl px-6 py-16">
    <a href="/#projects" class="text-sm text-muted transition-colors hover:text-fg">← All projects</a>

    <header class="mt-6">
      <div class="flex flex-wrap gap-2">
        {data.categories.map((category) => (
          <span class="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">{category}</span>
        ))}
      </div>
      <h1 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">{data.title}</h1>
      <p class="mt-3 text-lg text-muted">{data.description}</p>
      <div class="mt-4 flex flex-wrap items-center gap-4 text-sm text-muted">
        <time datetime={data.date.toISOString().slice(0, 10)}>{formattedDate}</time>
        {externalLinks.map((link) => (
          <a href={link.url} class="font-medium text-accent hover:underline">{link.label} ↗</a>
        ))}
      </div>
    </header>

    <div class="prose prose-stone dark:prose-invert mt-10 max-w-none">
      <Content />
    </div>

    {data.gallery && data.gallery.length > 0 && <Gallery items={data.gallery} />}
    {data.models && data.models.length > 0 && <ModelsSection items={data.models} />}
    {data.schematics && data.schematics.length > 0 && <SchematicsSection items={data.schematics} />}
    {data.components && data.components.length > 0 && <ComponentsSection items={data.components} />}

    <div class="mt-14 border-t border-line pt-8">
      <a href="/#projects" class="font-medium text-accent hover:underline">← All projects</a>
    </div>
  </article>
</Base>
```

- [ ] **Step 6: Build and verify the media-heavy pages**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build \
  && grep -c "<video" dist/projects/ar4-pickplace-rl/index.html \
  && grep -c "model-viewer" dist/projects/6dof-robotic-arm/index.html \
  && grep -c "Schematics" dist/projects/rgbw-keyboard/index.html
```
Expected: ar4 video count ≥ 5 (five mp4 gallery entries); model-viewer count ≥ 2; Schematics count ≥ 1.

- [ ] **Step 7: Commit**

```bash
git add src/components src/pages/projects src/env.d.ts 2>/dev/null; git add src/components src/pages/projects
git commit -m "Render full project detail pages: prose, gallery, models, schematics"
```

---

### Task 7: `/projects/` index redirect page

**Files:**
- Create: `src/pages/projects/index.astro`

**Interfaces:**
- Consumes: nothing new. `/about` redirect already exists via config (Task 1).
- Produces: `/projects/` → `/#projects` meta-refresh redirect (same mechanism Astro's config redirects emit; written as a page because a config redirect at `/projects` collides with the `[slug]` route directory).

- [ ] **Step 1: Write `src/pages/projects/index.astro`**

```astro
---
const target = '/#projects';
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Redirecting to projects</title>
    <meta http-equiv="refresh" content={`0;url=${target}`} />
    <meta name="robots" content="noindex" />
    <link rel="canonical" href="https://hksaperstein.github.io/#projects" />
  </head>
  <body>
    <a href={target}>Redirecting to projects…</a>
  </body>
</html>
```

- [ ] **Step 2: Build and verify both redirects**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && grep -l "http-equiv=\"refresh\"" dist/projects/index.html dist/about/index.html
```
Expected: both files listed.

- [ ] **Step 3: Commit**

```bash
git add src/pages/projects/index.astro
git commit -m "Redirect old /projects/ and /about/ URLs to homepage sections"
```

---

### Task 8: Remove Jekyll, update repo docs

**Files:**
- Delete: `_config.yml`, `Gemfile`, `Gemfile.lock`, `_layouts/`, `_includes/`, `_sass/`, `_site/`, `vendor/`, `theme.json`, `3d-model-test.html`, `index.md`, `docs/about.md`, `docs/projects.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
- Modify: `README.md`, `CLAUDE.md`

**Interfaces:**
- Consumes: all content already migrated (Tasks 3, 5).
- Produces: a repo where Astro is the only site toolchain. `scripts/` (CAD/SPICE utilities) and `docs/superpowers/` are kept.

- [ ] **Step 1: Remove Jekyll files**

```bash
git rm -r --quiet _config.yml Gemfile Gemfile.lock _layouts _includes _sass _site theme.json 3d-model-test.html index.md docs/about.md docs/projects.md CHANGELOG.md CONTRIBUTING.md
git rm -r --quiet --cached vendor 2>/dev/null; rm -rf vendor
```
(`vendor/` is bundler output; it may or may not be tracked — the second line handles both.)

- [ ] **Step 2: Replace `README.md`**

````markdown
# hksaperstein.github.io

My portfolio site — robotics, machine learning, and 3D-printing projects.

Built with [Astro](https://astro.build) and Tailwind CSS. Deployed to GitHub Pages by
GitHub Actions on every push to `main`.

## Development

Requires Node 22 (`.nvmrc`).

```sh
npm install
npm run dev      # local dev server
npm run build    # static build into dist/
npm run preview  # serve the build locally
```

Project write-ups live in `src/content/projects/*.md`; static assets in `public/assets/`.
````

- [ ] **Step 3: Replace `CLAUDE.md`**

```markdown
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

Node 22 required (system node is too old). If `node --version` is < 20, use the local
install: `export PATH="$HOME/.local/node22/bin:$PATH"`.

- `npm run build` — must pass before committing site changes
- `npm run dev` — local dev server
```

- [ ] **Step 4: Full build still green**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && ls dist/index.html
```
Expected: build succeeds.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "Remove Jekyll toolchain; Astro is now the only site build"
```

---

### Task 9: GitHub Actions deploy workflow

**Files:**
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Produces: CI deploy to GitHub Pages on push to `main`. Requires a one-time manual repo setting change (flagged to Harrison; NOT done by the implementer): Settings → Pages → Source → "GitHub Actions".

- [ ] **Step 1: Write `.github/workflows/deploy.yml`**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Build with Astro
        uses: withastro/action@v3
        with:
          node-version: 22

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Validate YAML parses**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && node -e "const yaml=require('yaml');const fs=require('fs');yaml.parse(fs.readFileSync('.github/workflows/deploy.yml','utf8'));console.log('yaml ok')" 2>/dev/null || python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deploy.yml')); print('yaml ok')"
```
Expected: `yaml ok`

- [ ] **Step 3: Commit**

```bash
git add .github
git commit -m "Deploy to GitHub Pages via Actions on push to main"
```

---

### Task 10: Link check + final verification

**Files:**
- Create: `scripts/check-links.mjs`

**Interfaces:**
- Consumes: the finished `dist/` build.
- Produces: a repeatable internal-link checker; a fully verified build.

- [ ] **Step 1: Write `scripts/check-links.mjs`**

```js
// Checks that every root-relative href/src in dist/**/*.html resolves to a file in dist/.
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const DIST = 'dist';

function htmlFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return htmlFiles(path);
    return entry.name.endsWith('.html') ? [path] : [];
  });
}

const failures = [];
for (const file of htmlFiles(DIST)) {
  const html = readFileSync(file, 'utf8');
  for (const match of html.matchAll(/(?:href|src)="(\/[^"#?]*)/g)) {
    const url = decodeURIComponent(match[1]);
    if (url === '/') continue;
    const clean = url.replace(/\/$/, '');
    const candidates = [join(DIST, clean), join(DIST, clean, 'index.html')];
    if (!candidates.some((c) => existsSync(c) && statSync(c).isFile())) {
      failures.push(`${file}: ${url}`);
    }
  }
}

if (failures.length) {
  console.error(`BROKEN INTERNAL LINKS (${failures.length}):`);
  for (const failure of failures) console.error('  ' + failure);
  process.exit(1);
}
console.log('all internal links resolve');
```

- [ ] **Step 2: Build and run the checker**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run build && node scripts/check-links.mjs
```
Expected: `all internal links resolve`. If it reports broken links, fix the referencing component/markdown (or, for genuinely missing legacy assets, report them — do not delete content to silence the checker).

- [ ] **Step 3: Verify the six project URLs and redirects one final time**

```bash
ls dist/projects/6dof-robotic-arm/index.html dist/projects/agentic-ai-experiments/index.html dist/projects/ar4-pickplace-rl/index.html dist/projects/dice-detection/index.html dist/projects/ender-3/index.html dist/projects/rgbw-keyboard/index.html dist/about/index.html dist/sitemap-index.xml dist/robots.txt
```
Expected: all nine paths listed.

- [ ] **Step 4: Smoke-test the preview server**

```bash
export PATH="$HOME/.local/node22/bin:$PATH" && npm run preview > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:4321/ | grep -c "Harrison Saperstein"
curl -s http://localhost:4321/projects/ar4-pickplace-rl/ | grep -c "AR4"
pkill -f "astro preview"
```
Expected: both grep counts ≥ 1.

- [ ] **Step 5: Commit**

```bash
git add scripts/check-links.mjs
git commit -m "Add internal link checker; verify full Astro build"
```
