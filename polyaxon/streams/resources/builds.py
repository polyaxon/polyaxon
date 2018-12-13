from django.conf import settings

import auditor

from constants.k8s_jobs import DOCKERIZER_JOB_NAME, JOB_NAME_FORMAT
from event_manager.events.build_job import BUILD_JOB_LOGS_VIEWED
from streams.authentication import authorized
from streams.resources.logs import log_job
from streams.resources.utils import get_error_message
from streams.validation.build import validate_build


@authorized()
async def build_logs_v2(request, ws, username, project_name, build_id):
    job, message = validate_build(request=request,
                                  username=username,
                                  project_name=project_name,
                                  build_id=build_id)
    if job is None:
        await ws.send(get_error_message(message))
        return

    job_uuid = job.uuid.hex

    auditor.record(event_type=BUILD_JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)
    pod_id = JOB_NAME_FORMAT.format(name=DOCKERIZER_JOB_NAME, job_uuid=job_uuid)
    # Stream logs
    await log_job(request=request,
                  ws=ws,
                  job=job,
                  pod_id=pod_id,
                  container=settings.CONTAINER_NAME_DOCKERIZER_JOB,
                  namespace=settings.K8S_NAMESPACE)
