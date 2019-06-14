from db.models.abstract.store_catalog import StoreCatalogModel


class LogsStore(StoreCatalogModel):

    class Meta(StoreCatalogModel.Meta):
        app_label = 'db'
