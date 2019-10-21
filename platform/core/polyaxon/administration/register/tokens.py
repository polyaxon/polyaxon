from administration.register.utils import DiffModelAdmin
from db.models.tokens import Token


class TokenAdmin(DiffModelAdmin):
    list_display = ('user', 'started_at', 'is_expired', ) + DiffModelAdmin.list_display


def register(admin_register):
    admin_register(Token, TokenAdmin)
