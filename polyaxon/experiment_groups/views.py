from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from experiment_groups.models import ExperimentGroup
from experiment_groups.serializers import ExperimentGroupDetailSerializer, ExperimentGroupSerializer
from experiment_groups.tasks import stop_group_experiments
from libs.utils import to_bool
from libs.views import ListCreateAPIView
from projects.permissions import IsItemProjectOwnerOrPublicReadOnly, get_permissible_project


class ExperimentGroupListView(ListCreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    create_serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=get_permissible_project(view=self))


class ExperimentGroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def get_object(self):
        obj = super(ExperimentGroupDetailView, self).get_object()
        # Check project permissions
        self.check_object_permissions(self.request, obj)
        return obj


class ExperimentGroupStopView(CreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        pending = request.data.get('pending')
        pending = to_bool(pending) if pending is not None else False
        stop_group_experiments.delay(experiment_group_id=obj.id,
                                     pending=pending,
                                     message='User stopped experiment group')
        return Response(status=status.HTTP_200_OK)
