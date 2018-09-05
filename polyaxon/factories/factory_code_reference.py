
from faker import Factory as FakerFactory

import factory

from db.models.repos import CodeReference
from factories.factory_repos import RepoFactory

fake = FakerFactory.create()


class CodeReferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = CodeReference

    repo = factory.SubFactory(RepoFactory)
    commit = factory.Sequence('commit{}'.format)
