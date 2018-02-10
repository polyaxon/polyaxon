export const PAGE_SIZE = 30;

export function get_offset(page?: number): number | null {
  if (page == null || page <= 1) {
    return null;
  }
  return (page - 1) * PAGE_SIZE;
}
