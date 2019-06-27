import conf

from options.registry import restarts

conf.subscribe(restarts.MaxRestartsBuildJobs)
conf.subscribe(restarts.MaxRestartsJobs)
conf.subscribe(restarts.MaxRestartsExperiments)
conf.subscribe(restarts.MaxRestartsNotebooks)
conf.subscribe(restarts.MaxRestartsTensorboards)
