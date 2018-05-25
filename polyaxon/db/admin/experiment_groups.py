from django.contrib import admin

from db.admin.utils import DiffModelAdmin
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupIteration,
    ExperimentGroupStatus
)


class ExperimentGroupAdmin(DiffModelAdmin):
    pass


class ExperimentGroupStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentGroupIterationAdmin(DiffModelAdmin):
    pass


admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
admin.site.register(ExperimentGroupStatus, ExperimentGroupStatusAdmin)
admin.site.register(ExperimentGroupIteration, ExperimentGroupIterationAdmin)
