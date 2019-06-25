from compiler.managers.base import BaseCompileManager
from schemas import BuildSpecification, kinds


class BuildCompileManager(BaseCompileManager):
    KIND = kinds.BUILD
    SPECIFICATION = BuildSpecification
