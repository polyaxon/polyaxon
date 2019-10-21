from compiler.managers.base import BaseCompileManager
from schemas import ExperimentSpecification, kinds


class ExperimentCompileManager(BaseCompileManager):
    KIND = kinds.EXPERIMENT
    SPECIFICATION = ExperimentSpecification
