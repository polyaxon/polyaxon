from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'
    verbose_name = 'Projects'

    def ready(self):
        from projects.signals import (  # noqa
            new_project,
            project_pre_deleted,
            project_post_deleted
        )
