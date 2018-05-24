from django.contrib import admin

from db.admin.utils import DiffModelAdmin
from db.models.sso import SSOIdentity


class SSOIdentityAdmin(DiffModelAdmin):
    pass


admin.site.register(SSOIdentity, SSOIdentityAdmin)
