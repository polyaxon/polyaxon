import { Field, FieldProps } from 'formik';
import * as React from 'react';

import TagsEdit from '../tags/tagsEdit';

export const TagsComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <TagsEdit
    tags={[]}
    handleChange={(value: Array<{ label: string, value: string }>) => form.setFieldValue(field.name, value)}
  />
);

export const TagsField = (
  <div className="form-group">
    <label className="col-sm-2 control-label">Tags</label>
    <div className="col-sm-10">
      <Field name="tags" component={TagsComponent}/>
    </div>
  </div>
);
