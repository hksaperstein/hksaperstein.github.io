// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://hksaperstein.github.io',
  integrations: [
    sitemap({
      // /projects/* are redirect stubs; the write-ups live in homepage modals.
      filter: (page) => !page.startsWith('https://hksaperstein.github.io/projects/'),
    }),
  ],
  redirects: {
    '/about': '/#about',
    '/projects': '/#projects',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
