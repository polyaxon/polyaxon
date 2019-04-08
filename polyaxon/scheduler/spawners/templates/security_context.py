from kubernetes import client

import conf


def get_security_context():
    uid = conf.get('SECURITY_CONTEXT_USER')
    gid = conf.get('SECURITY_CONTEXT_GROUP')
    if uid and gid:
        return client.V1PodSecurityContext(fs_group=gid,
                                           run_as_user=uid,
                                           run_as_group=gid)
    return None
