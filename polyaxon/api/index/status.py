from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from checks.status import get_status


class StatusView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        return Response(get_status())
