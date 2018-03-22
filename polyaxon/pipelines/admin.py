from django.contrib import admin

from pipelines.models import Schedule, Task, Pipeline

admin.site.register(Schedule)
admin.site.register(Pipeline)
admin.site.register(Task)
