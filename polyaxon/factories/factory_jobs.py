from faker import Factory as FakerFactory

import factory

from db.models.jobs import Job
from factories.factory_users import UserFactory
from factories.fixtures import job_spec_parsed_content

fake = FakerFactory.create()


class JobFactory(factory.DjangoModelFactory):
    config = job_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Job
