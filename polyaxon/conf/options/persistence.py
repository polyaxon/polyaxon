import conf

from options.registry import persistence

conf.subscribe(persistence.ReposClaimNAme)
conf.subscribe(persistence.ReposHostPath)
conf.subscribe(persistence.ReposMountPath)
conf.subscribe(persistence.UploadMountPath)
conf.subscribe(persistence.PersistenceData)
conf.subscribe(persistence.PersistenceOutputs)
conf.subscribe(persistence.PersistenceLogs)
