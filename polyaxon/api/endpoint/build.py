from api.endpoint.project import ProjectResourceEndpoint


class BuildEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('build_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('build',)
    lookup_url_kwarg = 'build_id'

    def _initialize_context(self):
        super()._initialize_context()
        self.build = self.get_object()
