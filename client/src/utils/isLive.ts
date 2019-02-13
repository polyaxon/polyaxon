import * as _ from 'lodash';

export const isLive = (obj: any): boolean => _.isNil(obj.deleted) || !obj.deleted;
