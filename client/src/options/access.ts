import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const ACCESS_GIT =
  `${option_namespaces.ACCESS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.GIT}`;
export const ACCESS_REGISTRY =
  `${option_namespaces.ACCESS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.REGISTRY}`;
