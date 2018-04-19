import logging

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from experiment_groups.models import ExperimentGroup
from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
    ExperimentStatus
)
from experiments.paths import get_experiment_logs_path
from experiments.serializers import (
    ExperimentCreateSerializer,
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from libs.utils import to_bool
from libs.views import ListCreateAPIView
from projects.permissions import get_permissible_project

logger = logging.getLogger("polyaxon.experiments.views")

class ExperimentListView(ListAPIView):
    """List all experiments"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)


class ProjectExperimentListView(ListCreateAPIView):
    """List/Create an experiment under a project"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        independent = self.request.query_params.get('independent', None)
        filters = {}
        if independent is not None and to_bool(independent):
            filters['experiment_group__isnull'] = True
        return queryset.filter(project=get_permissible_project(view=self), **filters)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=get_permissible_project(view=self))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupExperimentListView(ListAPIView):
    """List all experiments under a group"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)

    def get_group(self):
        sequence = self.kwargs['sequence']
        # Get project and check permissions
        project = get_permissible_project(view=self)
        group = get_object_or_404(ExperimentGroup, project=project, sequence=sequence)

        return group

    def filter_queryset(self, queryset):
        return queryset.filter(experiment_group=self.get_group())


class ExperimentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))


class ExperimentRestartView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        new_obj = obj.restart(user=self.request.user)
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class ExperimentViewMixin(object):
    """A mixin to filter by experiment."""

    def get_experiment(self):
        # Get project and check access
        project = get_permissible_project(view=self)
        sequence = self.kwargs['experiment_sequence']
        experiment = get_object_or_404(Experiment, project=project, sequence=sequence)
        return experiment

    def filter_queryset(self, queryset):
        queryset = super(ExperimentViewMixin, self).filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentMetricListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentMetric.objects.all()
    serializer_class = ExperimentMetricSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(ExperimentViewMixin, RetrieveAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentJobListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    create_serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentJobDetailView(ExperimentViewMixin, RetrieveUpdateDestroyAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'


class ExperimentJobViewMixin(object):
    """A mixin to filter by experiment job."""

    def get_experiment(self):
        # Get project and check access
        project = get_permissible_project(view=self)
        sequence = self.kwargs['experiment_sequence']
        experiment = get_object_or_404(Experiment, project=project, sequence=sequence)
        return experiment

    def get_job(self):
        job_sequence = self.kwargs['sequence']
        job = get_object_or_404(ExperimentJob,
                                sequence=job_sequence,
                                experiment=self.get_experiment())
        return job

    def filter_queryset(self, queryset):
        queryset = super(ExperimentJobViewMixin, self).filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class ExperimentJobStatusListView(ExperimentJobViewMixin, ListCreateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(job=self.get_job())


class ExperimentJobStatusDetailView(ExperimentJobViewMixin, RetrieveUpdateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentLogListView(ExperimentViewMixin, APIView):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (IsAuthenticated,)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, username, name, experiment_sequence):
        experiment = self.get_experiment()
        log_path = get_experiment_logs_path(experiment.unique_name)
        logs = []

        try:
            with open(log_path, 'r') as file:
                logs = [line.rstrip('\n') for line in file]
        except FileNotFoundError:
            logger.warning('Log file not found: log_path=%s', log_path)

        page = self.paginate_queryset(logs)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(page)
