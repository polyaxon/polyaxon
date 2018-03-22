import factory

from experiments.models import (
    Experiment,
    ExperimentStatus,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,)
from factories.factory_projects import ProjectFactory

from factories.factory_users import UserFactory
from factories.fixtures import exec_experiment_spec_parsed_content


class ExperimentFactory(factory.DjangoModelFactory):
    config = exec_experiment_spec_parsed_content.parsed_data

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


class ExperimentJobFactory(factory.DjangoModelFactory):
    definition = {}
    experiment = factory.SubFactory(ExperimentFactory)

    class Meta:
        model = ExperimentJob


class ExperimentJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(ExperimentJobFactory)

    class Meta:
        model = ExperimentJobStatus
