from faker import Factory as FakerFactory

import factory

from db.models.build_jobs import BuildJob
from factories.factory_users import UserFactory

fake = FakerFactory.create()


class BuildJobFactory(factory.DjangoModelFactory):
    config = {'image': 'busybox'}

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BuildJob
