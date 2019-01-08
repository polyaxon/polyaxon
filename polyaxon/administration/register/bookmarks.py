from db.models.bookmarks import Bookmark


def register(admin_register):
    admin_register(Bookmark)
