import { Field } from 'formik';
import * as React from 'react';

export const VisibilityField = (
  <div className="form-group">
    <label className="col-sm-2 control-label">Visibility</label>
    <div className="col-sm-2">
      <Field component="select" name="visibility" className="form-control input-sm">
        <option>Public</option>
        <option>Private</option>
      </Field>
    </div>
  </div>
);
