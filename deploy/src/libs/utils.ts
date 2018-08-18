import * as jsYaml from 'js-yaml';
import * as _ from 'lodash';

export function b64DecodeUnicode(str: string) {
  // Going backwards: from bytestream, to percent-encoding, to original string.
  return decodeURIComponent(atob(str).split('').map((c: string) => {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
}

export function checkDefaultOrUndefined(value: any, configValue?: any, deep: boolean = false) {
  let check: boolean;
  if (!deep) {
    check = value === configValue || !value;
  } else {
    check = _.isEqual(value, configValue) || !value;
  }
  if (check) {
    return undefined;
  } else {
    return value;
  }
}

export function parseJson(value: string) {
  try {
    return JSON.parse(value);
  } catch (e) {
    return null;
  }
}

export function parseYaml(value: string) {
  try {
    return jsYaml.safeLoad(value);
  } catch (e) {
    return null;
  }
}

export const checkArray = (v: any) =>  _.isNil(v) || ! (v instanceof Array);
export const checkObj = (v: any) =>  _.isNil(v) ||
  ! (typeof v === 'object') ||
  ((v instanceof Array) || (v instanceof Date));
