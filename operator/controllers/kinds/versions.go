/*
Copyright 2018-2020 Polyaxon, Inc.

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

package kinds

const (
	// MPIJobAPIVersion mpijob api version
	MPIJobAPIVersion = "kubeflow.org/v1"

	// MPIJobKind mpijob kind
	MPIJobKind = "MPIJob"

	// TFJobAPIVersion tfjob api version
	TFJobAPIVersion = "kubeflow.org/v1"

	// TFJobKind tfjob kind
	TFJobKind = "TFJob"

	// PytorchJobAPIVersion pytorchjob api version
	PytorchJobAPIVersion = "kubeflow.org/v1"

	// PytorchJobKind pytorchjob kind
	PytorchJobKind = "PyTorchJob"

	// IstioAPIVersion istio networing api version
	IstioAPIVersion = "networking.istio.io/v1alpha3"

	// IstioVirtualServiceKind istio virtual service kind
	IstioVirtualServiceKind = "VirtualService"

	// SparkAPIVersion Spark operator api version
	SparkAPIVersion = "sparkoperator.k8s.io/v1beta2"

	// SparkApplicationKind Spark application kind
	SparkApplicationKind = "SparkApplication"
)
