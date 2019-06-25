from compiler.managers.base import BaseCompileManager
from schemas import PipelineSpecification, kinds


class PipelineCompileManager(BaseCompileManager):
    KIND = kinds.PIPELINE
    SPECIFICATION = PipelineSpecification
