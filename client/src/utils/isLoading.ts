import * as _ from 'lodash';

export const getIsLoading = (byIds: any, id: string, type: string): boolean => {
  return !(_.isNil(byIds[id])) && byIds[id].type === type && byIds[id].isLoading;
};
