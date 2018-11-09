from django.contrib.admin import site

from db.models.owner import Owner

site.register(Owner)
