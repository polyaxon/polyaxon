import { isTrue } from '../constants/utils';
import { BookmarkInterface } from '../interfaces/bookmarks';

export const getBookmark = (bookmarked: boolean,
                            bookmarkCb: () => any,
                            unbookmarkCb: () => any): BookmarkInterface => {
  return {
    active: isTrue(bookmarked),
    callback: isTrue(bookmarked) ? unbookmarkCb : bookmarkCb
  };
};
