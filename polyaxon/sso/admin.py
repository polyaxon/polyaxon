from django.contrib import admin

from libs.admin import DiffModelAdmin
from sso.models import SSOIdentity, SSOProvider


class SSOIdentityAdmin(DiffModelAdmin):
    pass


class SSOProviderAdmin(DiffModelAdmin):
    pass


admin.site.register(SSOIdentity, SSOIdentityAdmin)
admin.site.register(SSOProvider, SSOProviderAdmin)
