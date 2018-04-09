from django.contrib import admin

from pipelines.models import (
    Operation,
    OperationRun,
    OperationRunStatus,
    Pipeline,
    PipelineRun,
    PipelineRunStatus,
    Schedule
)


class PipelineRunStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class OperationRunStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Schedule)
admin.site.register(Pipeline)
admin.site.register(Operation)
admin.site.register(PipelineRunStatus, PipelineRunStatusAdmin)
admin.site.register(OperationRunStatus, OperationRunStatusAdmin)
admin.site.register(PipelineRun)
admin.site.register(OperationRun)
