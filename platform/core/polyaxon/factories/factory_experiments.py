import factory

from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import (
    Experiment,
    ExperimentChartView,
    ExperimentMetric,
    ExperimentStatus
)
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from factories.fixtures import exec_experiment_spec_parsed_content


class ExperimentFactory(factory.DjangoModelFactory):
    content = exec_experiment_spec_parsed_content.raw_data

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Experiment


class ExperimentStatusFactory(factory.DjangoModelFactory):
    experiment = factory.SubFactory(ExperimentFactory)

    class Meta:
        model = ExperimentStatus


class ExperimentMetricFactory(factory.DjangoModelFactory):
    experiment = factory.SubFactory(ExperimentFactory)
    values = {'accuracy': 0.9}

    class Meta:
        model = ExperimentMetric


class ExperimentChartViewFactory(factory.DjangoModelFactory):
    experiment = factory.SubFactory(ExperimentFactory)
    charts = [{'uuid': 'id1'}, {'uuid': 'id2'}]

    class Meta:
        model = ExperimentChartView


class ExperimentJobFactory(factory.DjangoModelFactory):
    definition = {}
    experiment = factory.SubFactory(ExperimentFactory)

    class Meta:
        model = ExperimentJob


class ExperimentJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(ExperimentJobFactory)

    class Meta:
        model = ExperimentJobStatus
