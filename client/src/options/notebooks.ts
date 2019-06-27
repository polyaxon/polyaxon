import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const AFFINITIES_NOTEBOOKS =
  `${option_namespaces.AFFINITIES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const TOLERATIONS_NOTEBOOKS =
  `${option_namespaces.TOLERATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const NODE_SELECTORS_NOTEBOOKS =
  `${option_namespaces.NODE_SELECTORS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const ENV_VARS_NOTEBOOKS =
  `${option_namespaces.ENV_VARS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const K8S_CONFIG_MAPS_NOTEBOOKS =
  `${option_namespaces.K8S_CONFIG_MAPS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const K8S_SECRETS_NOTEBOOKS =
  `${option_namespaces.K8S_SECRETS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const SERVICE_ACCOUNTS_NOTEBOOKS =
  `${option_namespaces.SERVICE_ACCOUNTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const K8S_RESOURCES_NOTEBOOKS =
  `${option_namespaces.K8S_RESOURCES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;
export const MAX_RESTARTS_NOTEBOOKS =
  `${option_namespaces.MAX_RESTARTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.NOTEBOOKS}`;

export const NOTEBOOKS_BACKEND =
  `${option_namespaces.NOTEBOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BACKEND}`;
export const NOTEBOOKS_DOCKER_IMAGE =
  `${option_namespaces.NOTEBOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.DOCKER_IMAGE}`;

export const NOTEBOOK_KEYS = [
  AFFINITIES_NOTEBOOKS,
  TOLERATIONS_NOTEBOOKS,
  NODE_SELECTORS_NOTEBOOKS,
  ENV_VARS_NOTEBOOKS,
  K8S_CONFIG_MAPS_NOTEBOOKS,
  K8S_SECRETS_NOTEBOOKS,
  SERVICE_ACCOUNTS_NOTEBOOKS,
  K8S_RESOURCES_NOTEBOOKS,
  MAX_RESTARTS_NOTEBOOKS,
  NOTEBOOKS_BACKEND,
  NOTEBOOKS_DOCKER_IMAGE,
];
