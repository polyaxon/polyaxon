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

KUBE_ROOT=$(dirname "${BASH_SOURCE}")/..
CODEGEN_PKG=vendor/k8s.io/code-generator
if [ -z "${GOPATH:-}" ]; then
    export GOPATH=$(go env GOPATH)
fi
vendor/k8s.io/code-generator/generate-groups.sh all "github.com/polyaxon/polyaxon/operator/pkg/client" "github.com/polyaxon/polyaxon/operator/api" core:v1  --go-header-file hack/boilerplate.go.txt
