from models.versions import ChartVersion, CliVersion, LibVersion, PlatformVersion


def versions(request):
    return {
        'cli_version': CliVersion.load(),
        'platfornm_version': PlatformVersion.load(),
        'lib_version': LibVersion.load(),
        'chart_version': ChartVersion.load(),
    }
