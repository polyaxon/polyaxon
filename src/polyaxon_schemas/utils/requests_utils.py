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
import time

try:
    import requests
except ImportError:
    raise ImportError("This module depends on requests.")


def safe_request(
    url,
    method=None,
    params=None,
    data=None,
    json=None,
    headers=None,
    allow_redirects=False,
    timeout=30,
    verify_ssl=True,
):
    """A slightly safer version of `request`."""

    session = requests.Session()

    kwargs = {}

    if json:
        kwargs["json"] = json
        if not headers:
            headers = {}
        headers.setdefault("Content-Type", "application/json")

    if data:
        kwargs["data"] = data

    if params:
        kwargs["params"] = params

    if headers:
        kwargs["headers"] = headers

    if method is None:
        method = "POST" if (data or json) else "GET"

    response = session.request(
        method=method,
        url=url,
        allow_redirects=allow_redirects,
        timeout=timeout,
        verify=verify_ssl,
        **kwargs
    )

    return response


STREAM = sys.stderr

BAR_TEMPLATE = "%s[%s%s] %i/%i - %s\r"
MILL_TEMPLATE = "%s %s %i/%i\r"

DOTS_CHAR = "."
BAR_FILLED_CHAR = "#"
BAR_EMPTY_CHAR = " "
MILL_CHARS = ["|", "/", "-", "\\"]

# How long to wait before recalculating the ETA
ETA_INTERVAL = 1
# How many intervals (excluding the current one) to calculate the simple moving average
ETA_SMA_WINDOW = 9


class Bar:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done()
        return False  # we're not suppressing exceptions

    def __init__(
        self,
        label="",
        width=32,
        hide=None,
        empty_char=BAR_EMPTY_CHAR,
        filled_char=BAR_FILLED_CHAR,
        expected_size=None,
        every=1,
    ):
        self.label = label
        self.width = width
        self.hide = hide
        # Only show bar in terminals by default (better for piping, logging etc.)
        if hide is None:
            try:
                self.hide = not STREAM.isatty()
            except AttributeError:  # output does not support isatty()
                self.hide = True
        self.empty_char = empty_char
        self.filled_char = filled_char
        self.expected_size = expected_size
        self.every = every
        self.start = time.time()
        self.ittimes = []
        self.eta = 0
        self.etadelta = time.time()
        self.etadisp = self.format_time(self.eta)
        self.last_progress = 0
        self.elapsed = None
        if self.expected_size:
            self.show(0)

    def show(self, progress, count=None):
        if count is not None:
            self.expected_size = count
        if self.expected_size is None:
            raise Exception("expected_size not initialized")
        self.last_progress = progress
        if (time.time() - self.etadelta) > ETA_INTERVAL:
            self.etadelta = time.time()
            self.ittimes = self.ittimes[-ETA_SMA_WINDOW:] + [
                -(self.start - time.time()) / (progress + 1)
            ]
            self.eta = (
                sum(self.ittimes)
                / float(len(self.ittimes))
                * (self.expected_size - progress)
            )
            self.etadisp = self.format_time(self.eta)
        x = int(self.width * progress / self.expected_size)
        if not self.hide:
            # True every "every" updates and when we're done
            if (progress % self.every) == 0 or (progress == self.expected_size):
                STREAM.write(
                    BAR_TEMPLATE
                    % (
                        self.label,
                        self.filled_char * x,
                        self.empty_char * (self.width - x),
                        progress,
                        self.expected_size,
                        self.etadisp,
                    )
                )
                STREAM.flush()

    def done(self):
        self.elapsed = time.time() - self.start
        elapsed_disp = self.format_time(self.elapsed)
        if not self.hide:
            # Print completed bar with elapsed time
            STREAM.write(
                BAR_TEMPLATE
                % (
                    self.label,
                    self.filled_char * self.width,
                    self.empty_char * 0,
                    self.last_progress,
                    self.expected_size,
                    elapsed_disp,
                )
            )
            STREAM.write("\n")
            STREAM.flush()

    @staticmethod
    def format_time(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))


def progress_bar(items, label="", width=32, hide=None, expected_size=None, every=1):
    """Progress iterator. Wrap your iterables with it."""

    count = len(items) if expected_size is None else expected_size

    with Bar(
        label=label,
        width=width,
        hide=hide,
        empty_char=BAR_EMPTY_CHAR,
        filled_char=BAR_FILLED_CHAR,
        expected_size=count,
        every=every,
    ) as _bar:
        for i, item in enumerate(items):
            yield item
            _bar.show(i + 1)


def create_progress_callback(encoder):
    encoder_len = encoder.len
    callback_bar = Bar(expected_size=encoder_len, filled_char="=")

    def callback(monitor):
        callback_bar.show(monitor.bytes_read)

    return callback, callback_bar
