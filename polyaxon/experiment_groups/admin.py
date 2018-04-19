from django.contrib import admin

from experiment_groups.models import ExperimentGroup, ExperimentGroupIteration
from libs.admin import DiffModelAdmin


class ExperimentGroupAdmin(DiffModelAdmin):
    pass


class ExperimentGroupIterationAdmin(DiffModelAdmin):
    pass


admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
admin.site.register(ExperimentGroupIteration, ExperimentGroupIterationAdmin)
