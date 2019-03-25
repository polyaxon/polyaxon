import * as _ from 'lodash';
import * as React from 'react';

export const ErrorsField = (errors: any) => {
  if (_.isArray(errors)) {
    return (
      <div className="has-error form-group">
        <div className="col-sm-10 col-lg-offset-2">
          {errors.map((error) => <div className="help-block" key={error}>{errors}</div>)}
        </div>
      </div>
    );
  }
  return null;
};
