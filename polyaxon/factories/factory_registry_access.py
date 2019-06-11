import factory

from db.models.registry_access import RegistryAccess


class RegistryAccessFactory(factory.DjangoModelFactory):
    name = factory.Sequence("registry-access-{}".format)

    class Meta:
        model = RegistryAccess
