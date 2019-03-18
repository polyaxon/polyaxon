from rest_framework.generics import get_object_or_404

import auditor

from api.endpoint.project import ProjectEndpoint, ProjectResourceEndpoint
from db.models.notebooks import NotebookJob
from scopes.authentication.utils import is_user


class NotebookEndpoint(ProjectEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)
    notebook_queryset = NotebookJob.objects
    NOTEBOOK_AUDITOR_EVENT_TYPES = None

    def get_object(self):
        project = super().get_object()

        notebook = get_object_or_404(self.notebook_queryset, project=project)

        if not self.NOTEBOOK_AUDITOR_EVENT_TYPES:
            return notebook

        method = self.request.method
        event_type = self.NOTEBOOK_AUDITOR_EVENT_TYPES.get(method)
        if method == 'GET' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=notebook,
                           actor_id=self.request.user.id,
                           target='project',
                           actor_name=self.request.user.username)
        elif method == 'DELETE' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=notebook,
                           actor_id=self.request.user.id,
                           target='project',
                           actor_name=self.request.user.username)
        return notebook

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        self.notebook = self.get_object()
        self.project = self.notebook.project
        self.owner = self.notebook.project.owner


class NotebookResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.notebook)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        project = self.project

        self.notebook = project.notebook
