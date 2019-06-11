import factory

from db.models.data_stores import DataStore


class DataStoreFactory(factory.DjangoModelFactory):
    name = factory.Sequence("dataset-{}".format)

    class Meta:
        model = DataStore
