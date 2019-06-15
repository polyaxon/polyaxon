import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';

import { K8SResourceModel } from '../../models/k8sResource';
import { getRequiredClass } from './utils';
import { checkValidationError } from './validation';

import './groupFields.less';

export interface AccessFieldSchema {
  host: string;
  k8s_secret?: string | number;
}

export function validateAccess(value: AccessFieldSchema) {
  let error;
  if (!value.host) {
    error = 'Host is Required.';
  }
  return error;
}

export interface AccessFieldProps extends FieldProps {
  secrets: K8SResourceModel[];
}

export const AccessComponent: React.FunctionComponent<AccessFieldProps> = (
  {
    field,
    form,
    secrets
  }) => (
  <div className="form-horizontal">
    <div className="form-group">
      <label className="col-sm-2 control-label">Host</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          defaultValue={form.initialValues.access.host}
          onChange={(event) => form.setFieldValue(field.name, {...field.value, host: event.target.value})}
        />
      </div>
    </div>
    <div className="form-group">
      <label className="col-sm-2 control-label">Secret</label>
      <div className="col-sm-10">
        <select
          name="k8s_secret"
          className="form-control input-sm"
          defaultValue={form.initialValues.access.k8s_secret}
          onChange={(event) => form.setFieldValue(field.name, {...field.value, k8s_secret: event.target.value})}
        >
          <option value=""> No secret</option>
          {secrets.map(
            (secret: K8SResourceModel) => (
              <option
                key={secret.uuid}
                value={secret.id}
                selected={form.initialValues.access.k8s_secret === secret.id}
              >
                {secret.name}
              </option>)
          )}
        </select>
        <span id="helpBlock" className="help-block">
            If this storage requires access.
          </span>
      </div>
    </div>
  </div>
);

export const checkAccessServer = (errors: any) => {
  const fields = ['type', 'bucket', 'host_path', 'volume_claim', 'mount_path', 'read_only'];
  return _.isObject(errors) && fields.filter((field: string) => field in errors).length > 0;
};

export const AccessField = (props: FormikProps<{}>, errors: any, secrets: K8SResourceModel[]) => {
  const hasServerError = checkAccessServer(errors);
  const hasValidationError = checkValidationError(props, 'access');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group group-fields`}>
      <label className={`control-label ${getRequiredClass(true)}`}>Access</label>
      <Field
        name="access"
        secrets={secrets}
        component={AccessComponent}
        validate={(value: AccessFieldSchema) => validateAccess(value)}
      />
      {hasServerError &&
      <div className="help-block">
        {'host' in errors && <span>{errors.host}</span>}
        {'k8s_secret' in errors && <span>{errors.k8s_secret}</span>}
      </div>
      }
      <ErrorMessage name="access">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
