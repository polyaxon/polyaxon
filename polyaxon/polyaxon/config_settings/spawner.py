from polyaxon.config_manager import config

PUBLIC_PLUGIN_JOBS = config.get_boolean('POLYAXON_PUBLIC_PLUGIN_JOBS', is_optional=True)

# k8s
K8S_SERVICE_ACCOUNT_NAME = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_NAME')
K8S_SERVICE_ACCOUNT_EXPERIMENTS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_EXPERIMENTS',
                                                    is_optional=True)
K8S_SERVICE_ACCOUNT_JOBS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_JOBS',
                                             is_optional=True)
K8S_SERVICE_ACCOUNT_BUILDS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_BUILDS',
                                               is_optional=True)
K8S_RBAC_ENABLED = config.get_boolean('POLYAXON_K8S_RBAC_ENABLED')
K8S_PROVISIONER_ENABLED = config.get_boolean('POLYAXON_K8S_PROVISIONER_ENABLED')
K8S_INGRESS_ENABLED = config.get_boolean('POLYAXON_K8S_INGRESS_ENABLED')
K8S_INGRESS_ANNOTATIONS = config.get_string('POLYAXON_K8S_INGRESS_ANNOTATIONS', is_optional=True)

# Builds
BUILD_ALWAYS_PULL_LATEST = config.get_boolean('POLYAXON_BUILD_ALWAYS_PULL_LATEST',
                                              is_optional=True,
                                              default=False)

# Refs
REFS_SECRETS = config.get_string('POLYAXON_REFS_SECRETS',
                                 is_optional=True,
                                 is_list=True,
                                 default=())
REFS_CONFIG_MAPS = config.get_string('POLYAXON_REFS_CONFIG_MAPS',
                                     is_optional=True,
                                     is_list=True,
                                     default=())

# Ports
TENSORBOARD_PORT_RANGE = [5700, 6700]
NOTEBOOK_PORT_RANGE = [6700, 7700]

# Roles
ROLE_LABELS_WORKER = config.get_string('POLYAXON_ROLE_LABELS_WORKER')
ROLE_LABELS_DASHBOARD = config.get_string('POLYAXON_ROLE_LABELS_DASHBOARD')
ROLE_LABELS_LOG = config.get_string('POLYAXON_ROLE_LABELS_LOG')
ROLE_LABELS_API = config.get_string('POLYAXON_ROLE_LABELS_API')

# Types
TYPE_LABELS_CORE = config.get_string('POLYAXON_TYPE_LABELS_CORE')
TYPE_LABELS_RUNNER = config.get_string('POLYAXON_TYPE_LABELS_RUNNER')

# Selectors
NODE_SELECTOR_EXPERIMENTS = config.get_string(
    'POLYAXON_NODE_SELECTOR_EXPERIMENTS', is_optional=True)
NODE_SELECTOR_JOBS = config.get_string(
    'POLYAXON_NODE_SELECTOR_JOBS', is_optional=True)
NODE_SELECTOR_BUILDS = config.get_string(
    'POLYAXON_NODE_SELECTOR_BUILDS', is_optional=True)
NODE_SELECTOR_TENSORBOARDS = config.get_string(
    'POLYAXON_NODE_SELECTOR_TENSORBOARDS', is_optional=True)
NODE_SELECTOR_CORE = config.get_string(
    'POLYAXON_NODE_SELECTOR_CORE', is_optional=True)

# Affinity
AFFINITY_EXPERIMENTS = config.get_string(
    'POLYAXON_AFFINITY_EXPERIMENTS', is_optional=True)
AFFINITY_JOBS = config.get_string(
    'POLYAXON_AFFINITY_JOBS', is_optional=True)
AFFINITY_BUILDS = config.get_string(
    'POLYAXON_AFFINITY_BUILDS', is_optional=True)
AFFINITY_TENSORBOARDS = config.get_string(
    'POLYAXON_AFFINITY_TENSORBOARDS', is_optional=True)
AFFINITY_CORE = config.get_string(
    'POLYAXON_AFFINITY_CORE', is_optional=True)

# Tolerations
TOLERATIONS_EXPERIMENTS = config.get_string(
    'POLYAXON_TOLERATIONS_EXPERIMENTS', is_optional=True)
TOLERATIONS_JOBS = config.get_string(
    'POLYAXON_TOLERATIONS_JOBS', is_optional=True)
TOLERATIONS_BUILDS = config.get_string(
    'POLYAXON_TOLERATIONS_BUILDS', is_optional=True)
TOLERATIONS_TENSORBOARDS = config.get_string(
    'POLYAXON_TOLERATIONS_TENSORBOARDS', is_optional=True)
TOLERATIONS_CORE = config.get_string(
    'POLYAXON_TOLERATIONS_CORE', is_optional=True)

# Container names
CONTAINER_NAME_EXPERIMENT_JOB = config.get_string('POLYAXON_CONTAINER_NAME_EXPERIMENT_JOB',
                                                  is_optional=True,
                                                  default='polyaxon-experiment-job')
CONTAINER_NAME_JOB = config.get_string('POLYAXON_CONTAINER_NAME_JOB',
                                       is_optional=True,
                                       default='polyaxon-job')
CONTAINER_NAME_SIDECAR = config.get_string('POLYAXON_CONTAINER_NAME_SIDECAR',
                                           is_optional=True,
                                           default='polyaxon-job-sidecar')
CONTAINER_NAME_INIT = config.get_string('POLYAXON_CONTAINER_NAME_INIT',
                                        is_optional=True,
                                        default='polyaxon-job-init')
CONTAINER_NAME_PLUGIN_JOB = config.get_string('POLYAXON_CONTAINER_NAME_PLUGIN_JOB',
                                              is_optional=True,
                                              default='polyaxon-plugin-job')
CONTAINER_NAME_DOCKERIZER_JOB = config.get_string('POLYAXON_CONTAINER_NAME_DOCKERIZER_JOB',
                                                  is_optional=True,
                                                  default='polyaxon-dockerizer-job')
JOB_DOCKER_NAME = config.get_string('POLYAXON_JOB_DOCKER_NAME',
                                    is_optional=True,
                                    default='polyaxon/polyaxon-lib')

# Sidecar
JOB_SIDECAR_DOCKER_IMAGE = config.get_string('POLYAXON_JOB_SIDECAR_DOCKER_IMAGE')
JOB_SIDECAR_DOCKER_IMAGE_PULL_POLICY = config.get_string(
    'POLYAXON_JOB_SIDECAR_DOCKER_IMAGE_PULL_POLICY',
    is_optional=True)

# Init job
JOB_INIT_DOCKER_IMAGE = config.get_string('POLYAXON_JOB_INIT_DOCKER_IMAGE')
JOB_INIT_DOCKER_IMAGE_PULL_POLICY = config.get_string(
    'POLYAXON_JOB_INIT_DOCKER_IMAGE_PULL_POLICY',
    is_optional=True)

# Dockerizer
BUILD_BACKEND = config.get_string('POLYAXON_BUILD_BACKEND',
                                  is_optional=True,
                                  default='native')
JOB_KANIKO_IMAGE = config.get_string('POLYAXON_JOB_KANIKO_IMAGE')
JOB_KANIKO_IMAGE_PULL_POLICY = config.get_string(
    'POLYAXON_JOB_KANIKO_IMAGE_PULL_POLICY',
    is_optional=True)
JOB_DOCKERIZER_IMAGE = config.get_string('POLYAXON_JOB_DOCKERIZER_IMAGE')
JOB_DOCKERIZER_IMAGE_PULL_POLICY = config.get_string(
    'POLYAXON_JOB_DOCKERIZER_IMAGE_PULL_POLICY',
    is_optional=True,)

# Tensorboard
TENSORBOARD_DOCKER_IMAGE = config.get_string('POLYAXON_TENSORBOARD_DOCKER_IMAGE',
                                             is_optional=True,
                                             default='tensorflow/tensorflow:1.11.0-py3')

# Notebook config
MOUNT_CODE_IN_NOTEBOOKS = config.get_boolean('POLYAXON_MOUNT_CODE_IN_NOTEBOOKS',
                                             is_optional=True,
                                             default=False)
NOTEBOOK_DOCKER_IMAGE = config.get_string('POLYAXON_NOTEBOOK_DOCKER_IMAGE',
                                          is_optional=True)
NOTEBOOK_BACKEND = config.get_string('POLYAXON_NOTEBOOK_BACKEND',
                                     is_optional=True,
                                     default='notebook')
# Sidecar config
JOB_SIDECAR_LOG_SLEEP_INTERVAL = config.get_int('POLYAXON_JOB_SIDECAR_LOG_SLEEP_INTERVAL',
                                                is_optional=True)

# TPU
K8S_TPU_TF_VERSION = config.get_string('POLYAXON_K8S_TPU_TF_VERSION',
                                       is_optional=True,
                                       default='1.12')
