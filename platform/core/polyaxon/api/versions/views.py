from rest_framework.response import Response

from api.endpoint.base import BaseEndpoint, RetrieveEndpoint
from db.models.versions import ChartVersion, CliVersion, LibVersion, PlatformVersion
from polyaxon.config_manager import config
from schemas import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    LogHandlerConfig,
    PlatformVersionConfig
)


class CliVersionView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        cli_version = CliVersion.load()
        return Response(CliVersionConfig.obj_to_dict(cli_version))


class PlatformVersionView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        platform_version = PlatformVersion.load()
        return Response(PlatformVersionConfig.obj_to_dict(platform_version))


class LibVersionView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        lib_version = LibVersion.load()
        return Response(LibVersionConfig.obj_to_dict(lib_version))


class ChartVersionView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        chart_version = ChartVersion.load()
        return Response(ChartVersionConfig.obj_to_dict(chart_version))


class ClusterLogHandlerView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        cli_version = CliVersionConfig.obj_to_dict(CliVersion.load())
        chart_version = ChartVersionConfig.obj_to_dict(ChartVersion.load())
        platform_version = PlatformVersionConfig.obj_to_dict(PlatformVersion.load())
        handler_config = LogHandlerConfig(
            dsn=config.cli_dsn,
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
