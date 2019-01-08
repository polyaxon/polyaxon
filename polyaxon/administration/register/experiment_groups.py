from django.contrib.admin import ModelAdmin

from administration.register.utils import DiffModelAdmin
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupIteration,
    ExperimentGroupStatus
)


class ExperimentGroupAdmin(DiffModelAdmin):
    pass


class ExperimentGroupStatusAdmin(ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentGroupIterationAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(ExperimentGroup, ExperimentGroupAdmin)
    admin_register(ExperimentGroupStatus, ExperimentGroupStatusAdmin)
    admin_register(ExperimentGroupIteration, ExperimentGroupIterationAdmin)
