from faker import Factory as FakerFactory

import factory

from factories.factory_users import UserFactory
from factories.fixtures import plugin_spec_parsed_content
from db.models.plugins import NotebookJob, TensorboardJob

fake = FakerFactory.create()


class TensorboardJobFactory(factory.DjangoModelFactory):
    config = plugin_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = TensorboardJob


class NotebookJobFactory(factory.DjangoModelFactory):
    config = plugin_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = NotebookJob
