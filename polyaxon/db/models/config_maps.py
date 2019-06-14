from db.models.abstract.access_catalog import K8SResourceCatalog


class K8SConfigMap(K8SResourceCatalog):
    """A model to represent a catalog of config_maps.

    Since k8s config_maps can hold several entries,
    often time the user only requires mounting some of these keys.

    N.B. If no keys are specified, the whole config_map will be mounted to the requiting jobs.
    """

    class Meta(K8SResourceCatalog.Meta):
        app_label = 'db'
