import os


def ensure_path(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
