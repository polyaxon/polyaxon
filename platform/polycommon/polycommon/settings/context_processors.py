from polycommon import conf, pkg
from polycommon.options.registry.core import JS_OFFLINE, UI_ENABLED


def versions(request):
    return {"version": pkg.VERSION}


def js_offline(request):
    return {"js_offline": conf.get(JS_OFFLINE)}


def ui_enabled(request):
    return {"ui_enabled": conf.get(UI_ENABLED)}
