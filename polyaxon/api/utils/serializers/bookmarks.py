from rest_framework import serializers

from db.models.bookmarks import Bookmark
from scopes.authentication.utils import is_user


class BookmarkedSerializerMixin(serializers.Serializer):
    bookmarked_model = None

    bookmarked = serializers.SerializerMethodField()

    def get_bookmarked(self, obj):
        bookmarks = self.context.get('bookmarks', None)

        if bookmarks is not None:
            return obj.id in bookmarks
        else:
            # Get the requesting user if set in the context
            request = self.context.get('request', None)
            if request and is_user(request.user):
                return Bookmark.objects.filter(
                    user=request.user,
                    content_type__model=self.bookmarked_model,
                    object_id=obj.id,
                    enabled=True).exists()
        return False
