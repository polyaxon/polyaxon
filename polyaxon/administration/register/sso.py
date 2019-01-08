from administration.register.utils import DiffModelAdmin
from db.models.sso import SSOIdentity


class SSOIdentityAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(SSOIdentity, SSOIdentityAdmin)
