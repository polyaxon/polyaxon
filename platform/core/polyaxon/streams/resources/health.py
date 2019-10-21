from sanic import response


def health(request):
    return response.text('', status=200)
