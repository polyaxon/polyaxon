from rest_framework.pagination import LimitOffsetPagination


class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 300000
