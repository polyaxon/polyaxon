from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "polyaxon/index.html"


class ReactIndexView(TemplateView):
    template_name = "polyaxon/react_index.html"

