import conf

from options.registry import build_jobs

conf.subscribe(build_jobs.BuildJobsBackend)
conf.subscribe(build_jobs.BuildJobsAlwaysPullLatest)
conf.subscribe(build_jobs.BuildJobsLangEnv)
conf.subscribe(build_jobs.BuildJobsDockerImage)
conf.subscribe(build_jobs.BuildJobsImagePullPolicy)
conf.subscribe(build_jobs.BuildJobsSetSecurityContext)
conf.subscribe(build_jobs.KanikoDockerImage)
conf.subscribe(build_jobs.KanikoImagePullPolicy)
