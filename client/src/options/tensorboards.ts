import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const ANNOTATIONS_TENSORBOARDS =
  `${option_namespaces.ANNOTATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const AFFINITIES_TENSORBOARDS =
  `${option_namespaces.AFFINITIES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const TOLERATIONS_TENSORBOARDS =
  `${option_namespaces.TOLERATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const NODE_SELECTORS_TENSORBOARDS =
  `${option_namespaces.NODE_SELECTORS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const ENV_VARS_TENSORBOARDS =
  `${option_namespaces.ENV_VARS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const K8S_CONFIG_MAPS_TENSORBOARDS =
  `${option_namespaces.K8S_CONFIG_MAPS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const K8S_SECRETS_TENSORBOARDS =
  `${option_namespaces.K8S_SECRETS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const SERVICE_ACCOUNTS_TENSORBOARDS =
  `${option_namespaces.SERVICE_ACCOUNTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const K8S_RESOURCES_TENSORBOARDS =
  `${option_namespaces.K8S_RESOURCES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;
export const MAX_RESTARTS_TENSORBOARDS =
  `${option_namespaces.MAX_RESTARTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENSORBOARDS}`;

export const TENSORBOARDS_DOCKER_IMAGE =
  `${option_namespaces.TENSORBOARDS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.DOCKER_IMAGE}`;

export const TENSORBOARD_KEYS = [
  AFFINITIES_TENSORBOARDS,
  TOLERATIONS_TENSORBOARDS,
  NODE_SELECTORS_TENSORBOARDS,
  ANNOTATIONS_TENSORBOARDS,
  ENV_VARS_TENSORBOARDS,
  K8S_CONFIG_MAPS_TENSORBOARDS,
  K8S_SECRETS_TENSORBOARDS,
  SERVICE_ACCOUNTS_TENSORBOARDS,
  K8S_RESOURCES_TENSORBOARDS,
  MAX_RESTARTS_TENSORBOARDS,
  TENSORBOARDS_DOCKER_IMAGE,
];
