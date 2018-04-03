import factory

from projects.models import Project

from factories.factory_users import UserFactory


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "project-{}".format(x))

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
