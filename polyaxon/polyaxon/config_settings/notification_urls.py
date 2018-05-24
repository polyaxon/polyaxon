from polyaxon.utils import config

CLUSTER_NOTIFICATION_URL = config.notification_url

POLYAXON_NOTIFICATION_CLUSTER_ALIVE_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}"
    "%2F{create_at}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")

POLYAXON_NOTIFICATION_CLUSTER_NODES_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}%2F{n_nodes}"
    "%2F{n_cpus}%2F{memory}%2F{n_gpus}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")
