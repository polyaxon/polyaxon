import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { checkServerError, checkValidationError } from '../forms/validation';

export const QuerySchema = Yup.string()
  .max(128, 'Name too Long.');

export const QueryField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'query');
  const hasValidationError = checkValidationError(props, 'query');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-sm-2 control-label">Query</label>
      <div className="col-sm-10">
        <Field
          type="text"
          name="query"
          className="form-control input-sm"
        />
        {hasServerError && <div className="help-block">{errors.query}</div>}
        <ErrorMessage name="query">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );
};
