from faker import Factory as FakerFactory

import factory

from db.models.ci import CI
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory

fake = FakerFactory.create()


class CIFactory(factory.DjangoModelFactory):
    class Meta:
        model = CI

    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
