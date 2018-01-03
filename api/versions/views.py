# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from polyaxon_schemas.version import (
    CliVersionConfig,
    LibVersionConfig,
    PlatformVersionConfig,
    ChartVersionConfig
)

from versions.models import CliVersion, PlatformVersion, LibVersion, ChartVersion


class CliVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        cli_version = CliVersion.load()
        return Response(CliVersionConfig.obj_to_dict(cli_version))


class PlatformVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        platform_version = PlatformVersion.load()
        return Response(PlatformVersionConfig.obj_to_dict(platform_version))


class LibVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        lib_version = LibVersion.load()
        return Response(LibVersionConfig.obj_to_dict(lib_version))


class ChartVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        chart_version = ChartVersion.load()
        return Response(ChartVersionConfig.obj_to_dict(chart_version))
