import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import Polyaxonfile from '../polyaxonfile/polyaxonfile';
import { checkServerError, checkValidationError } from './utils';

export const ConfigSchema = Yup.string();

export const ConfigComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <Polyaxonfile
    content=""
    handleChange={(value: string) => {
      form.setFieldValue(field.name, value);
    }}
  />
);

export const ConfigField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'config');
  const hasValidationError = checkValidationError(props, 'config');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-sm-2 control-label">Config</label>
      <div className="col-sm-10">
        <Field name="config" component={ConfigComponent}/>
        {hasServerError && <div className="help-block">{errors.config}</div>}
        <ErrorMessage name="config">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );
};
