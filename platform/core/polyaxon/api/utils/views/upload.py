import json
import os

from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class UploadView(APIView):
    """Base view to handle data upload."""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _handle_posted_data(request, filename, directory, upload_filename):
        file_path = os.path.join(directory, filename)
        file_data = request.data[upload_filename]

        # filename might already exist, if uploads are done in quick succession
        # we just delete the previous one and assume that its changes are already committed
        while os.path.exists(file_path):
            os.remove(file_path)

        # Creating the new file
        with open(file_path, 'wb') as destination:
            for chunk in file_data.chunks():
                destination.write(chunk)
        return file_path

    @staticmethod
    def _handle_json_data(request):
        json_data = request.data.get('json')
        if json_data:
            return json.loads(json_data)
        return {}
