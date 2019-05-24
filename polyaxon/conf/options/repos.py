import conf

from options.registry import repos

conf.subscribe(repos.ReposAccessToken)
conf.subscribe(repos.ReposCredentials)
