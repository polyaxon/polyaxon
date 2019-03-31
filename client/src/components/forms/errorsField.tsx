import * as _ from 'lodash';
import * as React from 'react';

export const ErrorsField = (errors: any, classCss?: string) => {
  if (_.isArray(errors)) {
    return (
      <div className="has-error form-group">
        <div className={classCss ? classCss : `col-sm-12 col-lg-offset-2`}>
          {errors.map((error) => <div className="help-block" key={error}>{error}</div>)}
        </div>
      </div>
    );
  } else if (typeof errors === 'string') {
    return (
      <div className="has-error form-group">
        <div className="col-sm-10 col-lg-offset-2">
          <div className="help-block">{errors}</div>
        </div>
      </div>
    );
  }
  return null;
};
