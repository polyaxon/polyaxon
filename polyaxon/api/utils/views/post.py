from rest_framework import generics


class PostAPIView(generics.CreateAPIView):
    def get_serializer(self, *args, **kwargs):
        pass
