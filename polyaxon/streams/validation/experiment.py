from django.core.exceptions import ValidationError

from db.models.experiments import Experiment
from streams.validation.project import validate_project


def validate_experiment(request, username, project_name, experiment_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        experiment = Experiment.objects.get(project=project, id=experiment_id)
    except (Experiment.DoesNotExist, ValidationError):
        return None, 'Experiment was not found'
    if experiment.is_done:
        return None, 'Experiment is not running, current status: {}'.format(
            experiment.last_status
        )
    return experiment, None
