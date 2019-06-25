from typing import Any, Optional, Tuple

from hestia.service_interface import Service

from query import managers
from query.exceptions import QueryError
from query.parser import parse_field


class QueryService(Service):
    __all__ = ('filter_queryset', 'parse_field',)

    @classmethod
    def filter_queryset(cls, manager: str, query_spec: str, queryset: Any) -> Any:
        if manager not in managers.MAPPING:
            raise QueryError('Manager `{}` was not configured'.format(manager))
        return managers.MAPPING[manager].apply(query_spec=query_spec, queryset=queryset)

    @classmethod
    def parse_field(cls, field: str) -> Tuple[str, Optional[str]]:
        return parse_field(field=field)
