import conf

from options.registry import spawner

conf.subscribe(spawner.RoleLabelsWorker)
conf.subscribe(spawner.RoleLabelsDashboard)
conf.subscribe(spawner.RoleLabelsLog)
conf.subscribe(spawner.RoleLabelsApi)
conf.subscribe(spawner.RoleLabelsConfig)
conf.subscribe(spawner.RoleLabelsHooks)
conf.subscribe(spawner.TypeLabelsCore)
conf.subscribe(spawner.TypeLabelsRunner)
conf.subscribe(spawner.AppLabelsTensorboard)
conf.subscribe(spawner.AppLabelsNotebook)
conf.subscribe(spawner.AppLabelsDockerizer)
conf.subscribe(spawner.AppLabelsExperiment)
conf.subscribe(spawner.AppLabelsJob)
conf.subscribe(spawner.DnsUseResolver)
conf.subscribe(spawner.DnsCustomCluster)
conf.subscribe(spawner.Plugins)
conf.subscribe(spawner.PublicPluginJobs)
conf.subscribe(spawner.RefsConfigMaps)
conf.subscribe(spawner.RefsSecrets)
conf.subscribe(spawner.RestrictK8SResources)
