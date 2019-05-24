from db.models.abstract.store_catalog import StoreCatalogModel


class DataStore(StoreCatalogModel):

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
