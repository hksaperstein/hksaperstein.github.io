// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://hksaperstein.github.io',
  integrations: [
    sitemap({
      filter: (page) =>
        page !== 'https://hksaperstein.github.io/projects/' &&
        page !== 'https://hksaperstein.github.io/projects/ar4-pickplace-rl/',
    }),
  ],
  redirects: {
    '/about': '/#about',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
