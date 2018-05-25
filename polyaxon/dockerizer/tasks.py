import logging

from docker.errors import DockerException

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.getters.experiments import get_valid_experiment
from db.getters.projects import get_valid_project
from db.models.repos import Repo
from dockerizer.builders import experiments as experiments_builder
from dockerizer.builders import notebooks as notebooks_builder
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import Intervals, RunnerCeleryTasks

_logger = logging.getLogger(__name__)


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def projects_notebook_build(project_id):
    project = get_valid_project(project_id)
    if not project or not project.notebook:
        return None

    job = project.notebook

    # Update job status to show that its building docker image
    job.set_status(JobLifeCycle.BUILDING, message='Building container')

    # Building the docker image
    try:
        status = notebooks_builder.build_notebook_job(project=project, job=project.notebook)
    except DockerException as e:
        _logger.warning('Failed to build notebook %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Failed to build image for notebook.')
        return
    except Repo.DoesNotExist:
        _logger.warning('No code was found for this project')
        job.set_status(
            JobLifeCycle.FAILED,
            message='Failed to build image for notebook.')
        return
    except Exception as e:  # Other exceptions
        _logger.warning('Failed to build notebook %s', e)
        job.set_status(JobLifeCycle.FAILED,
                       message='Failed to build image for notebook.')
        return

    if not status:
        return

    # Now we can start the notebook
    celery_app.send_task(
        RunnerCeleryTasks.PROJECTS_NOTEBOOK_START,
        kwargs={'project_id': project_id})


@celery_app.task(name=RunnerCeleryTasks.EXPERIMENTS_BUILD, bind=True, max_retries=3)
def build_experiment(self, experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        if self.request.retries < 2:
            _logger.info('Trying again for Experiment `%s`.', experiment_id)
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

        _logger.info('Something went wrong, '
                     'the Experiment `%s` does not exist anymore.', experiment_id)
        return

    # No need to build the image, start the experiment directly
    if not experiment.specification.run_exec:
        celery_app.send_task(
            RunnerCeleryTasks.EXPERIMENTS_START,
            kwargs={'experiment_id': experiment_id})
        return

    if not ExperimentLifeCycle.can_transition(status_from=experiment.last_status,
                                              status_to=ExperimentLifeCycle.BUILDING):
        _logger.info('Experiment id `%s` cannot transition from `%s` to `%s`.',
                     experiment_id, experiment.last_status, ExperimentLifeCycle.BUILDING)
        return None

    # Update experiment status to show that its building
    experiment.set_status(ExperimentLifeCycle.BUILDING)

    # Building the docker image
    try:
        status = experiments_builder.build_experiment(experiment)
    except DockerException as e:
        _logger.warning('Failed to build experiment %s', e)
        experiment.set_status(ExperimentLifeCycle.FAILED,
                              message='Failed to build image for experiment.')
        return
    except Repo.DoesNotExist:
        _logger.warning('No code was found for this project')
        experiment.set_status(ExperimentLifeCycle.FAILED,
                              message='No code was found for to build this experiment.')
        return
    except Exception as e:  # Other exceptions
        _logger.warning('Failed to build experiment %s', e)
        experiment.set_status(ExperimentLifeCycle.FAILED,
                              message='Failed to build image for experiment.')
        return

    if not status:
        return

    # Now we can start the experiment
    celery_app.send_task(
        RunnerCeleryTasks.EXPERIMENTS_START,
        kwargs={'experiment_id': experiment_id})
