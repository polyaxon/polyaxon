import conf

from polyaxon.celery_api import celery_app
from polyaxon.settings import K8SEventsCeleryTasks


def send_status(build_job, status, message=None, traceback=None):
    payload = {
        'details': {
            'labels': {
                'app': 'dockerizer',
                'job_uuid': build_job.uuid.hex,
                'job_name': build_job.unique_name,
                'project_uuid': build_job.project.uuid.hex,
                'project_name': build_job.project.unique_name,
            },
            'node_name': conf.get('K8S_NODE_NAME')
        },
        'status': status,
        'message': message,
        'traceback': traceback
    }
    celery_app.send_task(
        K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES,
        kwargs={'payload': payload})
