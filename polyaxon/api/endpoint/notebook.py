from api.endpoint.project import ProjectResourceEndpoint


class NotebookResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('notebook',)

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.notebook)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        project = self.project

        self.notebook = project.notebook
