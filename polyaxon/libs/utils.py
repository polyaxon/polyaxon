from schemas.utils import to_list


def get_list(values):
    return to_list(values) if values is not None else []
