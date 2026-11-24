// Projects live in modals on the homepage. A link to projectHref(slug) opens
// that project's dialog (ProjectDialog.astro handles the click and the hash).
export function projectHref(slug: string): string {
  return `/#${slug}`;
}

export function projectDialogId(slug: string): string {
  return `project-${slug}`;
}
