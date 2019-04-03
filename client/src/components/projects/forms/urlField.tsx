import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { checkServerError, checkValidationError } from '../../forms';

export const UrlSchema = Yup.string().url();

export const UrlField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'url');
  const hasValidationError = checkValidationError(props, 'url');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
    <div className="col-md-10">
      <Field
        type="url"
        name="url"
        className="form-control input-sm"
        placeholder="Git url"
      />
      <ErrorMessage name="name">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
    </div>
  );
};
