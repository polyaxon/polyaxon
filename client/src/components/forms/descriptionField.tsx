import { ErrorMessage, Field, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';
import * as Yup from 'yup';

export const DescriptionSchema = Yup.string();

export const DescriptionField = (props: FormikProps<{}>) => (
  <div
    className={`${(_.get(props.errors, 'description') && _.get(props.touched, 'description'))
      ? 'has-error'
      : ''} form-group`}
  >
    <label className="col-sm-2 control-label">Description</label>
    <div className="col-sm-10">
      <Field
        type="text"
        name="description"
        placeholder="Description"
        className="form-control input-sm"
      />
      <ErrorMessage name="description">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  </div>
);
