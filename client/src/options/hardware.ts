import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const K8S_GPU_RESOURCE_KEY =
    `${option_namespaces.K8S}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.GPU_RESOURCE_KEY}`;
export const K8S_TPU_TF_VERSION =
    `${option_namespaces.K8S}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TPU_TF_VERSION}`;
export const K8S_TPU_RESOURCE_KEY =
    `${option_namespaces.K8S}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TPU_RESOURCE_KEY}`;

export const HARDWARE_KEYS = [
  K8S_GPU_RESOURCE_KEY,
  K8S_TPU_TF_VERSION,
  K8S_TPU_RESOURCE_KEY,
];

export const ClusterHardwareSettingsURL = '/app/settings/hardware/';
