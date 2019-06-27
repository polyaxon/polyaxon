import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const AFFINITIES_JOBS =
  `${option_namespaces.AFFINITIES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const TOLERATIONS_JOBS =
  `${option_namespaces.TOLERATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const NODE_SELECTORS_JOBS =
  `${option_namespaces.NODE_SELECTORS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const ENV_VARS_JOBS =
  `${option_namespaces.ENV_VARS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const K8S_CONFIG_MAPS_JOBS =
  `${option_namespaces.K8S_CONFIG_MAPS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const K8S_SECRETS_JOBS =
  `${option_namespaces.K8S_SECRETS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const SERVICE_ACCOUNTS_JOBS =
  `${option_namespaces.SERVICE_ACCOUNTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const K8S_RESOURCES_JOBS =
  `${option_namespaces.K8S_RESOURCES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;
export const MAX_RESTARTS_JOBS =
  `${option_namespaces.MAX_RESTARTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.JOBS}`;

export const JOB_KEYS = [
  AFFINITIES_JOBS,
  TOLERATIONS_JOBS,
  NODE_SELECTORS_JOBS,
  ENV_VARS_JOBS,
  K8S_CONFIG_MAPS_JOBS,
  K8S_SECRETS_JOBS,
  SERVICE_ACCOUNTS_JOBS,
  K8S_RESOURCES_JOBS,
  MAX_RESTARTS_JOBS
];
