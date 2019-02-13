import * as React from 'react';

import './emptyList.less';

export function EmptyArchives(isCurrentUser: boolean, objectType: string, image: string) {
  return (
    <div className="row">
      <div className="col-md-offset-2 col-md-8">
        <div className="jumbotron jumbotron-action text-center empty-jumbotron">
          <h3>No bookmarked {objectType}</h3>
          {image && isCurrentUser &&
          <img src={`/static/images/${image}.svg`} alt={image} className="empty-icon"/>
          }
        </div>
      </div>
    </div>
  );
}
