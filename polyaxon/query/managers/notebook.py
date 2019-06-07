from query.builder import ArrayCondition, DateTimeCondition, SearchCondition, ValueCondition
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_search_operation, parse_value_operation


class NotebookQueryManager(BaseQueryManager):
    NAME = 'notebook'
    FIELDS_PROXY = {
        'status': 'status__status',
    }
    PARSERS_BY_FIELD = {
        # Id
        'id': parse_value_operation,
        # Dates
        'created_at': parse_datetime_operation,
        'updated_at': parse_datetime_operation,
        'started_at': parse_datetime_operation,
        'finished_at': parse_datetime_operation,
        # Name
        'name': parse_search_operation,
        # Description
        'description': parse_search_operation,
        # User
        'user': parse_value_operation,
        # Status
        'status': parse_value_operation,
        # Project
        'project': parse_value_operation,
        # Tags
        'tags': parse_value_operation,
        # Backend
        'backend': parse_value_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Id
        'id': ValueCondition,
        # Dates
        'created_at': DateTimeCondition,
        'updated_at': DateTimeCondition,
        'started_at': DateTimeCondition,
        'finished_at': DateTimeCondition,
        # Name
        'name': SearchCondition,
        # Description
        'description': SearchCondition,
        # User
        'user': ValueCondition,
        # Status
        'status': ValueCondition,
        # Tags
        'tags': ArrayCondition,
        # Project
        'project': ValueCondition,
        # Backend
        'backend': ValueCondition,
    }
