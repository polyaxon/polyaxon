import { Field, FieldProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import MDEdit from '../mdEditor/mdEdit';

export const ReadmeSchema = Yup.string();

export const ReadmeComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <MDEdit
    content=""
    handleChange={(value: string) => form.setFieldValue(field.name, value)}
  />
);

export const ReadmeField = (
  <div className="form-group">
    <label className="control-label">Readme</label>
    <Field name="readme" component={ReadmeComponent}/>
  </div>
);
