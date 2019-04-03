import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as React from 'react';
import * as Yup from 'yup';

import Polyaxonfile from '../polyaxonfile/polyaxonfile';
import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

export const ConfigSchema = Yup.string();

export const getConfig = (config: string): { [key: string]: any } => {
  return jsYaml.safeLoad(config);
};

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

export const ConfigField = (props: FormikProps<{}>, errors: any, isRequired: boolean = false) => {
  const hasServerError = checkServerError(errors, 'config');
  const hasValidationError = checkValidationError(props, 'config');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Config</label>
      <Field name="config" component={ConfigComponent}/>
      {hasServerError && <div className="help-block">{errors.config}</div>}
      <ErrorMessage name="config">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
