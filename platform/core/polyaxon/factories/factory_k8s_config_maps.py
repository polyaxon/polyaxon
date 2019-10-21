import factory

from db.models.config_maps import K8SConfigMap


class K8SConfigMapFactory(factory.DjangoModelFactory):
    name = factory.Sequence("k8s-config-map-{}".format)

    class Meta:
        model = K8SConfigMap
