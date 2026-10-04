## Description

Removed the `@click.self="emit('close')"` behavior from all modals. This prevents modals from automatically closing when users click or interact outside the modal content area (the backdrop). This fix ensures users do not accidentally lose form progress (such as while filling out the 'Add Paper' modal) due to stray clicks or hovering off the modal.

Users must now explicitly dismiss dialogs using the dedicated close buttons ('X' or 'Cancel') included in the modal headers and footers.

## Changes Made
- Removed `@click.self` backdrop closing on `AddPaperModal.vue`
- Removed `@click.self` backdrop closing on `AddArticleModal.vue`
- Removed `@click.self` backdrop closing on `AdminLoginModal.vue`
- Removed `@click.self` backdrop closing on `ArticleDetailModal.vue`
- Removed `@click.self` backdrop closing on `PaperDetailModal.vue`
