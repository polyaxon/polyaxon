import factory

from factories.factory_users import UserFactory
from projects.models import Project


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "project-{}".format(x))

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
