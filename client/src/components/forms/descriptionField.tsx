import { ErrorMessage, Field, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';
import * as Yup from 'yup';

import { checkServerError, checkValidationError } from './validation';

export const DescriptionSchema = Yup.string();

export const DescriptionField = (props: FormikProps<{}>, errors: any, col?: string) => {
  const hasServerError = checkServerError(errors, 'description');
  const hasValidationError = checkValidationError(props, 'description');
  const hasError = hasServerError || hasValidationError;
  const isInline = !_.isNil(col);

  const getDescription = () => (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="control-label">Description</label>
      <Field
        type="text"
        name="description"
        placeholder="Description"
        className="form-control input-sm"
      />
      {hasServerError && <div className="help-block">{errors.description}</div>}
      <ErrorMessage name="description">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  );

  const getInlineDescription = () => (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className="col-md-2 control-label">Description</label>
      <div className={col ? `col-md-${col}` : `col-md-5`}>
        <Field
          type="text"
          name="description"
          placeholder="Description"
          className="form-control input-sm"
        />
        {hasServerError && <div className="help-block">{errors.description}</div>}
        <ErrorMessage name="description">
          {(errorMessage) => <div className="help-block">{errorMessage}</div>}
        </ErrorMessage>
      </div>
    </div>
  );

  return isInline ? getInlineDescription() : getDescription();
};
