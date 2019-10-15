# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

NEWLINES = ('\n', '\r', '\r\n')

INIT_COMMAND = "`polyaxon init PROJECT_NAME [--polyaxonfile]`"

DEFAULT_IGNORE_LIST = """
.git
.eggs
eggs
lib
lib64
parts
sdist
var
*.pyc
*.swp
.DS_Store
./.polyaxon
"""

INIT_FILE = 'polyaxonfile.yaml'

INIT_FILE_MODEL_TEMPLATE = """---
version: 1

kind: experiment

logging:
  level: INFO

model:
  # set you model
"""

INIT_FILE_RUN_TEMPLATE = """---
version: 1

kind: experiment

build:
  # image: # Image name to use

run:
  # cmd: # Command to use
"""

INIT_FILE_MODEL = 'model'
INIT_FILE_RUN = 'run'

INIT_FILE_TEMPLATES = {
    INIT_FILE_MODEL: INIT_FILE_MODEL_TEMPLATE,
    INIT_FILE_RUN: INIT_FILE_RUN_TEMPLATE
}
