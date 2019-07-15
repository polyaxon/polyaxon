import conf

from options.registry.container_names import CONTAINER_NAME_BUILD_JOBS
from options.registry.k8s import K8S_NAMESPACE
from streams.resources.logs import log_job
from streams.resources.utils import get_error_message
from streams.validation.build import get_build_job


async def build_logs_v2(request, ws, username, project_name, build_id):
    job, message = get_build_job(build_id=build_id)
    if job is None:
        await ws.send(get_error_message(message))
        return

    pod_id = job.pod_id
    # Stream logs
    await log_job(request=request,
                  ws=ws,
                  job=job,
                  pod_id=pod_id,
                  container=conf.get(CONTAINER_NAME_BUILD_JOBS),
                  namespace=conf.get(K8S_NAMESPACE))
