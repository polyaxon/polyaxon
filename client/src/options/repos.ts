import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const REPOS_ACCESS_TOKEN =
  `${option_namespaces.REPOS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.ACCESS_TOKEN}`;
export const REPOS_CREDENTIALS =
  `${option_namespaces.REPOS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CREDENTIALS}`;

export const REPOS_KEYS = [
  REPOS_ACCESS_TOKEN,
  REPOS_CREDENTIALS,
];
