from rest_framework.generics import get_object_or_404

from api.endpoint.project import ProjectResourceEndpoint
from db.models.notebooks import NotebookJob


class NotebookEndpoint(ProjectResourceEndpoint):
    queryset = NotebookJob.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)
    lookup_url_kwarg = 'job_id'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.notebook = self.get_object()


class ProjectNotebookEndpoint(ProjectResourceEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.notebook)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        project = self.project

        self.notebook = project.notebook


class NotebookResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)
    lookup_url_kwarg = 'job_id'

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.notebook)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.notebook = get_object_or_404(NotebookJob,
                                          id=self.job_id,
                                          project=self.project)
