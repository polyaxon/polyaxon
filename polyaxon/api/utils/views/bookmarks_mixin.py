from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from db.models.bookmarks import Bookmark


class BookmarkedListMixinView(object):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if not isinstance(serializer_class, BookmarkedSerializerMixin):
            return super().get_serializer(*args, **kwargs)

        queryset = args[0]

        if not queryset:
            return super().get_serializer(*args, **kwargs)

        object_ids = [o.id for o in queryset]

        # Batch-get all the bookmarks for the objects in the queryset
        # and pass them on to the serializer
        bookmarks = Bookmark.objects.filter(
            user=self.request.user,
            content_type__model=self.serializer_class.bookmarked_model,
            object_id__in=object_ids,
            enabled=True).values_list('id', flat=True)

        context = self.get_serializer_context()
        context['bookmarks'] = list(bookmarks)
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)
