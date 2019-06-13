import { ErrorMessage, Field, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { getRequiredClass } from './utils';
import { checkServerError, checkValidationError } from './validation';

export const K8SRefSchema = Yup.string()
  .min(2, 'K8S Ref too Short.')
  .max(128, 'K8S Ref too Long.');

export const K8SRefField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'k8s_ref');
  const hasValidationError = checkValidationError(props, 'k8s_ref');
  const hasError = hasServerError || hasValidationError;

  const getK8SRef = () => (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className={`control-label ${getRequiredClass(true)}`}>K8S Ref</label>
      <Field
        type="text"
        name="k8s_ref"
        className="form-control input-sm"
      />
      <span id="helpBlock" className="help-block">The K8S entity reference name.</span>
      {hasServerError && <div className="help-block">{errors.k8s_ref}</div>}
      <ErrorMessage name="k8s_ref">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );

  return getK8SRef();
};
