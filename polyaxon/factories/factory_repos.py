from faker import Factory as FakerFactory

import factory

from factories.factory_projects import ProjectFactory
from models.repos import Repo

fake = FakerFactory.create()


class RepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Repo

    project = factory.SubFactory(ProjectFactory)
