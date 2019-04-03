import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as React from 'react';

import { BuildFieldSchema, validateBuild } from './buildField';
import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

import './configField.less';

export interface RunFieldSchema extends BuildFieldSchema {
  command?: string;
}

export function validateRun(value: RunFieldSchema, isRequired: boolean) {
  let error = validateBuild(value || {}, isRequired);
  if (error) {
    return error;
  }

  if (isRequired && !value.command) {
    error = 'Required.';
  }
  return error;
}

export const RunComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <div className="form-horizontal">
    <div className="form-group">
      <label htmlFor="inputEmail3" className="col-sm-2 control-label">Docker Image</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          onChange={(event) => form.setFieldValue(field.name, {...field.value, image: event.target.value})}
        />
      </div>
    </div>
    <div className="form-group">
      <label htmlFor="inputPassword3" className="col-sm-2 control-label">Build steps</label>
      <div className="col-sm-10">
        <textarea
          className="form-control"
          onChange={(event) => form.setFieldValue(
            field.name,
            {...field.value, build_steps: event.target.value.split('\n')})}
        />
        <span id="helpBlock" className="help-block">
        Use new line to make different build steps.
        </span>
      </div>
    </div>
    <div className="form-group">
      <label htmlFor="inputEmail3" className="col-sm-2 control-label">Command</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          onChange={(event) => form.setFieldValue(field.name, {...field.value, command: event.target.value})}
        />
      </div>
    </div>
  </div>
);

export const RunField = (props: FormikProps<{}>, errors: any, isRequired: boolean, defaultImage?: string) => {
  const hasServerError = checkServerError(errors, 'config');
  const hasValidationError = checkValidationError(props, 'run');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group config-field`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Config</label>
      <Field
        name="run"
        component={RunComponent}
        validate={(value: RunFieldSchema) => validateRun(value, isRequired)}
      />
      {defaultImage &&
      <span id="helpBlock" className="help-block">
        If left empty it will use the default <code>{defaultImage}</code>
      </span>
      }
      {hasServerError && <div className="help-block">{errors.config}</div>}
      <ErrorMessage name="run">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
