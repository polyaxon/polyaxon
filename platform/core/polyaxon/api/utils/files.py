import mimetypes
import os

from typing import Any, Union
from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework.response import Response

from django.http import StreamingHttpResponse


def stream_file(file_path: str, logger: Any) -> Union[Response, StreamingHttpResponse]:
    filename = os.path.basename(file_path)
    chunk_size = 8192
    try:
        wrapped_file = FileWrapper(open(file_path, 'rb'), chunk_size)
        response = StreamingHttpResponse(wrapped_file,
                                         content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = "attachment; filename={}".format(filename)
        return response
    except FileNotFoundError:
        logger.warning('File not found: file_path=%s', file_path)
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data='File not found: file_path={}'.format(file_path))
    except OSError:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data='Could not get the file, an error was encountered.')
