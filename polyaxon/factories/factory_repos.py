from faker import Factory as FakerFactory

import factory

from db.models.repos import Repo, ExternalRepo
from factories.factory_projects import ProjectFactory

fake = FakerFactory.create()


class RepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Repo

    project = factory.SubFactory(ProjectFactory)


class ExternalRepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = ExternalRepo

    project = factory.SubFactory(ProjectFactory)
