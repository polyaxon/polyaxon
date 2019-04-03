import { Field } from 'formik';
import * as React from 'react';

export const VisibilityField = (
  <div className="form-group">
    <label className="col-md-2 control-label">Visibility</label>
    <Field component="select" name="visibility" className="form-control input-sm">
      <option>Public</option>
      <option>Private</option>
    </Field>
  </div>
);
