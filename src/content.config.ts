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
