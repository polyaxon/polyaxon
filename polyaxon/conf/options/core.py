import conf

from options.registry import core

conf.subscribe(core.PasswordLength)
conf.subscribe(core.AdminViewEnabled)
conf.subscribe(core.Logging)
conf.subscribe(core.Debug)
conf.subscribe(core.Protocol)
conf.subscribe(core.ApiHost)
conf.subscribe(core.LoginUrl)
conf.subscribe(core.AccountActivationDays)
conf.subscribe(core.CeleryBrokerBackend)
conf.subscribe(core.CeleryBrokerUrl)
conf.subscribe(core.HeadersInternal)
conf.subscribe(core.SecretInternalToken)
conf.subscribe(core.HealthCheckWorkerTimeout)
conf.subscribe(core.ClusterNotificationAliveUrl)
conf.subscribe(core.ClusterNotificationUrl)
conf.subscribe(core.ClusterNotificationNodesUrl)
conf.subscribe(core.SecurityContextUser)
conf.subscribe(core.SecurityContextGroup)
conf.subscribe(core.EncryptionKey)
conf.subscribe(core.EncryptionSecret)
