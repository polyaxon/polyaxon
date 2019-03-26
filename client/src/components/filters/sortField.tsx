import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { checkServerError, checkValidationError } from '../forms/validation';

export const SortSchema = Yup.string()
  .max(128, 'Name too Long.');

export const SortField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'sort');
  const hasValidationError = checkValidationError(props, 'sort');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-sm-2 control-label">Sort</label>
      <div className="col-sm-10">
        <Field
          type="text"
          name="sort"
          className="form-control input-sm"
        />
        {hasServerError && <div className="help-block">{errors.sort}</div>}
        <ErrorMessage name="sort">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );
};
