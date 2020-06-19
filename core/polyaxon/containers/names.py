MAIN_JOB_CONTAINER = "polyaxon-main"
INIT_AUTH_CONTAINER = "polyaxon-init-auth"
SIDECAR_CONTAINER = "polyaxon-sidecar"
TFJOBS_CONTAINER = "tensorflow"
PYTORCHJOBS_CONTAINER = "pytorch"
INIT_DOCKERFILE_CONTAINER_PREFIX = "polyaxon-init-dockerfile"
INIT_GIT_CONTAINER_PREFIX = "polyaxon-init-git"
INIT_ARTIFACTS_CONTAINER_PREFIX = "polyaxon-init-artifacts"
POLYAXON_INIT_PREFIX = "polyaxon-init"
INIT_PREFIX = "init"
SIDECAR_PREFIX = "sidecar"


def generate_container_name(prefix: str, suffix: str = None) -> str:
    import uuid

    prefix = prefix or "container"
    suffix = suffix or uuid.uuid4().hex[:10]
    return "{}-{}".format(prefix, suffix)
