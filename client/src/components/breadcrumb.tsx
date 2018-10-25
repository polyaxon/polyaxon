import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { BookmarkInterface } from '../interfaces/bookmarks';
import BookmarkStar from './bookmarkStar';

import './breadcrumb.less';

export interface Props {
  icon?: string;
  links: Array<{ name: string, value?: string }>;
  bookmark?: BookmarkInterface;
  actions?: React.ReactNode;
}

function Breadcrumb({icon, links, bookmark, actions}: Props) {
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
      {actions && actions}
    </ol>
  );
}

export default Breadcrumb;
