import factory

from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from pipelines.models import Pipeline, Operation


class PipelineFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Pipeline


class OperationFactory(factory.DjangoModelFactory):
    pipeline = factory.SubFactory(PipelineFactory)

    class Meta:
        model = Operation
