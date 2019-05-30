import conf

from options.registry import registries

conf.subscribe(registries.RegistryInCluster)
conf.subscribe(registries.RegistryLocalHost)
conf.subscribe(registries.RegistryHost)
