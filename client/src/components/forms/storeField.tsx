import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';

import { K8SResourceModel } from '../../models/k8sResource';
import { getRequiredClass } from './utils';
import { checkValidationError } from './validation';

import './groupFields.less';

export interface StoreFieldSchema {
  type?: string;
  host_path?: string;
  volume_claim?: string;
  mount_path?: string;
  bucket?: string;
  k8s_secret?: string | number;
}

export function validateStore(value: StoreFieldSchema) {
  let error;

  if (!value.type) {
    return 'Store type is Required.';
  }
  if (['s3', 'azure', 'gcs'].indexOf(value.type) > -1) {
    if (!value.bucket) {
      error = 'Store type requires a bucket.';
    }
  } else {
    if (!value.mount_path) {
      error = 'Store type requires a mount path.';
    }
    if (!value.host_path && !value.volume_claim) {
      error = 'Store type requires a volume claim or host path to be provided.';
    }
    if (value.host_path && value.volume_claim) {
      error = 'Store type requires a volume claim or host path to be provided.';
    }
  }
  return error;
}

export interface StoreFieldProps extends FieldProps {
  secrets: K8SResourceModel[];
}

export const StoreComponent: React.FunctionComponent<StoreFieldProps> = (
  {
    field,
    form,
    secrets
  }) => (
  <div className="form-horizontal">
    <div className="form-group">
      <label className="col-sm-2 control-label">Type</label>
      <div className="col-sm-10">
        <select
          onChange={(event) => form.setFieldValue(field.name, {...field.value, type: event.target.value})}
          defaultValue={form.initialValues.store.type}
          className="form-control"
        >
          <option value="s3">S3</option>
          <option value="gcs">GCS</option>
          <option value="azure">Azure Blob</option>
          <option value="host_path">Host Path</option>
          <option value="volume_claim">Volume Claim</option>
        </select>
      </div>
    </div>
    {field.value.type === 'host_path' &&
    <div className="form-group">
      <label className="col-sm-2 control-label">Host Path</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          defaultValue={form.initialValues.store.host_path}
          onChange={(event) => form.setFieldValue(field.name, {...field.value, host_path: event.target.value})}
        />
      </div>
    </div>
    }
    {field.value.type === 'volume_claim' &&
    <div className="form-group">
      <label className="col-sm-2 control-label">Volume Claim</label>
      <div className="col-sm-10">
        <input
          type="text"
          className="form-control"
          defaultValue={form.initialValues.store.volume_claim}
          onChange={(event) => form.setFieldValue(field.name, {...field.value, volume_claim: event.target.value})}
        />
      </div>
    </div>
    }
    {(field.value.type === 'host_path' || field.value.type === 'volume_claim') &&
    <>
      <div className="form-group">
        <label className="col-sm-2 control-label">Mount Path</label>
        <div className="col-sm-10">
          <input
            type="text"
            className="form-control"
            defaultValue={form.initialValues.store.mount_path}
            onChange={(event) => form.setFieldValue(field.name, {...field.value, mount_path: event.target.value})}
          />
        </div>
      </div>
      <div className="form-group">
        <label className="col-sm-2 control-label">Read Only</label>
        <div className="col-sm-10">
          <select
            name="read_only"
            className="form-control"
            defaultValue={form.initialValues.store.read_only || 'false'}
            onChange={(event) => form.setFieldValue(field.name, {...field.value, read_only: event.target.value})}
          >
            <option value="true">True</option>
            <option value="false">False</option>
          </select>
        </div>
      </div>
    </>
    }
    {['s3', 'azure', 'gcs'].indexOf(field.value.type) > -1 &&
    <>
      <div className="form-group">
        <label className="col-sm-2 control-label">Bucket</label>
        <div className="col-sm-10">
          <input
            type="text"
            className="form-control"
            name="bucket"
            defaultValue={form.initialValues.store.bucket}
            onChange={(event) => form.setFieldValue(field.name, {...field.value, bucket: event.target.value})}
          />
        </div>
      </div>
      <div className="form-group">
        <label className="col-sm-2 control-label">Secret</label>
        <div className="col-sm-10">
          <select
            name="k8s_secret"
            className="form-control input-sm"
            defaultValue={form.initialValues.store.k8s_secret}
            onChange={(event) => form.setFieldValue(field.name, {...field.value, k8s_secret: event.target.value})}
          >
            <option value=""> No secret </option>
            {secrets.map(
              (secret: K8SResourceModel) => (
                <option
                  key={secret.uuid}
                  value={secret.id}
                  selected={form.initialValues.store.k8s_secret === secret.id}
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
    </>
    }
  </div>
);

export const checkStoreServer = (errors: any) => {
  const fields = ['type', 'bucket', 'host_path', 'volume_claim', 'mount_path', 'read_only'];
  return _.isObject(errors) && fields.filter((field: string) => field in errors).length > 0;
};

export const StoreField = (props: FormikProps<{}>, errors: any, secrets: K8SResourceModel[]) => {
  const hasServerError = checkStoreServer(errors);
  const hasValidationError = checkValidationError(props, 'store');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group group-fields`}>
      <label className={`control-label ${getRequiredClass(true)}`}>Store</label>
      <Field
        name="store"
        secrets={secrets}
        component={StoreComponent}
        validate={(value: StoreFieldSchema) => validateStore(value)}
      />
      {hasServerError &&
      <div className="help-block">
        {'type' in errors && <span>{errors.type}</span>}
        {'bucket' in errors && <span>{errors.bucket}</span>}
        {'k8s_secret' in errors && <span>{errors.k8s_secret}</span>}
        {'host_path' in errors && <span>{errors.host_path}</span>}
        {'volume_claim' in errors && <span>{errors.volume_claim}</span>}
        {'mount_path' in errors && <span>{errors.mount_path}</span>}
        {'read_only' in errors && <span>{errors.read_only}</span>}
      </div>
      }
      <ErrorMessage name="store">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );
};
