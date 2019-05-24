import conf

from options.registry import auth_azure

conf.subscribe(auth_azure.AuthAzureEnabled)
conf.subscribe(auth_azure.AuthAzureVerificationSchedule)
conf.subscribe(auth_azure.AuthAzureTenantId)
conf.subscribe(auth_azure.AuthAzureClientId)
conf.subscribe(auth_azure.AuthAzureClientSecret)
