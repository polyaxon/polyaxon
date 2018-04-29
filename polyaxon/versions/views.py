from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from polyaxon.utils import config
from polyaxon_schemas.log_handler import LogHandlerConfig
from polyaxon_schemas.version import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    PlatformVersionConfig
)
from versions.models import ChartVersion, CliVersion, LibVersion, PlatformVersion


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


class ClusterLogHandlerView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        cli_version = CliVersionConfig.obj_to_dict(CliVersion.load())
        chart_version = ChartVersionConfig.obj_to_dict(ChartVersion.load())
        platform_version = PlatformVersionConfig.obj_to_dict(PlatformVersion.load())
        handler_config = LogHandlerConfig(
            dns=config.cli_dns,
            environment=config.env,
            tags={
                'cli_min_version': cli_version['min_version'],
                'cli_latest_version': cli_version['latest_version'],
                'platform_min_version': platform_version['min_version'],
                'platform_latest_version': platform_version['latest_version'],
                'chart_version': chart_version['version']
            }
        )
        return Response(handler_config.to_dict())
