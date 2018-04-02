import factory

from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from pipelines.models import Pipeline, Operation, PipelineRun, OperationRun


class PipelineFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "pipeline-{}".format(x))
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Pipeline


class OperationFactory(factory.DjangoModelFactory):
    pipeline = factory.SubFactory(PipelineFactory)

    class Meta:
        model = Operation


class PipelineRunFactory(factory.DjangoModelFactory):
    pipeline = factory.SubFactory(PipelineFactory)

    class Meta:
        model = PipelineRun


class OperationRunFactory(factory.DjangoModelFactory):
    operation = factory.SubFactory(OperationFactory)
    pipeline_run = factory.SubFactory(PipelineRunFactory)

    class Meta:
        model = OperationRun
