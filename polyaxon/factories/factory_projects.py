import factory

from db.models.projects import Project
from factories.factory_users import UserFactory


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence("project-{}".format)

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
