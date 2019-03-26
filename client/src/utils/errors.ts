import * as _ from 'lodash';

import { AlertByIds, AlertGlobal } from '../models/alerts';

export const getErrorsByIds = (errors: AlertByIds, isLoading: boolean, id: string, type: string): boolean => {
  if (!(_.isNil(errors[id])) && errors[id].type === type && isLoading) {
    return errors[id].error;
  }
  return false;
};

export const getErrorsGlobal = (errors: AlertGlobal, isLoading: boolean, type: string): boolean => {
  if (!(_.isNil(errors[type])) && !(_.isNil(errors[type].error) && isLoading)) {
    return errors[type].error;
  }
  return false;
};
