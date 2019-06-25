from query.managers.build import BuildQueryManager
from query.managers.experiment import ExperimentQueryManager
from query.managers.experiment_group import ExperimentGroupQueryManager
from query.managers.job import JobQueryManager
from query.managers.notebook import NotebookQueryManager
from query.managers.tensorboad import TensorboardQueryManager

MAPPING = {
    ExperimentQueryManager.NAME: ExperimentQueryManager,
    ExperimentGroupQueryManager.NAME: ExperimentGroupQueryManager,
    BuildQueryManager.NAME: BuildQueryManager,
    JobQueryManager.NAME: JobQueryManager,
    TensorboardQueryManager.NAME: TensorboardQueryManager,
    NotebookQueryManager.NAME: NotebookQueryManager,
}
