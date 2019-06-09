import conf

from options.registry import k8s_resources

conf.subscribe(k8s_resources.K8SResourcesJobs)
conf.subscribe(k8s_resources.K8SResourcesBuildJobs)
conf.subscribe(k8s_resources.K8SResourcesExperiments)
conf.subscribe(k8s_resources.K8SResourcesNotebooks)
conf.subscribe(k8s_resources.K8SResourcesTensorboards)
