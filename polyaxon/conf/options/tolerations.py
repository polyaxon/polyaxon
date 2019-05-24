import conf

from options.registry import tolerations

conf.subscribe(tolerations.TolerationsBuildJobs)
conf.subscribe(tolerations.TolerationsJobs)
conf.subscribe(tolerations.TolerationsExperiments)
conf.subscribe(tolerations.TolerationsNotebooks)
conf.subscribe(tolerations.TolerationsTensorboards)
