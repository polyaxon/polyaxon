import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { checkServerError, checkValidationError } from './validation';

export const DescriptionSchema = Yup.string();

export const DescriptionField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'description');
  const hasValidationError = checkValidationError(props, 'description');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-sm-2 control-label">Description</label>
      <div className="col-sm-10">
        <Field
          type="text"
          name="description"
          placeholder="Description"
          className="form-control input-sm"
        />
        {hasServerError && <div className="help-block">{errors.description}</div>}
        <ErrorMessage name="description">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );
};
