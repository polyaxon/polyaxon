import conf

from options.registry import env_vars

conf.subscribe(env_vars.EnvVarsBuildJobs)
conf.subscribe(env_vars.EnvVarsJobs)
conf.subscribe(env_vars.EnvVarsExperiments)
conf.subscribe(env_vars.EnvVarsNotebooks)
conf.subscribe(env_vars.EnvVarsTensorboards)
