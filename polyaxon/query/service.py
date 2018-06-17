from libs.services import Service
from query.managers.build import BuildQueryManager
from query.managers.experiment import ExperimentQueryManager
from query.managers.experiment_group import ExperimentGroupQueryManager
from query.managers.job import JobQueryManager


class QueryService(Service):
    __all__ = ('setup', 'filter_queryset')

    @classmethod
    def filter_queryset(cls, manager, query_spec, queryset):
        if manager == ExperimentQueryManager.NAME:
            return cls.filter_experiments(query_spec=query_spec, queryset=queryset)
        if manager == ExperimentGroupQueryManager.NAME:
            return cls.filter_experiment_groups(query_spec=query_spec, queryset=queryset)
        if manager == BuildQueryManager.NAME:
            return cls.filter_builds(query_spec=query_spec, queryset=queryset)
        if manager == JobQueryManager.NAME:
            return cls.filter_jobs(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def filter_experiments(query_spec, queryset):
        return ExperimentQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def filter_experiment_groups(query_spec, queryset):
        return ExperimentGroupQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def filter_jobs(query_spec, queryset):
        return JobQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def filter_builds(query_spec, queryset):
        return BuildQueryManager.apply(query_spec=query_spec, queryset=queryset)
