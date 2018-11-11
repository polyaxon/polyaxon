from rest_framework import status
from rest_framework.exceptions import APIException


class SuperuserRequired(APIException):
    status_code = status.HTTP_403_FORBIDDEN
