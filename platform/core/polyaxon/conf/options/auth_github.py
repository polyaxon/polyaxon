import conf

from options.registry import auth_github

conf.subscribe(auth_github.AuthGithubEnabled)
conf.subscribe(auth_github.AuthGithubVerificationSchedule)
conf.subscribe(auth_github.AuthGithubClientId)
conf.subscribe(auth_github.AuthGithubClientSecret)
