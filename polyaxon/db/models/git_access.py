from db.models.abstract.access_catalog import HostAccessCatalog


class GitAccess(HostAccessCatalog):
    class Meta(HostAccessCatalog.Meta):
        pass
