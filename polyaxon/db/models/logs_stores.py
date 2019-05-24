from db.models.abstract.store_catalog import StoreCatalogModel


class LogsStore(StoreCatalogModel):

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
