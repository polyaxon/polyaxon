import logging
import os

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.http import HttpResponseServerError

from datasets.models import Dataset
from datasets.permissions import IsDatasetOwnerOrPublicReadOnly, has_dataset_permissions
from datasets.serializers import DatasetSerializer

logger = logging.getLogger(__name__)


class DatasetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = (IsAuthenticated, IsDatasetOwnerOrPublicReadOnly)


class UploadDataView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        dataset, is_created = Dataset.objects.get_or_create(user=self.request.user)
        if not is_created:
            has_dataset_permissions(self.request.user, dataset, self.request.method)
        return dataset

    @staticmethod
    def _handle_posted_data(request, repo, directory):
        filename = os.path.join(directory, '{}.tar.gz'.format(repo.project.name))
        file_data = request.data['data']

        # filename might already exist, if uploads are done in quick succession
        # we just delete the previous one and assume that its changes are already committed
        while os.path.exists(filename):
            os.remove(filename)

        # Creating the new file
        with open(filename, 'wb') as destination:
            for chunk in file_data.chunks():
                destination.write(chunk)
        return filename

    def put(self, request, *args, **kwargs):
        user = request.user
        dataset = self.get_object()
        path = os.path.join(settings.UPLOAD_ROOT, user.username)
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            tar_file_name = self._handle_posted_data(request, repo, path)
        except (IOError, os.error) as e:  # pragma: no cover
            logger.warning(
                'IOError while trying to save posted data ({}): {}'.format(e.errno, e.strerror))
            return HttpResponseServerError()

        # handle_new_data.delay(user_id=user.id,
        #                       dataset_id=dataset.id,
        #                       tar_file_name=tar_file_name)

        # do some stuff with uploaded file
        return Response(status=204)
