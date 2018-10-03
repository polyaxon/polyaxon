import * as React from 'react';

import './emptyList.less';

export function Empty(objectType: string, content: string) {
  return (
    <div className="row">
      <div className="col-md-offset-2 col-md-8">
        <div className="jumbotron jumbotron-action text-center empty-jumbotron">
          <h3>No {objectType} was found</h3>
          <div>{content}</div>
        </div>
      </div>
    </div>
  );
}
