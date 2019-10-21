import conf

from options.registry import auth_gitlab

conf.subscribe(auth_gitlab.AuthGitlabEnabled)
conf.subscribe(auth_gitlab.AuthGitlabVerificationSchedule)
conf.subscribe(auth_gitlab.AuthGitlabUrl)
conf.subscribe(auth_gitlab.AuthGitlabClientId)
conf.subscribe(auth_gitlab.AuthGitlabClientSecret)
