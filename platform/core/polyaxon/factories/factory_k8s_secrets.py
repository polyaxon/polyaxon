import factory

from db.models.secrets import K8SSecret


class K8SSecretFactory(factory.DjangoModelFactory):
    name = factory.Sequence("k8s-secret-{}".format)

    class Meta:
        model = K8SSecret
