# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.views.generic import TemplateView

from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthRateThrottle(AnonRateThrottle):
    scope = 'health'


class IndexView(TemplateView):
    template_name = "polyaxon/index.html"


class ReactIndexView(TemplateView):
    template_name = "polyaxon/react_index.html"


class Handler404View(TemplateView):
    template_name = "polyaxon/404.html"


class Handler50xView(TemplateView):
    template_name = "polyaxon/50x.html"


class Handler403View(TemplateView):
    template_name = "polyaxon/403.html"


class HealthView(APIView):
    authentication_classes = ()
    throttle_classes = (HealthRateThrottle,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
