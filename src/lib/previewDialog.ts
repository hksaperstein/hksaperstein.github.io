// Shared id format for project preview dialogs, so trigger elements (which may
// live outside the ProjectPreviewDialog component, e.g. ProjectSections rows)
// can point at the right dialog without duplicating the string format.
export function previewDialogId(idPrefix: string, projectId: string): string {
  return `project-preview-${idPrefix}-${projectId}`;
}
