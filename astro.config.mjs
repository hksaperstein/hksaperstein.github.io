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
