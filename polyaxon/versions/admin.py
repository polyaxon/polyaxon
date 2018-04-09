from django.contrib import admin

from libs.admin import ReadOnlyAdmin
from versions.models import ChartVersion, CliVersion, LibVersion, PlatformVersion


class CliVersionAdmin(ReadOnlyAdmin):
    pass


class LibVersionAdmin(ReadOnlyAdmin):
    pass


class PlatformVersionAdmin(ReadOnlyAdmin):
    pass


class ChartVersionAdmin(ReadOnlyAdmin):
    pass


admin.site.register(CliVersion, CliVersionAdmin)
admin.site.register(LibVersion, LibVersionAdmin)
admin.site.register(PlatformVersion, PlatformVersionAdmin)
admin.site.register(ChartVersion, ChartVersionAdmin)
