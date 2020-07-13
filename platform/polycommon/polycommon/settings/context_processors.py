from polycommon import conf, pkg
from polycommon.options.registry.core import UI_ENABLED, UI_OFFLINE


def versions(request):
    return {"version": pkg.VERSION}


def ui_offline(request):
    return {"ui_offline": conf.get(UI_OFFLINE)}


def ui_enabled(request):
    return {"ui_enabled": conf.get(UI_ENABLED)}
