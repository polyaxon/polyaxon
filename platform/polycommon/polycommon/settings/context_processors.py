from polycommon import conf, pkg
from polycommon.options.registry.core import UI_ASSETS_VERSION, UI_ENABLED, UI_OFFLINE


def version(request):
    return {"version": pkg.VERSION}


def assets_version(request):
    return {"assets_version": "{}.{}".format(pkg.VERSION, conf.get(UI_ASSETS_VERSION))}


def ui_offline(request):
    return {"ui_offline": conf.get(UI_OFFLINE)}


def ui_enabled(request):
    return {"ui_enabled": conf.get(UI_ENABLED)}
