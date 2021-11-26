#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

from typing import Dict

try:
    import pandas as pd
except ImportError:
    pd = None
    try:
        import csv
    except ImportError:
        print("pandas or csv module are required to use save as csv file")
        sys.exit(1)


def write_csv(objects: Dict, filename: str):
    if pd:
        df = pd.DataFrame(objects)
        df.to_csv(filename)
    else:
        with open(filename, "w", encoding="utf8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=objects[0].keys())
            writer.writeheader()
            writer.writerows(objects)
