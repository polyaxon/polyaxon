import * as _ from 'lodash';

import { AlertByIds, AlertGlobal } from '../models/alerts';

export const getSuccessByIds = (alerts: AlertByIds, isLoading: boolean, id: string, type: string): boolean | null => {
  if (!(_.isNil(alerts[id])) && alerts[id].type === type && !isLoading && !(_.isNil(alerts[id].success))) {
    return alerts[id].success;
  }
  return false;
};

export const getSuccessGlobal = (alerts: AlertGlobal, isLoading: boolean, type: string): boolean | null => {
  if (!(_.isNil(alerts[type])) && !(_.isNil(alerts[type].success)) && !isLoading) {
    return alerts[type].success;
  }
  return false;
};
