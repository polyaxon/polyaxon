from django.contrib import admin

from db.admin.jobs import JobStatusAdmin
from db.admin.utils import DiffModelAdmin
from db.models.experiments import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
    ExperimentStatus
)


class ExperimentAdmin(DiffModelAdmin):
    readonly_fields = DiffModelAdmin.readonly_fields + (
        'sequence', 'unique_name', 'last_status', 'dockerfile', 'cloning_strategy', 'declarations')


class ExperimentStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentMetricAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentJobAdmin(DiffModelAdmin):
    readonly_fields = DiffModelAdmin.readonly_fields + ('sequence', 'unique_name', 'last_status')


class ExperimentJobStatusAdmin(JobStatusAdmin):
    pass


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentStatus, ExperimentStatusAdmin)
admin.site.register(ExperimentMetric, ExperimentMetricAdmin)
admin.site.register(ExperimentJob, ExperimentJobAdmin)
admin.site.register(ExperimentJobStatus, ExperimentJobStatusAdmin)
