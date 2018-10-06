from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class HealthRateThrottle(AnonRateThrottle):
    scope = 'health'


class HealthView(APIView):
    authentication_classes = ()
    throttle_classes = (HealthRateThrottle,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
