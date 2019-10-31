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
PATH_SWAGGER_CLI := ~/bin/swagger-codegen-cli-2.4.9.jar
LICENSE_OWNER := "Polyaxon, Inc."

# Client
PB_CLIENT := pb_client
HTTP_CLIENT := http_client

# Flags
INCLUDE_FLAGS := -I/usr/local/include -I. -I/gopath/src -I/gopath/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis -I/gopath/src/github.com/grpc-ecosystem/grpc-gateway
PROTO_PATH := --proto_path=protos/

# Proto files
PROTO_FILES := protos/$(VERSION)/*.proto

default: all

docker-bash:
	$(DOCKER_RUN) bash

docker-build:
	docker build -t $(IMG) .

compile-go:
	# Compile the *.proto files into *.pb.go (grpc client).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-go=/gopath/bin/protoc-gen-go --go_out=plugins=grpc:go/$(PB_CLIENT) $(PROTO_FILES)
	# Compile the *.proto files into *.pb.gw.go (grpc client).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc-gateway=/gopath/bin/protoc-gen-grpc-gateway --grpc-gateway_out=logtostderr=true,allow_delete_body=true:go/$(PB_CLIENT) $(PROTO_FILES)

compile-swagger:
	# Compile the *.proto files into *.swagger.json (swagger specification).
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-swagger=/gopath/bin/protoc-gen-swagger --swagger_out=logtostderr=true,allow_delete_body=true:swagger $(PROTO_FILES)

compile-js:
	$(PROTOC) $(PROTO_PATH) $(INCLUDE_FLAGS) --plugin=protoc-gen-grpc=/usr/local/bin/grpc_tools_node_protoc_plugin --js_out=import_style=commonjs,binary:js/$(PB_CLIENT) --grpc_out=minimum_node_version=6:js/$(PB_CLIENT) $(PROTO_FILES)

compile-python:
	# Compile the *.proto files into *pb2.py *pb2_grpc.py (grpc client).
	$(PYTHON) -m grpc_tools.protoc $(PROTO_PATH) $(INCLUDE_FLAGS) --grpc_python_out=python/$(PB_CLIENT) --python_out=python/$(PB_CLIENT) $(PROTO_FILES)

generate-go-swagger:
	# Compile the *.swagger.json into go REST clients, see https://github.com/go-swagger/go-swagger
	$(SWAGGER) generate client -f swagger/$(VERSION)/polyaxon_sdk.swagger.json -A polyaxon-sdk --principal models.Principal -c service_client -m service_model -t go/$(HTTP_CLIENT)/$(VERSION)
	# Executes the //go:generate directives in the generated code.
	$(GO) generate ./...

generate-js-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -l javascript -o js/$(HTTP_CLIENT)/$(VERSION) -c swagger/config.json

generate-ts-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -l typescript-fetch -o ts/$(HTTP_CLIENT)/$(VERSION) -c swagger/config.json

generate-java-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -l java -o java/$(HTTP_CLIENT)/$(VERSION) -c swagger/config.json -D hideGenerationTimestamp=true

generate-py-swagger:
	java -jar $(PATH_SWAGGER_CLI) generate -i swagger/$(VERSION)/polyaxon_sdk.swagger.json -l python -o python/$(HTTP_CLIENT)/$(VERSION) -c swagger/config.json

auto-license:
	# Add licenses to the generated files.
	$(DOCKER_RUN) find ./ -name "*.go" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -c $(LICENSE_OWNER) -l apache {} \;
	$(DOCKER_RUN) find ./ -name "*.py" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -c $(LICENSE_OWNER) -l apache {} \;
	$(DOCKER_RUN) find ./ -name "*.ts" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -c $(LICENSE_OWNER) -l apache {} \;
	$(DOCKER_RUN) find ./ -name "*.js" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -c $(LICENSE_OWNER) -l apache {} \;
	$(DOCKER_RUN) find ./ -name "*.java" -exec $(DOCKER_PATH_AUTOGEN) -i --no-tlc --no-code -c $(LICENSE_OWNER) -l apache {} \;

clean:
	# Clean current generated code.
	rm -rf go/$(HTTP_CLIENT)/$(VERSION)/*
	rm -rf go/$(PB_CLIENT)/$(VERSION)/*
	rm -rf python/$(HTTP_CLIENT)/$(VERSION)/*
	rm -rf python/$(PB_CLIENT)/$(VERSION)/*
	rm -rf js/$(HTTP_CLIENT)/$(VERSION)/*
	rm -rf js/$(PB_CLIENT)/$(VERSION)/*
	rm -rf ts/$(HTTP_CLIENT)/$(VERSION)/*
	rm -rf ts/$(PB_CLIENT)/$(VERSION)/*
	rm -rf java/$(HTTP_CLIENT)/$(VERSION)/*
	rm -rf java/$(PB_CLIENT)/$(VERSION)/*
	rm -rf swagger/$(VERSION)/*

swagger-generate: generate-go-swagger \
	 generate-js-swagger \
	 generate-ts-swagger \
	 generate-java-swagger \
	 generate-py-swagger \
	 auto-license

all: clean \
	 docker-build \
	 compile-go \
	 compile-python \
	 compile-swagger
