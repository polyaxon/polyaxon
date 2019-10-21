import conf

from options.registry import k8s_config_maps

conf.subscribe(k8s_config_maps.K8SConfigMapsBuildJobs)
conf.subscribe(k8s_config_maps.K8SConfigMapsJobs)
conf.subscribe(k8s_config_maps.K8SConfigMapsExperiments)
conf.subscribe(k8s_config_maps.K8SConfigMapsNotebooks)
conf.subscribe(k8s_config_maps.K8SConfigMapsTensorboards)
