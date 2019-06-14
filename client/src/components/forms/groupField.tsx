import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as React from 'react';

import { RunFieldSchema, validateRun } from './runField';
import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

import './groupFields.less';

export interface GroupFieldSchema extends RunFieldSchema {
  hptuning?: string;
}

export function validateGroup(value: GroupFieldSchema, isRequired: boolean) {
  let error = validateRun(value || {}, isRequired);
  if (error) {
    return error;
  }

  if (isRequired && !value.hptuning) {
    error = 'Required.';
  }
  if (value.hptuning) {
    try {
      jsYaml.safeLoad(value.hptuning);
    } catch (err) {
      error = 'The hptuning section is not a valid object.';
    }
  }
  return error;
}

export const GroupComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <div className="form-horizontal">
    <div className="form-group">
      <label className="col-sm-2 control-label">HPTuning</label>
      <div className="col-sm-10">
        <textarea
          className="form-control"
          onChange={(event) => form.setFieldValue(
            field.name,
            {...field.value, hptuning: event.target.value})}
        />
        <span id="helpBlock" className="help-block">
        Pleas provide a valid Yaml/Json
        </span>
      </div>
    </div>
    <div className="form-group">
      <label className="col-sm-2 control-label">Docker Image</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          onChange={(event) => form.setFieldValue(field.name, {...field.value, image: event.target.value})}
        />
      </div>
    </div>
    <div className="form-group">
      <label className="col-sm-2 control-label">Build steps</label>
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
      <label className="col-sm-2 control-label">Command</label>
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

export const GroupField = (props: FormikProps<{}>, errors: any, isRequired: boolean, defaultImage?: string) => {
  const hasServerError = checkServerError(errors, 'content');
  const hasValidationError = checkValidationError(props, 'hptuning');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group group-fields`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Config</label>
      <Field
        name="hptuning"
        component={GroupComponent}
        validate={(value: GroupFieldSchema) => validateGroup(value, isRequired)}
      />
      {defaultImage &&
      <span id="helpBlock" className="help-block">
        If left empty it will use the default <code>{defaultImage}</code>
      </span>
      }
      {hasServerError && <div className="help-block">{errors.content}</div>}
      <ErrorMessage name="hptuning">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
