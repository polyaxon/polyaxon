from django.contrib import admin

from libs.admin import DiffModelAdmin
from sso.models import SSOIdentity


class SSOIdentityAdmin(DiffModelAdmin):
    pass


admin.site.register(SSOIdentity, SSOIdentityAdmin)
