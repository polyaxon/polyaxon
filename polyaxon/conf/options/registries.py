import conf

from options.registry import registries

conf.subscribe(registries.RegistryInCluster)
conf.subscribe(registries.RegistryUser)
conf.subscribe(registries.RegistryPassword)
conf.subscribe(registries.RegistryLocalUri)
conf.subscribe(registries.RegistryUri)
