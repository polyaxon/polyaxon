from django.contrib import admin

from pipelines.models import (
    Schedule,
    Operation,
    Pipeline,
    OperationRun,
    PipelineRun,
)

admin.site.register(Schedule)
admin.site.register(Pipeline)
admin.site.register(Operation)
admin.site.register(PipelineRun)
admin.site.register(OperationRun)
