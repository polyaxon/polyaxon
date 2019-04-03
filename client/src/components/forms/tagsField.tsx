import { Field, FieldProps, FormikProps } from 'formik';
import * as React from 'react';

import TagsEdit from '../tags/tagsEdit';
import { checkServerError, checkValidationError } from './validation';

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

export const TagsField = (props: FormikProps<{}>, errors: any) => {
  const hasServerError = checkServerError(errors, 'name');
  const hasValidationError = checkValidationError(props, 'name');
  const hasError = hasServerError || hasValidationError;

  return (
    <div className={`${hasError ? 'has-error' : ''} form-group`}>
      <label className=" control-label">Tags</label>
      <Field name="tags" component={TagsComponent}/>
      {hasServerError && <div className="help-block">{errors.name}</div>}
    </div>
  );
};
