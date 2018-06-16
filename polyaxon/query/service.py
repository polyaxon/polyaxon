from libs.services import Service
from query.managers.experiment import ExperimentQueryManager
from query.managers.experiment_group import ExperimentGroupQueryManager
from query.managers.job import JobQueryManager


class BuildQueryManager(object):
    pass


class QueryService(Service):
    __all__ = ('setup',
               'query_experiments',
               'query_experiment_groups',
               'query_jobs',
               'query_builds')

    @staticmethod
    def query_experiments(query_spec, queryset):
        return ExperimentQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def query_experiment_groups(query_spec, queryset):
        return ExperimentGroupQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def query_jobs(query_spec, queryset):
        return JobQueryManager.apply(query_spec=query_spec, queryset=queryset)

    @staticmethod
    def query_builds(query_spec, queryset):
        return BuildQueryManager.apply(query_spec=query_spec, queryset=queryset)
