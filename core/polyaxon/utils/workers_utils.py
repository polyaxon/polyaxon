#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import os
import signal
import threading

from contextlib import contextmanager
from typing import Generator

from polyaxon.logger import logger


def get_pool_workers():
    return min(32, (os.cpu_count() or 1) + 4)


@contextmanager
def exit_context() -> Generator:
    exit_event = threading.Event()

    def _exit_handler(*args, **kwargs) -> None:
        logger.info("Keyboard Interrupt received, exiting pool.")
        exit_event.set()

    original = signal.getsignal(signal.SIGINT)
    try:
        signal.signal(signal.SIGINT, _exit_handler)
        yield exit_event
    except SystemExit:
        pass
    finally:
        signal.signal(signal.SIGINT, original)


def get_wait(current: int) -> float:
    intervals = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

    if current >= 5:
        current = 5
    return intervals[current]
