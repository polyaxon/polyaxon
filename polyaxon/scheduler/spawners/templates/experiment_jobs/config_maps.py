import base64
import json

from kubernetes import client

from libs.api import API_KEY_NAME, get_settings_api_url
from libs.paths.experiments import get_experiment_logs_path, get_experiment_outputs_path
from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates import constants


def get_map_labels(project_name,
                   experiment_group_name,
                   experiment_name,
                   project_uuid,
                   experiment_group_uuid,
                   experiment_uuid):
    labels = {'project_name': project_name,
              'experiment_group_name': experiment_group_name,
              'experiment_name': experiment_name,
              'project_uuid': project_uuid,
              'experiment_uuid': experiment_uuid}
    if experiment_group_uuid:
        labels['experiment_group_uuid'] = experiment_group_uuid

    return labels


def get_config_map(namespace,
                   project_name,
                   experiment_group_name,
                   experiment_name,
                   project_uuid,
                   experiment_group_uuid,
                   experiment_uuid,
                   original_name,
                   cloning_strategy,
                   cluster_def,
                   persistence_outputs,
                   persistence_data,
                   declarations,
                   log_level):
    name = constants.CONFIG_MAP_NAME.format(uuid=experiment_uuid)
    labels = get_map_labels(project_name,
                            experiment_group_name,
                            experiment_name,
                            project_uuid,
                            experiment_group_uuid,
                            experiment_uuid)
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    experiment_outputs_path = get_experiment_outputs_path(persistence_outputs=persistence_outputs,
                                                          experiment_name=experiment_name,
                                                          original_name=original_name,
                                                          cloning_strategy=cloning_strategy)
    experiment_logs_path = get_experiment_logs_path(experiment_name)
    data = {
        constants.CONFIG_MAP_CLUSTER_KEY_NAME: json.dumps(cluster_def),
        constants.CONFIG_MAP_DECLARATIONS_KEY_NAME: json.dumps(declarations) or '{}',
        constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME: json.dumps(labels),
        constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME: log_level,
        API_KEY_NAME: get_settings_api_url(),
        constants.CONFIG_MAP_RUN_OUTPUTS_PATH_KEY_NAME: experiment_outputs_path,
        constants.CONFIG_MAP_RUN_LOGS_PATH_KEY_NAME: experiment_logs_path,
        constants.CONFIG_MAP_RUN_DATA_PATH_KEY_NAME: persistence_data,
    }
    return client.V1ConfigMap(api_version=k8s_constants.K8S_API_VERSION_V1,
                              kind=k8s_constants.K8S_CONFIG_MAP_KIND,
                              metadata=metadata,
                              data=data)


def get_secret(namespace,
               project_name,
               experiment_group_name,
               experiment_name,
               project_uuid,
               experiment_group_uuid,
               experiment_uuid,
               user_token):
    name = constants.SECRET_NAME.format(uuid=experiment_uuid)
    labels = get_map_labels(project_name,
                            experiment_group_name,
                            experiment_name,
                            project_uuid,
                            experiment_group_uuid,
                            experiment_uuid)
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    data = {
        constants.SECRET_USER_TOKEN: base64.b64encode(bytes(user_token, 'utf-8')).decode("utf-8")
    }
    return client.V1Secret(api_version=k8s_constants.K8S_API_VERSION_V1,
                           kind=k8s_constants.K8S_SECRET_KIND,
                           metadata=metadata,
                           type="Opaque",
                           data=data)
