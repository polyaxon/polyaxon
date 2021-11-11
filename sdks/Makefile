# Copyright 2019 Polyaxon, Inc.
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

IMG := polyaxon/polyaxon-sdks
VERSION := v1
DOCKER_RUN := docker run -it --rm -v ${PWD}:/sdks $(IMG)
PROTOC := $(DOCKER_RUN) protoc
PYTHON := $(DOCKER_RUN) python
GO := $(DOCKER_RUN) go
SWAGGER := $(DOCKER_RUN) swagger
DOCKER_PATH_AUTOGEN := /usr/local/bin/autogen/autogen
PATH_SWAGGER_CLI := ~/bin/openapi-generator-cli-5.3.0.jar
LICENSE_OWNER := "Polyaxon, Inc."

# Client
PB_CLIENT := pb_client
HTTP_CLIENT := http_client

# Move -I/gopath/pkg/mod/github.com/grpc-ecosystem/grpc-gateway\@v1.16.0/googleapis/ to -I/sdks/protos/google/api/
# See https://github.com/grpc-ecosystem/grpc-gateway/issues/1935#issuecomment-803572170
# Flags
INCLUDE_FLAGS := -I/usr/local/include -I. -I/gopath/pkg/mod -I/sdks/protos/google/api -I/gopath/pkg/mod/github.com/grpc-ecosystem/grpc-gateway/v2\@v2.6.0
API_FLAGS := --plugin=protoc-gen-openapiv2=/gopath/bin/protoc-gen-openapiv2 --swagger_out=simple_operation_ids=true,logtostderr=true,allow_delete_body=true:swagger
PROTO_PATH := --proto_path=protos/

# Proto files
PROTO_SDK := protos/$(VERSION)/*.proto
PROTO_API := protos/$(VERSION)/api/*.proto
PROTO_POLYFLOW := protos/$(VERSION)/polyflow/*.proto
PROTO_POLYBOARD := protos/$(VERSION)/polyboard/*.proto
PROTO_SCHEMAS := protos/$(VERSION)/schemas/*.proto
PROTO_TYPES := protos/$(VERSION)/types/*.proto

default: all

docker-bash:
	$(DOCKER_RUN) bash

docker-build:
	docker build -t $(IMG) .

compile-go:
	# Compile the *.proto files into *.pb.go (grpc client).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_SDK)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_API)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_POLYFLOW)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_POLYBOARD)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_SCHEMAS)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_TYPES)
	# Compile the *.proto files into *.pb.gw.go (grpc client).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_SDK)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_API)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_POLYFLOW)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_POLYBOARD)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_SCHEMAS)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_TYPES)

compile-swagger:
	# Compile the *.proto files into *.swagger.json (swagger specification).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_SDK)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_API)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_POLYFLOW)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_POLYBOARD)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_SCHEMAS)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) $(API_FLAGS) $(PROTO_TYPES)


compile-js:
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_SDK)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_API)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_POLYFLOW)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_POLYBOARD)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_SCHEMAS)
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_TYPES)


compile-python:
	# Compile the *.proto files into *pb2.py *pb2_grpc.py (grpc client).
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_SDK)
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_API)
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_POLYFLOW)
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_POLYBOARD)
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_SCHEMAS)
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_TYPES)

generate-go-swagger:
	# Compile the *.swagger.json into go REST clients, see https://github.com/go-swagger/go-swagger
	$(SWAGGER) generate client -f swagger/$(VERSION)/polyaxon_sdk.swagger.json -A polyaxon-sdk --principal models.Principal -c service_client -m service_model -t go/$(HTTP_CLIENT)/$(VERSION)
	# Executes the //go:generate directives in the generated code.
	$(GO) generate ./...
	$(DOCKER_RUN) find ./ -name "*.go" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -y 2018-2021 -c $(LICENSE_OWNER) -l apache {} \;

generate-js-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -g javascript -o js/$(HTTP_CLIENT)/$(VERSION) -c swagger/config/config-base.json
	$(DOCKER_RUN) find ./ -name "*.js" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -y 2018-2021 -c $(LICENSE_OWNER) -l apache {} \;

generate-ts-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -g typescript-fetch -o ts/$(HTTP_CLIENT)/$(VERSION) -c swagger/config/config-base.json
	$(DOCKER_RUN) find ./ -name "*.ts" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -y 2018-2021 -c $(LICENSE_OWNER) -l apache {} \;

generate-java-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -g java -o java/$(HTTP_CLIENT)/$(VERSION) -c swagger/config/config-java.json
	$(DOCKER_RUN) find ./ -name "*.java" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -y 2018-2021 -c $(LICENSE_OWNER) -l apache {} \;

generate-py-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -g python-legacy -o python/$(HTTP_CLIENT)/$(VERSION) -c swagger/config/config-py.json
	$(DOCKER_RUN) rm -rf python/$(HTTP_CLIENT)/$(VERSION)/test
	$(DOCKER_RUN) find ./ -name "*.py" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -y 2018-2021 -c $(LICENSE_OWNER) -l apache {} \;

generate-html-openapi:
	$(DOCKER_RUN) bootprint openapi swagger/$(VERSION)/polyaxon_sdk.swagger.json openapi-html/$(VERSION)

clean:
	# Clean current generated code.
	rm -rf go/$(HTTP_CLIENT)/$(VERSION)
	mkdir go/$(HTTP_CLIENT)/$(VERSION)
	rm -rf go/$(PB_CLIENT)/$(VERSION)
	mkdir go/$(PB_CLIENT)/$(VERSION)
	rm -rf python/$(HTTP_CLIENT)/$(VERSION)
	mkdir python/$(HTTP_CLIENT)/$(VERSION)
	rm -rf python/$(PB_CLIENT)/$(VERSION)
	mkdir python/$(PB_CLIENT)/$(VERSION)
	rm -rf js/$(HTTP_CLIENT)/$(VERSION)
	mkdir js/$(HTTP_CLIENT)/$(VERSION)
	rm -rf js/$(PB_CLIENT)/$(VERSION)
	mkdir js/$(PB_CLIENT)/$(VERSION)
	rm -rf ts/$(HTTP_CLIENT)/$(VERSION)
	mkdir ts/$(HTTP_CLIENT)/$(VERSION)
	rm -rf ts/$(PB_CLIENT)/$(VERSION)
	mkdir ts/$(PB_CLIENT)/$(VERSION)
	rm -rf java/$(HTTP_CLIENT)/$(VERSION)
	mkdir java/$(HTTP_CLIENT)/$(VERSION)
	rm -rf java/$(PB_CLIENT)/$(VERSION)
	mkdir java/$(PB_CLIENT)/$(VERSION)
	rm -rf swagger/$(VERSION)
	mkdir swagger/$(VERSION)
	rm -rf jsonschema/$(VERSION)
	mkdir jsonschema/$(VERSION)
	rm -rf openapi-html/$(VERSION)
	mkdir openapi-html/$(VERSION)

swagger-clean:
	rm -rf swagger/$(VERSION)/api
	rm -rf swagger/$(VERSION)/polyboard
	rm -rf swagger/$(VERSION)/polyflow
	rm -rf swagger/$(VERSION)/schemas
	rm -rf swagger/$(VERSION)/types
	rm -rf python/$(HTTP_CLIENT)/$(VERSION)/.openapi-generator
	rm -rf js/$(HTTP_CLIENT)/$(VERSION)/.openapi-generator
	rm -rf ts/$(HTTP_CLIENT)/$(VERSION)/.openapi-generator
	rm -rf java/$(HTTP_CLIENT)/$(VERSION)/.openapi-generator

swagger-generate: generate-go-swagger \
	generate-js-swagger \
	generate-ts-swagger \
	generate-java-swagger \
	generate-py-swagger \
  swagger-clean
	# generate-html-openapi

swagger-concat:
	./concat.sh

prepare: clean \
	compile-swagger \
	swagger-concat

compile-pb: compile-go \
	compile-python

jsonschema-generate: hack/jsonschema/main.go
	go run ./hack/jsonschema
	rm jsonschema/$(VERSION)/polyaxon_sdk.swagger.json

all: prepare \
    jsonschema-generate
