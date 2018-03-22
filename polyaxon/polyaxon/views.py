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


class TemplateStatusView(TemplateView):
    status_code = 200

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)


class Handler404View(TemplateStatusView):
    template_name = "polyaxon/404.html"
    status_code = 404


class Handler50xView(TemplateStatusView):
    template_name = "polyaxon/50x.html"
    status_code = 500


class Handler403View(TemplateStatusView):
    template_name = "polyaxon/403.html"
    status_code = 403


class HealthView(APIView):
    authentication_classes = ()
    throttle_classes = (HealthRateThrottle,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
