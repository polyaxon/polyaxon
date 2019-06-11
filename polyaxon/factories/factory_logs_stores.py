import factory

from db.models.logs_stores import LogsStore


class LogsStoreFactory(factory.DjangoModelFactory):
    name = factory.Sequence("logs-{}".format)

    class Meta:
        model = LogsStore
