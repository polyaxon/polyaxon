import { Field, FieldProps } from 'formik';
import * as React from 'react';

import Polyaxonfile from '../polyaxonfile/polyaxonfile';

export const ConfigComponent: React.FunctionComponent<FieldProps> = ({
  field,
  form,
}) => (
  <Polyaxonfile
    content=""
    handleChange={(value: string) => { form.setFieldValue(field.name, value); }}
  />
);

export const ConfigField = (
  <div className="form-group">
    <label className="col-sm-2 control-label">Config</label>
    <div className="col-sm-10">
      <Field name="config" component={ConfigComponent}/>
    </div>
  </div>
);
