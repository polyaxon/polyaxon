from db.models.abstract.access_catalog import HostAccessCatalog


class RegistryAccess(HostAccessCatalog):
    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
