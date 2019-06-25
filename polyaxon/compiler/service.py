from typing import Optional

from hestia.service_interface import Service

from compiler import managers
from compiler.execptions import CompilerError


class CompilerService(Service):
    __all__ = ('compile',)

    @classmethod
    def compile(cls, kind: str, content: str) -> Optional['BaseSpecification']:
        if not content:
            return None

        if kind not in managers.MAPPING:
            raise CompilerError('Specification with Kind `{}` was not configured'.format(kind))
        return managers.MAPPING[kind].compile(content=content)
