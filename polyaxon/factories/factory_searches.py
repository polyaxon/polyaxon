from faker import Factory as FakerFactory

import factory

from constants import content_types
from db.models.searches import Search
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory

fake = FakerFactory.create()


class SearchFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    content_type = content_types.EXPERIMENT
    query = {'query': 'user.id: 1|2, project.id: 1|2', 'sort': '-updated_at'}

    class Meta:
        model = Search
