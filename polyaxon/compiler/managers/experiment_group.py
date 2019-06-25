from compiler.managers.base import BaseCompileManager
from schemas import GroupSpecification, kinds


class GroupCompileManager(BaseCompileManager):
    KIND = kinds.GROUP
    SPECIFICATION = GroupSpecification
