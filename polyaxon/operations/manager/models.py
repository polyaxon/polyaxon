from constants import content_types
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.tensorboards import TensorboardJob

ENTITY_MODELS = {
    content_types.EXPERIMENT: Experiment,
    content_types.EXPERIMENT_GROUP: ExperimentGroup,
    content_types.BUILD_JOB: BuildJob,
    content_types.JOB: Job,
    content_types.TENSORBOARD_JOB: TensorboardJob,
    content_types.NOTEBOOK_JOB: NotebookJob,
}
