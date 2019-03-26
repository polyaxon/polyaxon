import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { NameSlug } from '../../constants/helpTexts';
import { checkServerError, checkValidationError } from './validation';

export const NameSchema = Yup.string()
  .min(2, 'Name too Short.')
  .max(128, 'Name too Long.');

function validateName(value: string) {
  let error;
  if (value && !/^([-a-zA-Z0-9_]+)$/.test(value)) {
    error = 'Name is not a valid slug.';
  }
  return error;
}

export const NameField = (props: FormikProps<{}>, errors: any, col?: string) => {
  const hasServerError = checkServerError(errors, 'name');
  const hasValidationError = checkValidationError(props, 'name');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-sm-2 control-label">Name</label>
      <div className={col ? `col-sm-${col}` : `col-sm-5`}>
        <Field
          type="text"
          name="name"
          className="form-control input-sm"
          validate={validateName}
        />
        <span id="helpBlock" className="help-block">{NameSlug}</span>
        {hasServerError && <div className="help-block">{errors.name}</div>}
        <ErrorMessage name="name">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );
};
