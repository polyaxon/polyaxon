import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as React from 'react';
import * as Yup from 'yup';

import { BuildFieldSchema, GroupFieldSchema, RunFieldSchema } from '../forms';
import Polyaxonfile from '../polyaxonfile/polyaxonfile';
import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

export const ConfigSchema = Yup.string();

export const getConfigFromImage = (dockerImage: string, kind: string): { [key: string]: any } => {
  return {
    version: 1,
    kind,
    build: {image: dockerImage}
  };
};

export const getConfigFromBuild = (build: BuildFieldSchema, kind: string): { [key: string]: any } => {
  return kind === 'build'
    ? {
      version: 1,
      kind,
      ...build
    } :
    {
      version: 1,
      kind,
      build
    };
};

export const getConfigFromRun = (run: RunFieldSchema, kind: string): { [key: string]: any } => {
  return {
    version: 1,
    kind,
    build: {image: run.image, build_steps: run.build_steps},
    run: {cmd: run.command}
  };
};

export const getConfigFromGroup = (group: GroupFieldSchema, kind: string): { [key: string]: any } => {
  return {
    version: 1,
    kind,
    hptuning: group.hptuning,
    build: {image: group.image, build_steps: group.build_steps},
    run: {cmd: group.command}
  };
};

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
  const hasServerError = checkServerError(errors, 'content');
  const hasValidationError = checkValidationError(props, 'config');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className={`control-label ${getRequiredClass(isRequired)}`}>Config</label>
      <Field name="config" component={ConfigComponent}/>
      {hasServerError && <div className="help-block">{errors.content}</div>}
      <ErrorMessage name="config">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
