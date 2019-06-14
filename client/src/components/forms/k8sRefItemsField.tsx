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
      defaultValue={form.initialValues.items.join('\n')}
      onChange={(event) => form.setFieldValue(field.name, event.target.value ? event.target.value.split('\n') : [])}
    />
);

export const K8sRefItemsField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'items');
  const hasValidationError = checkValidationError(props, 'items');
  const hasError = hasServerError || hasValidationError;

  const getK8SRef = () => (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="control-label">Items</label>
      <Field
        name="items"
        component={KeysComponent}
      />
      <span id="helpBlock" className="help-block">
        The K8S entity items to expose, if no key is provided, Polyaxon will expose all items of the resource.
      </span>
      <span id="helpBlock" className="help-block">
        Use new line to make different build steps.
      </span>
      {hasServerError && <div className="help-block">{errors.items}</div>}
      <ErrorMessage name="name">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );

  return getK8SRef();
};
