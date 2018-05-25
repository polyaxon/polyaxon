from faker import Factory as FakerFactory

import factory

from db.models.repos import Repo
from factories.factory_projects import ProjectFactory

fake = FakerFactory.create()


class RepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Repo

    project = factory.SubFactory(ProjectFactory)
