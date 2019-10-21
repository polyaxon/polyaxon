import conf

from options.registry import k8s_secrets

conf.subscribe(k8s_secrets.K8SSecretsBuildJobs)
conf.subscribe(k8s_secrets.K8SSecretsJobs)
conf.subscribe(k8s_secrets.K8SSecretsExperiments)
conf.subscribe(k8s_secrets.K8SSecretsNotebooks)
conf.subscribe(k8s_secrets.K8SSecretsTensorboards)
