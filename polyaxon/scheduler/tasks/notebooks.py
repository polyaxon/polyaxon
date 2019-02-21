import logging

import conf

from constants.jobs import JobLifeCycle
from db.getters.notebooks import get_valid_notebook
from polyaxon.celery_api import celery_app
from polyaxon.settings import Intervals, SchedulerCeleryTasks
from scheduler import dockerizer_scheduler, notebook_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def projects_notebook_build(notebook_job_id):
    notebook_job = get_valid_notebook(notebook_job_id=notebook_job_id)
    if not notebook_job:
        return None

    if not JobLifeCycle.can_transition(status_from=notebook_job.last_status,
                                       status_to=JobLifeCycle.BUILDING):
        _logger.info('Notebook `%s` cannot transition from `%s` to `%s`.',
                     notebook_job, notebook_job.last_status, JobLifeCycle.BUILDING)
        return

    build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
        user=notebook_job.user,
        project=notebook_job.project,
        config=notebook_job.specification.build,
        configmap_refs=notebook_job.specification.configmap_refs,
        secret_refs=notebook_job.specification.secret_refs,
        code_reference=notebook_job.code_reference)

    notebook_job.build_job = build_job
    notebook_job.save(update_fields=['build_job'])
    if image_exists:
        # The image already exists, so we can start the experiment right away
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START,
            kwargs={'notebook_job_id': notebook_job_id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return

    if not build_status:
        notebook_job.set_status(JobLifeCycle.FAILED, message='Could not start build process.')
        return

    # Update job status to show that its building docker image
    notebook_job.set_status(JobLifeCycle.BUILDING, message='Building container')


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START, ignore_result=True)
def projects_notebook_start(notebook_job_id):
    notebook_job = get_valid_notebook(notebook_job_id=notebook_job_id)
    if not notebook_job:
        return None

    if not JobLifeCycle.can_transition(status_from=notebook_job.last_status,
                                       status_to=JobLifeCycle.SCHEDULED):
        _logger.info('Notebook `%s` cannot transition from `%s` to `%s`.',
                     notebook_job.unique_name, notebook_job.last_status, JobLifeCycle.SCHEDULED)

    notebook_scheduler.start_notebook(notebook_job)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_SCHEDULE_DELETION, ignore_result=True)
def projects_notebook_schedule_deletion(notebook_job_id):
    notebook_job = get_valid_notebook(notebook_job_id=notebook_job_id, include_deleted=True)
    if not notebook_job:
        return None

    notebook_job.archive()

    if notebook_job.is_stoppable:
        project = notebook_job.project
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
            kwargs={
                'project_name': project.unique_name,
                'project_uuid': project.uuid.hex,
                'notebook_job_name': notebook_job.unique_name,
                'notebook_job_uuid': notebook_job.uuid.hex,
                'update_status': True,
                'collect_logs': False,
                'message': 'Notebook is scheduled for deletion.'
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def projects_notebook_stop(self,
                           project_name,
                           project_uuid,
                           notebook_job_name,
                           notebook_job_uuid,
                           update_status=True,
                           collect_logs=False,
                           message=None):
    deleted = notebook_scheduler.stop_notebook(
        project_name=project_name,
        project_uuid=project_uuid,
        notebook_job_name=notebook_job_name,
        notebook_job_uuid=notebook_job_uuid)

    if not deleted and self.request.retries < 2:
        _logger.info('Trying again to delete job `%s`.', notebook_job_name)
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    if not update_status:
        return

    notebook = get_valid_notebook(notebook_job_uuid=notebook_job_uuid, include_deleted=True)
    if not notebook:
        return None

    # Update notebook status to show that its stopped
    notebook.set_status(status=JobLifeCycle.STOPPED,
                        message=message or 'Notebook was stopped')
