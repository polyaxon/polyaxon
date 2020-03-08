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

from click import ClickException


class PolyaxonException(ClickException):
    def __init__(self, message=None):
        super().__init__(message)

    def __repr__(self):
        return self.message


class PolyaxonOperatorException(PolyaxonException):
    def __init__(self, cmd, args, return_code, stdout, stderr):
        self.cmd = cmd
        self.args = args
        self.return_code = return_code
        self.stdout = stdout.read() if stdout else None
        self.stderr = stderr.read()
        if stdout:
            message = "`{}` command {} failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                self.cmd, self.args, self.return_code, self.stdout, self.stderr
            )
        else:
            message = "`{}` command {} failed with exit status {}\nstderr:\n{}".format(
                self.cmd, self.args, self.return_code, self.stderr
            )
        super().__init__(message=message)


class PolypodException(PolyaxonException):
    pass


class PolyaxonCompilerError(PolyaxonException):
    pass


class PolyTuneException(PolyaxonException):
    pass


class PolyaxonConfigException(PolyaxonException):
    pass


class PolyaxonK8SError(PolyaxonException):
    pass


class PolyaxonAgentError(PolyaxonException):
    pass


class PolyaxonBuildException(PolyaxonException):
    pass


class PolyaxonContainerException(Exception):
    pass


class PolyaxonConnectionError(PolyaxonException):
    pass


class PolyaxonPathException(PolyaxonException):
    pass


class PolyaxonStoresException(PolyaxonException):
    pass


class PolyaxonSchemaError(PolyaxonException):
    pass


class PolyaxonDateTimeFormatterException(PolyaxonException):
    pass


class PQLException(PolyaxonException):
    pass


class PolyaxonfileError(PolyaxonSchemaError):
    pass


class PolyaxonClientException(PolyaxonException):
    pass


class PolyaxonNotificationException(PolyaxonException):
    pass


class PolyaxonShouldExitError(PolyaxonClientException):
    pass


class PolyaxonHTTPError(PolyaxonClientException):
    def __init__(self, endpoint, response, message=None, status_code=None):
        super().__init__()
        self.endpoint = endpoint
        self.response = response
        self.message = getattr(self, "message", message)
        self.status_code = getattr(self, "status_code", status_code)

    def __str__(self):
        return "{status_code} on {endpoint}.".format(
            status_code=self.status_code, endpoint=self.endpoint
        )


HTTP_ERROR_MESSAGES_MAPPING = {
    400: "Statuts: 400. One or more request parameters is incorrect",
    401: "Status: 401. Authentication failed. Retry by invoking Polyaxon login.",
    403: "Status: 403. You are not authorized to access this resource on Polyaxon.",
    404: "Status: 404. "
    "The resource you are looking for was not found. Check if the name or uuid is correct.",
    429: "Status: 429. You are over the allowed limits for this operation.",
    500: "Status: 502. Internal polyaxon server error, please try again later.",
    502: "Status: 502. Invalid response from Polyaxon server.",
    503: "Status: 503. A problem was encountered, please try again later.",
    504: "Status: 504. Polyaxon server took too long to respond.",
    525: "Status: 525. SSL error.",
}
