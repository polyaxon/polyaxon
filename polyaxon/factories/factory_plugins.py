from faker import Factory as FakerFactory

import factory

from db.models.notebooks import NotebookJob
from db.models.tensorboards import TensorboardJob
from factories.factory_users import UserFactory
from factories.fixtures import notebook_spec_parsed_content, tensorboard_spec_parsed_content

fake = FakerFactory.create()


class TensorboardJobFactory(factory.DjangoModelFactory):
    config = tensorboard_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = TensorboardJob


class NotebookJobFactory(factory.DjangoModelFactory):
    config = notebook_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = NotebookJob
