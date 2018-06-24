import * as queryString from 'query-string';

export const PAGE_SIZE = 30;

export function getOffset(page?: number): number | null {
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

export function paginateNext(offset: number, count: number): boolean {
  return offset < count;
}

export function paginatePrevious(offset: number): boolean {
  return offset >= PAGE_SIZE;
}

export function getPaginatedSlice(list: Array<any>): Array<any> {
  let pieces = location.href.split('?');
  let offset = null;
  if (pieces.length > 1) {
    let search = queryString.parse(pieces[1]);
    offset = search.offset ? parseInt(search.offset, 10) : null;
  }
  let start = offset || 0;
  let end = start + PAGE_SIZE;
  return list.slice(start, end);
}
