import os

DEFAULT_POLYAXON_FILE_NAME = [
    'polyaxon',
    'polyaxonci',
    'polyaxon-ci',
    'polyaxon.ci',
    'polyaxonfile',
]

DEFAULT_POLYAXON_FILE_EXTENSION = [
    'yaml',
    'yml',
    'json'
]


def get_default_polyaxonfile(path):
    path = os.path.abspath(path)
    for filename in DEFAULT_POLYAXON_FILE_NAME:
        for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
            filepath = os.path.join(path, '{}.{}'.format(filename, ext))
            if os.path.isfile(filepath):
                return filepath
