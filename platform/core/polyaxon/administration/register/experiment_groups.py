from django.contrib.admin import ModelAdmin

from administration.register.utils import DiffModelAdmin, ReadOnlyAdmin
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupIteration,
    ExperimentGroupStatus
)


class ExperimentGroupLightAdmin(DiffModelAdmin, ReadOnlyAdmin):
    list_display = ('id', 'user', 'project', 'name', 'last_status', 'concurrency', 'group_type',
                    'created_at', 'updated_at', 'started_at', 'finished_at',)
    fields = (
        'user',
        'project',
        'name',
        'description',
        'backend',
        'group_type'
        'algorithm',
        'concurrency',
        'last_status',
        'created_at',
        'updated_at',
        'started_at',
        'finished_at',
    )
    readonly_fields = ('last_status',)


def register_light(admin_register):
    admin_register(ExperimentGroup, ExperimentGroupLightAdmin)


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
