from compiler.managers.base import BaseCompileManager
from schemas import TensorboardSpecification, kinds


class TensorboardCompileManager(BaseCompileManager):
    KIND = kinds.TENSORBOARD
    SPECIFICATION = TensorboardSpecification
