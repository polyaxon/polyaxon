from faker import Factory as FakerFactory

import factory

from db.models.notebooks import NotebookJob, NotebookJobStatus
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from factories.fixtures import notebook_spec_parsed_content, tensorboard_spec_parsed_content

fake = FakerFactory.create()


class TensorboardJobFactory(factory.DjangoModelFactory):
    config = tensorboard_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = TensorboardJob


class NotebookJobFactory(factory.DjangoModelFactory):
    config = notebook_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = NotebookJob


class TensorboardJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(TensorboardJobFactory)

    class Meta:
        model = TensorboardJobStatus


class NotebookJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(NotebookJobFactory)

    class Meta:
        model = NotebookJobStatus
