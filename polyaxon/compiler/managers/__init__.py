from compiler.managers.build import BuildCompileManager
from compiler.managers.experiment import ExperimentCompileManager
from compiler.managers.experiment_group import GroupCompileManager
from compiler.managers.job import JobCompileManager
from compiler.managers.notebook import NotebookCompileManager
from compiler.managers.tensorboad import TensorboardCompileManager

MAPPING = {
    ExperimentCompileManager.KIND: ExperimentCompileManager,
    GroupCompileManager.KIND: GroupCompileManager,
    BuildCompileManager.KIND: BuildCompileManager,
    JobCompileManager.KIND: JobCompileManager,
    TensorboardCompileManager.KIND: TensorboardCompileManager,
    NotebookCompileManager.KIND: NotebookCompileManager,
}
