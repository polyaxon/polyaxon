from django.views.generic import TemplateView


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
