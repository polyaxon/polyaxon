from libs.services import Service
from query.managers.build import BuildQueryManager
from query.managers.experiment import ExperimentQueryManager
from query.managers.experiment_group import ExperimentGroupQueryManager
from query.managers.job import JobQueryManager
from query.managers.tensorboad import TensorboardQueryManager
from query.parser import parse_field


class QueryService(Service):
    __all__ = ('setup', 'filter_queryset', 'parse_field')

    @classmethod
    def filter_queryset(cls, manager, query_spec, queryset):
        if manager == ExperimentQueryManager.NAME:
            return ExperimentQueryManager.apply(query_spec=query_spec, queryset=queryset)
        if manager == ExperimentGroupQueryManager.NAME:
            return ExperimentGroupQueryManager.apply(query_spec=query_spec, queryset=queryset)
        if manager == BuildQueryManager.NAME:
            return BuildQueryManager.apply(query_spec=query_spec, queryset=queryset)
        if manager == JobQueryManager.NAME:
            return JobQueryManager.apply(query_spec=query_spec, queryset=queryset)
        if manager == TensorboardQueryManager.NAME:
            return TensorboardQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @classmethod
    def parse_field(cls, field):
        return parse_field(field=field)
