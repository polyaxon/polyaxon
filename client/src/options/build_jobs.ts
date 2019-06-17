import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const AFFINITIES_BUILD_JOBS =
  `${option_namespaces.AFFINITIES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const TOLERATIONS_BUILD_JOBS =
  `${option_namespaces.TOLERATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const NODE_SELECTORS_BUILD_JOBS =
  `${option_namespaces.NODE_SELECTORS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const ENV_VARS_BUILD_JOBS =
  `${option_namespaces.ENV_VARS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const K8S_CONFIG_MAPS_BUILD_JOBS =
  `${option_namespaces.K8S_CONFIG_MAPS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const K8S_SECRETS_BUILD_JOBS =
  `${option_namespaces.K8S_SECRETS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const SERVICE_ACCOUNTS_BUILD_JOBS =
  `${option_namespaces.SERVICE_ACCOUNTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;
export const K8S_RESOURCES_BUILD_JOBS =
  `${option_namespaces.K8S_RESOURCES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BUILD_JOBS}`;

export const BUILD_JOBS_BACKEND =
  `${option_namespaces.BUILD_JOBS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.BACKEND}`;
export const BUILD_JOBS_SET_SECURITY_CONTEXT =
  `${option_namespaces.BUILD_JOBS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.SET_SECURITY_CONTEXT}`;
export const BUILD_JOBS_LANG_ENV =
  `${option_namespaces.BUILD_JOBS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.LANG_ENV}`;

export const KANIKO_DOCKER_IMAGE =
  `${option_namespaces.KANIKO}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.DOCKER_IMAGE}`;
export const KANIKO_IMAGE_PULL_POLICY =
  `${option_namespaces.KANIKO}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.IMAGE_PULL_POLICY}`;

export const BUILD_JOB_KEYS = [
  AFFINITIES_BUILD_JOBS,
  TOLERATIONS_BUILD_JOBS,
  NODE_SELECTORS_BUILD_JOBS,
  ENV_VARS_BUILD_JOBS,
  K8S_CONFIG_MAPS_BUILD_JOBS,
  K8S_SECRETS_BUILD_JOBS,
  SERVICE_ACCOUNTS_BUILD_JOBS,
  K8S_RESOURCES_BUILD_JOBS,
  BUILD_JOBS_SET_SECURITY_CONTEXT,
  BUILD_JOBS_LANG_ENV,
  BUILD_JOBS_BACKEND,
  KANIKO_DOCKER_IMAGE,
  KANIKO_IMAGE_PULL_POLICY,
];
