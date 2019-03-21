import { ErrorMessage, Field, FieldProps, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';
import * as Yup from 'yup';

import Polyaxonfile from '../polyaxonfile/polyaxonfile';

export const ConfigSchema = Yup.string();

export const ConfigComponent: React.FunctionComponent<FieldProps> = (
  {
    field,
    form,
  }) => (
  <Polyaxonfile
    content=""
    handleChange={(value: string) => {
      form.setFieldValue(field.name, value);
    }}
  />
);

export const ConfigField = (props: FormikProps<{}>) => (
  <div
    className={`${(_.get(props.errors, 'config') && _.get(props.touched, 'config'))
      ? 'has-error'
      : ''} form-group`}
  >
    <label className="col-sm-2 control-label">Config</label>
    <div className="col-sm-10">
      <Field name="config" component={ConfigComponent}/>
      <ErrorMessage name="config">
        {(errorMessage) => <div className="help-block">{errorMessage}</div>}
      </ErrorMessage>
    </div>
  </div>
);
