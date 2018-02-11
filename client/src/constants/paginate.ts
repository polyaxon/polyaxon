export const PAGE_SIZE = 30;

export function get_offset(page?: number): number | null {
  if (page == null || page <= 1) {
    return null;
  }
  return (page - 1) * PAGE_SIZE;
}

export function paginate(count: number): boolean {
  return count > PAGE_SIZE;
}

export function getNumPages(count: number): number {
  return Math.ceil(count / PAGE_SIZE);
}

export function paginateNext(currentPage: number, count: number): boolean {
  return currentPage < getNumPages(count);
}

export function paginatePrevious(currentPage: number): boolean {
  return currentPage > 1;
}
