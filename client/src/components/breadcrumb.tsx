import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import BookmarkStar from './bookmarkStar';
import './breadcrumb.less';
import { Bookmark } from '../constants/bookmarks';

export interface Props {
  icon?: string;
  links: Array<{ name: string, value?: string }>;
  bookmark?: Bookmark;
}

function Breadcrumb({icon, links, bookmark}: Props) {
  return (
    <ol className="breadcrumb">
      {icon && <i className={`fa ${icon} icon`} aria-hidden="true"/>}
      {links.map(
        (link, idx) => {
          if (link.value) {
            return <LinkContainer to={link.value} key={idx}>
              <li>
                <a>
                  {link.name}
                </a>
              </li>
            </LinkContainer>;
          } else {
            return <li key={idx}>{link.name}</li>;
          }
        }
      )}
      {bookmark && <BookmarkStar active={bookmark.active} callback={bookmark.callback}/>}
    </ol>
  );
}

export default Breadcrumb;
