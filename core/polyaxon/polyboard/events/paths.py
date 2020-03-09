def get_resource_path(run_path: str, kind: str = None, name: str = None) -> str:
    _path = "{}/resources".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    if name:
        _path = "{}/{}.plx".format(_path, name)

    return _path


def get_event_path(run_path: str, kind: str = None, name: str = None) -> str:
    _path = "{}/events".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    if name:
        _path = "{}/{}.plx".format(_path, name)

    return _path


def get_asset_path(
    run_path: str, kind: str = None, name: str = None, step: int = None, ext=None
) -> str:
    _path = "{}/assets".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    if name:
        _path = "{}/{}".format(_path, name)
    if step is not None:
        _path = "{}_{}".format(_path, step)
    if ext:
        _path = "{}.{}".format(_path, ext)

    return _path
