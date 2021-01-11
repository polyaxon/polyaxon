#!/bin/bash

# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -o errexit
set -o nounset
set -o pipefail

if [ -z "${GOPATH:-}" ]; then
    export GOPATH=$(go env GOPATH)
fi

VERSION="v1"

KNOWN_VIOLATION_EXCEPTIONS=hack/violation_exceptions.list
CURRENT_VIOLATION_EXCEPTIONS=hack/current_violation_exceptions.list

PROJECT_ROOT=$(cd $(dirname "$0")/.. ; pwd)
CODEGEN_PKG=${PROJECT_ROOT}/vendor/k8s.io/kube-openapi

# Generating OpenAPI specification
go run ${CODEGEN_PKG}/cmd/openapi-gen/openapi-gen.go \
    --input-dirs github.com/polyaxon/polyaxon/operator/api/${VERSION} \
    --output-package api/${VERSION}/ \
    --go-header-file hack/boilerplate.go.txt \
    --report-filename $CURRENT_VIOLATION_EXCEPTIONS \
    $@

test -f $CURRENT_VIOLATION_EXCEPTIONS || touch $CURRENT_VIOLATION_EXCEPTIONS

# The API rule fails if generated API rule violation report differs from the
# checked-in violation file, prints error message to request developer to
# fix either the API source code, or the known API rule violation file.
diff $CURRENT_VIOLATION_EXCEPTIONS $KNOWN_VIOLATION_EXCEPTIONS || \
    (echo -e "ERROR: \n\t API rule check failed. Reported violations in file $CURRENT_VIOLATION_EXCEPTIONS differ from known violations in file $KNOWN_VIOLATION_EXCEPTIONS. \n"; exit 1)

# Generating swagger file
go run cmd/openapi-gen/main.go 1.0 > api/${VERSION}/swagger.json
