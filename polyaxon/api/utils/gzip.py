from functools import wraps

from django.utils.decorators import available_attrs
from django.utils.text import compress_string


class GzipDecorator(object):
    """Gzip the response and set the respective header.
    """
    def __call__(self, func):
        @wraps(func, assigned=available_attrs(func))
        def inner(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)

            # Before we can access response.content, the response needs to be rendered.
            response = self.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache

            compressed_content = compress_string(response.content)

            # Ensure that the compressed content is actually smaller than the original.
            if len(compressed_content) >= len(response.content):
                return response

            # Replace content with gzipped variant, update respective headers.
            response.content = compressed_content
            response['Content-Length'] = str(len(response.content))
            response['Content-Encoding'] = 'gzip'

            return response

        return inner


gzip = GzipDecorator
