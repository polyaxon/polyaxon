from db.models.bookmarks import Bookmark


def remove_bookmarks(object_id: int, content_type: str) -> None:
    # Remove any bookmark
    Bookmark.objects.filter(content_type__model=content_type, object_id=object_id).delete()
