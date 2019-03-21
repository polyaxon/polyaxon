import { ErrorMessage, Field, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';
import * as Yup from 'yup';

import { NameSlug } from '../../constants/helpTexts';

export const NameSchema = Yup.string()
  .min(2, 'Name too Short.')
  .max(128, 'Name too Long.');

function validateName(value: string) {
  let error;
  if (value && !/^([-a-zA-Z0-9_]+)$/.test(value)) {
    error = 'Name is not a valid slug.';
  }
  return error;
}

export const NameField = (props: FormikProps<{}>) => (
  <div
    className={`${(_.get(props.errors, 'name') && _.get(props.touched, 'name')) ? 'has-error' : ''} form-group`}
  >
    <label className="col-sm-2 control-label">Name</label>
    <div className="col-sm-5">
      <Field
        type="text"
        name="name"
        className="form-control input-sm"
        validate={validateName}
      />
      <span id="helpBlock" className="help-block">{NameSlug}</span>
      <ErrorMessage name="name">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  </div>
);
