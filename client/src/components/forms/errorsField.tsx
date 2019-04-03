import * as _ from 'lodash';
import * as React from 'react';

export const ErrorsField = (errors: any) => {
  if (_.isArray(errors)) {
    return (
      <div className="has-error form-group">
        {errors.map((error) => <div className="help-block" key={error}>{error}</div>)}
      </div>
    );
  } else if (typeof errors === 'string') {
    return (
      <div className="has-error form-group">
        <div className="help-block">{errors}</div>
      </div>
    );
  }
  return null;
};
