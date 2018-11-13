from api.endpoint.project import ProjectResourceEndpoint


class JobEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id', )
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('job',)
    lookup_url_kwarg = 'job_id'

    def _initialize_context(self):
        super()._initialize_context()
        self.job = self.get_object()
