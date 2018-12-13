from django.conf import settings

import auditor

from constants.k8s_jobs import JOB_NAME, JOB_NAME_FORMAT
from event_manager.events.job import JOB_LOGS_VIEWED
from streams.authentication import authorized
from streams.resources.logs import log_job
from streams.resources.utils import get_error_message
from streams.validation.job import validate_job


@authorized()
async def job_logs_v2(request, ws, username, project_name, job_id):
    job, message = validate_job(request=request,
                                username=username,
                                project_name=project_name,
                                job_id=job_id)
    if job is None:
        await ws.send(get_error_message(message))
        return

    job_uuid = job.uuid.hex

    auditor.record(event_type=JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    pod_id = JOB_NAME_FORMAT.format(name=JOB_NAME, job_uuid=job_uuid)
    # Stream logs
    await log_job(request=request,
                  ws=ws,
                  job=job,
                  pod_id=pod_id,
                  container=settings.CONTAINER_NAME_JOB,
                  namespace=settings.K8S_NAMESPACE)
