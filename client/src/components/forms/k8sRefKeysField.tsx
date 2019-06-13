import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as React from 'react';

import { checkServerError, checkValidationError } from './validation';

export const KeysComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
    <textarea
      className="form-control"
      defaultValue={form.initialValues.keys.join('\n')}
      onChange={(event) => form.setFieldValue(field.name, event.target.value ? event.target.value.split('\n') : [])}
    />
);

export const K8SRefKeysField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'keys');
  const hasValidationError = checkValidationError(props, 'keys');
  const hasError = hasServerError || hasValidationError;

  const getK8SRef = () => (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="control-label">Keys</label>
      <Field
        name="keys"
        component={KeysComponent}
      />
      <span id="helpBlock" className="help-block">
        The K8S entity keys to expose, if no key is provided, Polyaxon will expose all keys of the resource.
      </span>
      <span id="helpBlock" className="help-block">
        Please provide comma separated values.
      </span>
      {hasServerError && <div className="help-block">{errors.keys}</div>}
      <ErrorMessage name="name">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );

  return getK8SRef();
};
