from db.models.abstract.store_catalog import StoreCatalogModel


class ArtifactsStore(StoreCatalogModel):

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
