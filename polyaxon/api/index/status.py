from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from checks.status import get_status


class HealthRateThrottle(AnonRateThrottle):
    scope = 'status'


class StatusView(RetrieveAPIView):
    authentication_classes = ()
    throttle_classes = (HealthRateThrottle,)

    def retrieve(self, request, *args, **kwargs):
        return Response(get_status())
