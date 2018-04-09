from django.apps import AppConfig


class ReposConfig(AppConfig):
    name = 'repos'
    verbose_name = 'Repos'

    def ready(self):
        from repos.signals import new_repo, new_external_repo, repo_deleted, external_repo_deleted   # noqa
