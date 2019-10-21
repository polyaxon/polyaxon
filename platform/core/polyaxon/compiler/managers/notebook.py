from compiler.managers.base import BaseCompileManager
from schemas import NotebookSpecification, kinds


class NotebookCompileManager(BaseCompileManager):
    KIND = kinds.NOTEBOOK
    SPECIFICATION = NotebookSpecification
