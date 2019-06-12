from db.models.abstract.access_catalog import K8SResourceCatalog


class K8SSecret(K8SResourceCatalog):
    """A model to represent a catalog of k8s secrets.

    Since k8s secrets can hold several entries,
    often time the user only requires mounting some of these keys.

    N.B. If no keys are specified, the whole secret will be mounted to the requiting jobs.
    """

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
