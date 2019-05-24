from polyaxon.config_manager import config

CLUSTER_NOTIFICATION_URL = config.notification_url

CLUSTER_NOTIFICATION_ALIVE_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}"
    "%2F{created_at}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")

CLUSTER_NOTIFICATION_NODES_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}%2F{n_nodes}"
    "%2F{n_cpus}%2F{memory}%2F{n_gpus}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")
