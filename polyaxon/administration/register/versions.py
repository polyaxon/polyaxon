from administration.register.utils import ReadOnlyAdmin
from db.models.versions import ChartVersion, CliVersion, LibVersion, PlatformVersion


class CliVersionAdmin(ReadOnlyAdmin):
    pass


class LibVersionAdmin(ReadOnlyAdmin):
    pass


class PlatformVersionAdmin(ReadOnlyAdmin):
    pass


class ChartVersionAdmin(ReadOnlyAdmin):
    pass


def register(admin_register):
    admin_register(CliVersion, CliVersionAdmin)
    admin_register(LibVersion, LibVersionAdmin)
    admin_register(PlatformVersion, PlatformVersionAdmin)
    admin_register(ChartVersion, ChartVersionAdmin)
