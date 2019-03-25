import { FormikProps } from 'formik';
import * as _ from 'lodash';

export const checkServerError = (errors: any, field: string) => _.isObject(errors) && field in errors;
export const checkValidationError = (props: FormikProps<{}>, field: string) => {
  return _.get(props.errors, field) && _.get(props.touched, field);
};
