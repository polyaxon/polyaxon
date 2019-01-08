from administration.register.utils import DiffModelAdmin
from db.models.tokens import Token


class TokenAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(Token, TokenAdmin)
