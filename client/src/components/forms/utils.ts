import * as _ from 'lodash';

export const sanitizeForm = (formValues: { [key: string]: any }) => {
  Object.keys(formValues).forEach((key: string) =>
    (_.isNil(formValues[key]) || formValues[key] === '') && delete formValues[key]);
  return formValues;
};
