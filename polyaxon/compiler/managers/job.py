from compiler.managers.base import BaseCompileManager
from schemas import JobSpecification, kinds


class JobCompileManager(BaseCompileManager):
    KIND = kinds.JOB
    SPECIFICATION = JobSpecification
