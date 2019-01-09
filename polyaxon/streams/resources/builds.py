import auditor
import conf

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

    pod_id = job.pod_id

    auditor.record(event_type=BUILD_JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)
    # Stream logs
    await log_job(request=request,
                  ws=ws,
                  job=job,
                  pod_id=pod_id,
                  container=conf.get('CONTAINER_NAME_DOCKERIZER_JOB'),
                  namespace=conf.get('K8S_NAMESPACE'))
