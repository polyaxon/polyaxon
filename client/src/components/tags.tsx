import * as React from 'react';
import './tags.less';

export interface Props {
  tags: Array<string>;
}

function Tags({tags}: Props) {
  return (
    <div className="tags">
      {tags && tags.map(
        (tag, idx) =>
          <span key={idx} className="label label-tags">
            <i className="fa fa-tags icon" aria-hidden="true"/> {tag}
          </span>
      )}
    </div>
  );
}

export default Tags;
