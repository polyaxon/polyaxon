from django.contrib import admin

from administration.register.abstract_job import JobStatusAdmin
from administration.register.utils import DiffModelAdmin, ReadOnlyAdmin
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import Experiment, ExperimentMetric, ExperimentStatus


class ExperimentLightAdmin(DiffModelAdmin, ReadOnlyAdmin):
    list_display = ('id', 'user', 'project', 'name', 'last_status', 'framework',
                    'created_at', 'updated_at', 'started_at', 'finished_at',)
    fields = (
        'project',
        'name',
        'description',
        'backend',
        'framework',
        'last_status',
        'created_at',
        'updated_at',
        'started_at',
        'finished_at',
    )
    readonly_fields = ('last_status',)


def register_light(admin_register):
    admin_register(Experiment, ExperimentLightAdmin)


class ExperimentAdmin(DiffModelAdmin):
    readonly_fields = DiffModelAdmin.readonly_fields + (
        'id', 'unique_name', 'last_status', 'cloning_strategy', 'params')


class ExperimentStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentMetricAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentJobAdmin(DiffModelAdmin):
    readonly_fields = DiffModelAdmin.readonly_fields + ('id', 'unique_name', 'last_status')


class ExperimentJobStatusAdmin(JobStatusAdmin):
    pass


def register(admin_register):
    admin_register(Experiment, ExperimentAdmin)
    admin_register(ExperimentStatus, ExperimentStatusAdmin)
    admin_register(ExperimentMetric, ExperimentMetricAdmin)
    admin_register(ExperimentJob, ExperimentJobAdmin)
    admin_register(ExperimentJobStatus, ExperimentJobStatusAdmin)
