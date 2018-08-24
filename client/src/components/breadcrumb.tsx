import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { isDone } from '../constants/statuses';
import { ActionInterface } from '../interfaces/actions';
import { BookmarkInterface } from '../interfaces/bookmarks';
import Actions from './actions';
import BookmarkStar from './bookmarkStar';
import './breadcrumb.less';

export interface Props {
  icon?: string;
  links: Array<{ name: string, value?: string }>;
  bookmark?: BookmarkInterface;
  actions?: ActionInterface;
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
      {actions &&
      <Actions
        onDelete={actions.onDelete}
        onStop={actions.onStop}
        isRunning={actions.last_status ? !isDone(actions.last_status) : false}
        pullRight={true}
      />
      }
    </ol>
  );
}

export default Breadcrumb;
