#!/bin/sh

set -eux

python3 ci/validate/helm.py --values=values1.yml --output-dir=tmp_template1
python3 ci/validate/helm.py --values=values2.yml --output-dir=tmp_template2
python3 ci/validate/helm.py --values=values3.yml --output-dir=tmp_template3
