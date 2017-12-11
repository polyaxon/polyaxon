# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from polyaxon_schemas.version import CliVersionConfig, PlatformVersionConfig

from versions.models import CliVersion, PlatformVersion


class CliVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        cli_version = CliVersion.load()
        return Response(CliVersionConfig.obj_to_dict(cli_version))


class PlatformVersionView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        cli_version = PlatformVersion.load()
        return Response(PlatformVersionConfig.obj_to_dict(cli_version))
