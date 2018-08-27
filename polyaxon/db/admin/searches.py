from django.contrib.admin import site

from db.models.searches import Search

site.register(Search)
