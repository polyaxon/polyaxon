from hestia.bool_utils import to_bool
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import auditor

from api.experiment_groups import queries
from api.experiment_groups.serializers import (
    BookmarkedExperimentGroupSerializer,
    ExperimentGroupChartViewSerializer,
    ExperimentGroupCreateSerializer,
    ExperimentGroupDetailSerializer,
    ExperimentGroupSerializer,
    ExperimentGroupStatusSerializer
)
from api.experiments.serializers import ExperimentMetricSerializer
from api.filters import OrderingFilter, QueryFilter
from api.paginator import LargeLimitOffsetPagination
from api.utils.views.auditor_mixin import AuditorMixinView
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from api.utils.views.list_create import ListCreateAPIView
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupChartView,
    ExperimentGroupStatus
)
from db.models.experiments import ExperimentMetric
from event_manager.events.chart_view import CHART_VIEW_CREATED, CHART_VIEW_DELETED
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_DELETED_TRIGGERED,
    EXPERIMENT_GROUP_METRICS_VIEWED,
    EXPERIMENT_GROUP_STATUSES_VIEWED,
    EXPERIMENT_GROUP_STOPPED_TRIGGERED,
    EXPERIMENT_GROUP_UPDATED,
    EXPERIMENT_GROUP_VIEWED
)
from event_manager.events.project import PROJECT_EXPERIMENT_GROUPS_VIEWED
from libs.permissions.projects import IsItemProjectOwnerOrPublicReadOnly, get_permissible_project
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class ExperimentGroupListView(BookmarkedListMixinView, ListCreateAPIView):
    """
    get:
        List experiment groups under a project.

    post:
        Create an experiment group under a project.
    """
    queryset = queries.groups
    serializer_class = BookmarkedExperimentGroupSerializer
    create_serializer_class = ExperimentGroupCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'experiment_group'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        project = get_permissible_project(view=self)
        auditor.record(event_type=PROJECT_EXPERIMENT_GROUPS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        queryset = queryset.filter(project=project)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        project = get_permissible_project(view=self)
        instance = serializer.save(user=self.request.user,
                                   project=project)
        experiment_ids = self.request.data.get('experiment_ids')
        if instance.is_selection and experiment_ids:
            experiment_ids = set(experiment_ids)
            if len(experiment_ids) != project.experiments.filter(id__in=experiment_ids).count():
                raise ValidationError('Experiments selection is not valid.')
            instance.selection_experiments.set(experiment_ids)


class ExperimentGroupDetailView(AuditorMixinView, RetrieveUpdateDestroyAPIView):
    """
    get:
        Get an experiment group details.
    patch:
        Update an experiment group details.
    delete:
        Delete an experiment group.
    """
    queryset = queries.groups_details
    serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'id'
    get_event = EXPERIMENT_GROUP_VIEWED
    update_event = EXPERIMENT_GROUP_UPDATED
    delete_event = EXPERIMENT_GROUP_DELETED_TRIGGERED

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def get_object(self):
        obj = super().get_object()
        # Check project permissions
        self.check_object_permissions(self.request, obj)
        return obj


class ExperimentGroupSelectionView(UpdateAPIView):
    queryset = ExperimentGroup.objects
    serializer_class = None
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        # Check project permissions
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        if not group.is_selection:
            raise ValidationError('This group is a not a selection.')

        project = group.project
        experiment_ids = self.request.data.get('experiment_ids')
        if experiment_ids:
            experiment_ids = set(experiment_ids)
            if len(experiment_ids) != project.experiments.filter(id__in=experiment_ids).count():
                raise ValidationError('Experiments selection is not valid.')
            group.selection_experiments.set(experiment_ids)
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupStopView(CreateAPIView):
    """Stop an experiment group."""
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'id'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        pending = request.data.get('pending')
        pending = to_bool(pending) if pending is not None else False
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username,
                       pending=pending)
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
            kwargs={'experiment_group_id': obj.id,
                    'pending': pending,
                    'message': 'User stopped experiment group'})
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupViewMixin(object):
    """A mixin to filter by experiment group."""
    project = None
    group = None

    def get_experiment_group(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        group_id = self.kwargs['group_id']
        self.group = get_object_or_404(ExperimentGroup, project=self.project, id=group_id)
        return self.group

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(experiment_group=self.get_experiment_group())


class ExperimentGroupStatusListView(ExperimentGroupViewMixin, ListCreateAPIView):
    """
    get:
        List all statuses of experiment group.
    post:
        Create an experiment group status.
    """
    queryset = ExperimentGroupStatus.objects.order_by('created_at').all()
    serializer_class = ExperimentGroupStatusSerializer
    permission_classes = (IsAuthenticated,)
    project = None
    group = None

    def perform_create(self, serializer):
        serializer.save(experiment_group=self.get_experiment_group())

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_GROUP_STATUSES_VIEWED,
                       instance=self.group,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentGroupMetricsListView(ExperimentGroupViewMixin, ListAPIView):
    """
    get:
        List all metrics of experiments under a group.
    """
    queryset = ExperimentMetric.objects.all()
    serializer_class = ExperimentMetricSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeLimitOffsetPagination
    project = None
    group = None

    def filter_queryset(self, queryset):
        queryset = super(ListAPIView, self).filter_queryset(  # pylint:disable=bad-super-call
            queryset)
        group = self.get_experiment_group()
        if group.is_study:
            return queryset.filter(experiment__experiment_group=group)
        elif group.is_selection:
            return queryset.filter(experiment__selections=group)
        raise ValidationError('Invalid group.')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_GROUP_METRICS_VIEWED,
                       instance=self.group,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentGroupChartViewListView(ExperimentGroupViewMixin, ListCreateAPIView):
    """
    get:
        List all chart views of an experiment group.
    post:
        Create an experiment group chart view.
    """
    queryset = ExperimentGroupChartView.objects.all()
    serializer_class = ExperimentGroupChartViewSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeLimitOffsetPagination

    def perform_create(self, serializer):
        group = self.get_experiment_group()
        instance = serializer.save(experiment_group=group)
        auditor.record(event_type=CHART_VIEW_CREATED,
                       instance=instance,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username,
                       group=group)


class ExperimentGroupChartViewDetailView(ExperimentGroupViewMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
        Get experiment group chart view details.
    patch:
        Update an experiment group chart view details.
    delete:
        Delete an experiment group chart view.
    """
    queryset = ExperimentGroupChartView.objects.all()
    serializer_class = ExperimentGroupChartViewSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    delete_event = CHART_VIEW_DELETED

    def get_object(self):
        instance = super().get_object()
        method = self.request.method.lower()
        if method == 'delete' and self.delete_event:
            auditor.record(event_type=self.delete_event,
                           instance=instance,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           group=instance)
        return instance
