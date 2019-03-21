import { Field, FieldProps } from 'formik';
import * as React from 'react';

import MDEdit from '../mdEditor/mdEdit';

export const ReadmeComponent: React.FunctionComponent<FieldProps> = ({
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
    <label className="col-sm-2 control-label">Readme</label>
    <div className="col-sm-10">
      <Field name="readme" component={ReadmeComponent}/>
    </div>
  </div>
);
