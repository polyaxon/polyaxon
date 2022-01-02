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
from concurrent import futures
from typing import Callable, List, Optional, Tuple


class StoreMixin:
    def ls(self, path):
        raise NotImplementedError

    def list(self, *args, **kwargs):
        raise NotImplementedError

    def delete_file(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def download_file(self, *args, **kwargs):
        raise NotImplementedError

    def download_dir(self, *args, **kwargs):
        raise NotImplementedError

    def upload_file(self, *args, **kwargs):
        raise NotImplementedError

    def upload_dir(self, *args, **kwargs):
        raise NotImplementedError

    def init_pool(self, workers: int = 0) -> Tuple[futures.ThreadPoolExecutor, List]:
        pool = None
        future_results = []

        if workers:
            pool = futures.ThreadPoolExecutor(workers)

        return pool, future_results

    def submit_pool(
        self,
        fn: Callable,
        workers: int,
        pool: Optional[futures.ThreadPoolExecutor],
        future_results: Optional[List],
        **kwargs
    ) -> Optional[List]:
        if workers:
            future_result = pool.submit(fn, **kwargs)
            future_results.append(future_result)
        else:
            fn(**kwargs)
        return future_results

    def close_pool(self, pool: Optional[futures.ThreadPoolExecutor]):
        if pool:
            pool.shutdown(wait=True)
