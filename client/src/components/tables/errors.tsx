import * as React from 'react';

export const Errors = (errors: any) => {
  return (
    <div className="row">
      <div className="col-md-offset-2 col-md-8">
        <div className="jumbotron jumbotron-action text-center empty-jumbotron">
          <h3>No result was found, an error occurred</h3>
          <div className="help-block has-error">{errors}</div>
        </div>
      </div>
    </div>
  );
};
