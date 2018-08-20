from django.contrib.admin import site

from db.models.bookmarks import Bookmark

site.register(Bookmark)
