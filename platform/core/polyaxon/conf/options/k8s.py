import conf

from options.registry import k8s

conf.subscribe(k8s.K8SNamespace)
conf.subscribe(k8s.K8SConfig)
conf.subscribe(k8s.K8SNodeName)
conf.subscribe(k8s.K8SRBACEnabled)
conf.subscribe(k8s.K8SIngressEnabled)
conf.subscribe(k8s.K8SIngressAnnotations)
conf.subscribe(k8s.K8SServiceAccountName)
conf.subscribe(k8s.K8SServiceAccountExperiments)
conf.subscribe(k8s.K8SServiceAccountJobs)
conf.subscribe(k8s.K8SServiceAccountBuilds)
conf.subscribe(k8s.K8SGpuResourceKey)
conf.subscribe(k8s.K8STpuTfVersion)
conf.subscribe(k8s.K8STpuResourceKey)
