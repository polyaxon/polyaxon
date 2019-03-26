import * as _ from 'lodash';

import { AlertByIds, AlertGlobal } from '../models/alerts';

export const getErrorsByIds = (alerts: AlertByIds, isLoading: boolean, id: string, type: string): boolean => {
  if (!(_.isNil(alerts[id])) && alerts[id].type === type && isLoading) {
    return alerts[id].error;
  }
  return false;
};

export const getErrorsGlobal = (alerts: AlertGlobal, isLoading: boolean, type: string): boolean => {
  if (!(_.isNil(alerts[type])) && !(_.isNil(alerts[type].error) && isLoading)) {
    return alerts[type].error;
  }
  return false;
};
