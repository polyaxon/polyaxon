import factory

from db.models.git_access import GitAccess


class GitAccessFactory(factory.DjangoModelFactory):
    name = factory.Sequence("git-access-{}".format)

    class Meta:
        model = GitAccess
