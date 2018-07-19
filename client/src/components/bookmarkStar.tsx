import * as React from 'react';
import './bookmarkStar.less';

export interface Props {
  active: boolean;
  callback?: () => any;
}

function BookmarkStar({active, callback}: Props) {
  const className = active ? 'icon-bookmark-active' : '';
  return (
    <span className={`icon-bookmark ${className}`}>
      <a onClick={callback}> <i className="fa fa-star" aria-hidden="true"/> </a>
    </span>
  );
}

export default BookmarkStar;
