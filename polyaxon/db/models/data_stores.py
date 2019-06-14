from db.models.abstract.store_catalog import StoreCatalogModel


class DataStore(StoreCatalogModel):

    class Meta(StoreCatalogModel.Meta):
        app_label = 'db'
