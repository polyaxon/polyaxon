import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const AFFINITIES_EXPERIMENTS =
  `${option_namespaces.AFFINITIES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const TOLERATIONS_EXPERIMENTS =
  `${option_namespaces.TOLERATIONS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const NODE_SELECTORS_EXPERIMENTS =
  `${option_namespaces.NODE_SELECTORS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const ENV_VARS_EXPERIMENTS =
  `${option_namespaces.ENV_VARS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const K8S_CONFIG_MAPS_EXPERIMENTS =
  `${option_namespaces.K8S_CONFIG_MAPS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const K8S_SECRETS_EXPERIMENTS =
  `${option_namespaces.K8S_SECRETS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const SERVICE_ACCOUNTS_EXPERIMENTS =
  `${option_namespaces.SERVICE_ACCOUNTS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;
export const K8S_RESOURCES_EXPERIMENTS =
  `${option_namespaces.K8S_RESOURCES}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.EXPERIMENTS}`;

export const EXPERIMENT_KEYS = [
  AFFINITIES_EXPERIMENTS,
  TOLERATIONS_EXPERIMENTS,
  NODE_SELECTORS_EXPERIMENTS,
  ENV_VARS_EXPERIMENTS,
  K8S_CONFIG_MAPS_EXPERIMENTS,
  K8S_SECRETS_EXPERIMENTS,
  SERVICE_ACCOUNTS_EXPERIMENTS,
  K8S_RESOURCES_EXPERIMENTS,
];

export const ClusterSchedulingExperimentsSettingsURL = '/app/settings/scheduling/experiments/';
