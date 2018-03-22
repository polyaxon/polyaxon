import factory

from faker import Factory as FakerFactory

from repos.models import Repo
from factories.factory_projects import ProjectFactory

fake = FakerFactory.create()


class RepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Repo

    project = factory.SubFactory(ProjectFactory)
