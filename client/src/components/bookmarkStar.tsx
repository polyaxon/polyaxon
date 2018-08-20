import * as React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

import './bookmarkStar.less';

export interface Props {
  active: boolean;
  callback?: () => any;
}

function BookmarkStar({active, callback}: Props) {
  const className = active ? 'icon-bookmark-active' : '';
  const tooltip = active ? 'Remove from bookmarks' : 'Add to bookmarks';
  return (
    <OverlayTrigger placement="bottom" overlay={<Tooltip id="tooltipId">{tooltip}</Tooltip>}>
      <span className={`icon-bookmark ${className}`}>
        <a onClick={callback}> <i className="fa fa-star" aria-hidden="true"/> </a>
      </span>
    </OverlayTrigger>
  );
}

export default BookmarkStar;
