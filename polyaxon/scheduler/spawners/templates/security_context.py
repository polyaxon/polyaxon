from kubernetes import client

from scheduler.spawners.templates.constants import POLYAXON_FS_GROUP, POLYAXON_USER


def get_security_context():
    return client.V1PodSecurityContext(fs_group=POLYAXON_FS_GROUP,
                                       run_as_user=POLYAXON_USER,
                                       run_as_group=POLYAXON_USER)
