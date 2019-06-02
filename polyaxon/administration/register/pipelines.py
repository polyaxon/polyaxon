from django.contrib import admin

from administration.register.utils import DiffModelAdmin
from db.models.operations import Operation, OperationRun
from db.models.pipelines import Pipeline, PipelineRun, PipelineRunStatus
from db.models.schedules import Schedule


class PipelineRunStatusAdmin(admin.ModelAdmin):
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


def register(admin_register):
    admin_register(Schedule, ScheduleAdmin)
    admin_register(Pipeline, PipelineAdmin)
    admin_register(Operation, OperationAdmin)
    admin_register(PipelineRunStatus, PipelineRunStatusAdmin)
    admin_register(PipelineRun, PipelineRunAdmin)
    admin_register(OperationRun, OperationRunAdmin)
