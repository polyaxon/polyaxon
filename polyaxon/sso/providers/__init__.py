from libs.wizards import WizardManager
from sso.providers.bitbucket_provider import BitbucketIdentityProvider
from sso.providers.github_provider import GitHubIdentityProvider
from sso.providers.gitlab_provider import GitLabIdentityProvider

default_manager = WizardManager()
subscribe = default_manager.subscribe

subscribe(BitbucketIdentityProvider)
subscribe(GitHubIdentityProvider)
subscribe(GitLabIdentityProvider)
