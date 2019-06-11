import factory

from db.models.artifacts_stores import ArtifactsStore


class ArtifactsStoreFactory(factory.DjangoModelFactory):
    name = factory.Sequence("artifact-{}".format)

    class Meta:
        model = ArtifactsStore
