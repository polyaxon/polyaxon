from django.contrib import admin

from libs.admin import DiffModelAdmin
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


class ScheduleAdmin(DiffModelAdmin):
    pass


class PipelineAdmin(DiffModelAdmin):
    pass


class OperationAdmin(DiffModelAdmin):
    pass


class PipelineRunAdmin(DiffModelAdmin):
    pass


class OperationRunAdmin(DiffModelAdmin):
    pass


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(PipelineRunStatus, PipelineRunStatusAdmin)
admin.site.register(OperationRunStatus, OperationRunStatusAdmin)
admin.site.register(PipelineRun, PipelineRunAdmin)
admin.site.register(OperationRun, OperationRunAdmin)
