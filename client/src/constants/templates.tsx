import * as React from 'react';

export function noObjectListComponent(isCurrentUser: boolean, objectType: string, image: string, command?: string) {
  return (
    <div className="row">
      <div className="col-md-offset-2 col-md-8">
        <div className="jumbotron jumbotron-action text-center">
          <h3>No {objectType} was found</h3>
          <img src={`/static/images/${image}.svg`} alt={image} className="empty-icon"/>
          {command && isCurrentUser &&
          <div>
            You can start a new {objectType} by using CLI: <b> {command} </b>
          </div>
          }
        </div>
      </div>
    </div>
  );
}
