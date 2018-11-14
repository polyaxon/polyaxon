from django.contrib.admin import site

from db.admin.utils import DiffModelAdmin
from db.models.tokens import Token


class TokenAdmin(DiffModelAdmin):
    pass


site.register(Token, TokenAdmin)
