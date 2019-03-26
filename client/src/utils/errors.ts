import * as _ from 'lodash';

export const getErrors = (errors: any, id: string, type: string): boolean => {
  return !(_.isNil(errors[id])) && errors[id].type === type && errors[id].isLoading;
};
