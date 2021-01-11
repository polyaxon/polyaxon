/*
Copyright 2018-2021 Polyaxon, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package config

import (
	"os"
	"strconv"
)

const (
	// Namespace is a flag to enable TFJob conroller
	Namespace = "POLYAXON_K8S_NAMESPACE"

	// TFJobEnabled is a flag to enable TFJob conroller
	TFJobEnabled = "POLYAXON_TFJOB_ENABLED"

	// PytorchJobEnabled is a flag to enable PytorchJob conroller
	PytorchJobEnabled = "POLYAXON_PYTORCH_JOB_ENABLED"

	// MPIJobEnabled is a flag to enable MPIJob conroller
	MPIJobEnabled = "POLYAXON_MPIJOB_ENABLED"

	// SparkJobEnabled is a flag to enable Spark conroller
	SparkJobEnabled = "POLYAXON_SPARK_JOB_ENABLED"

	// IstioEnabled is a flag to enable istio controller
	IstioEnabled = "POLYAXON_ISTIO_ENABLED"

	// IstioGateway is the istio gateway to use
	IstioGateway = "POLYAXON_ISTIO_GATEWAY"

	// IstioTLSMode is the istio tls mode to use
	IstioTLSMode = "POLYAXON_ISTIO_TLS_MODE"

	// IstioPrefix is the istio tls mode to use
	IstioPrefix = "POLYAXON_ISTIO_PREFIX"

	// IstioTimeout is the istio default timeout
	IstioTimeout = "POLYAXON_ISTIO_TIMEOUT"

	// ClusterDomain is the istio tls mode to use
	ClusterDomain = "POLYAXON_CLUSTER_DOMAIN"

	// ProxyServicesPort port serving services
	ProxyServicesPort = "POLYAXON_PROXY_SERVICES_PORT"
)

// GetStrEnv returns an environment str variable given by key or return a default value.
func GetStrEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

// GetBoolEnv returns an environment bool variable given by key or return a default value.
func GetBoolEnv(key string, defaultValue bool) bool {
	if GetStrEnv(key, "false") == "true" {
		return true
	}
	return defaultValue
}

// GetIntEnv returns an environment int variable given by key or return a default value.
func GetIntEnv(key string, defaultValue int) int {
	if valueStr, ok := os.LookupEnv(key); ok {
		if value, err := strconv.Atoi(valueStr); err == nil {
			return value
		}
	}
	return defaultValue
}

// KFEnabled return a flag to tell if Kubeflow is enabled
func KFEnabled() bool {
	return GetBoolEnv(TFJobEnabled, false) || GetBoolEnv(PytorchJobEnabled, false) || GetBoolEnv(MPIJobEnabled, false)
}
