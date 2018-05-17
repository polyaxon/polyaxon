from libs.wizards import WizardManager
from sso.providers.github_provider import GitHubIdentityProvider

default_manager = WizardManager()
subscribe = default_manager.subscribe

subscribe(GitHubIdentityProvider)
