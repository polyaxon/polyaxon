from db.models.abstract.store_catalog import StoreCatalogModel


class ArtifactsStore(StoreCatalogModel):

    class Meta(StoreCatalogModel.Meta):
        app_label = 'db'
