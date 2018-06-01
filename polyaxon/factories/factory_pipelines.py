import factory

from db.models.pipelines import Operation, OperationRun, Pipeline, PipelineRun
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory


class PipelineFactory(factory.DjangoModelFactory):
    name = factory.Sequence("pipeline-{}".format)
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
