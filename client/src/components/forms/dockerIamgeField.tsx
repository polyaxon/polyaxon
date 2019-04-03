import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

export const DockerImageSchema = Yup.string()
  .min(2, 'Image name too Short.');

function validateDockerImage(value: string) {
  let error;
  if (value && /\s/.test(value)) {
    error = 'Docker image is not a valid slug.';
  }
  return error;
}

export const DockerImageField = (props: FormikProps<{}>,
                                 errors: any,
                                 defaultImage: string,
                                 isRequired: boolean = false) => {
  const hasServerError = checkServerError(errors, 'config');
  const hasValidationError = checkValidationError(props, 'dockerImage');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Docker Image</label>
      <Field
        type="text"
        name="dockerImage"
        className="form-control input-sm"
        validate={validateDockerImage}
      />
      <span id="helpBlock" className="help-block">
        If left empty it will use the default <code>{defaultImage}</code>
      </span>
      <div className="row">
        <div className="col-md-12">
          {hasServerError && <div className="help-block">{errors.config}</div>}
          <ErrorMessage name="dockerImage">
            {(errorMessage) => <div className="help-block">{errorMessage}</div>}
          </ErrorMessage>
        </div>
      </div>
    </div>
  );
};
