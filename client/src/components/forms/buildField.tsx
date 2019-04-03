import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';

import './configField.less';

import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

export interface BuildFieldSchema {
  image?: string;
  build_steps?: string[];
}

export function validateBuild(value: BuildFieldSchema, isRequired: boolean) {
  const buildSteps = value.build_steps ? value.build_steps.filter((s: string) => !_.isNil(s) && s) : [];
  let error;
  if (isRequired && !value.image && !buildSteps.length) {
    error = 'Required.';
  }
  if (value && value.image && /\s/.test(value.image)) {
    error = 'Docker image is not a valid slug.';
  }
  if (value && buildSteps.length && !value.image) {
    error = 'Docker image is required when build steps are provided.';
  }
  return error;
}

export const BuildComponent: React.FunctionComponent<FieldProps> = (
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
  </div>
);

export const BuildField = (props: FormikProps<{}>, errors: any, isRequired: boolean, defaultImage?: string) => {
  const hasServerError = checkServerError(errors, 'config');
  const hasValidationError = checkValidationError(props, 'build');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group config-field`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Config</label>
      <Field
        name="build"
        component={BuildComponent}
        validate={(value: BuildFieldSchema) => validateBuild(value, isRequired)}
      />
      {defaultImage &&
      <span id="helpBlock" className="help-block">
        If left empty it will use the default <code>{defaultImage}</code>
      </span>
      }
      {hasServerError && <div className="help-block">{errors.config}</div>}
      <ErrorMessage name="build">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
