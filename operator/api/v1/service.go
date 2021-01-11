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

package v1

import (
	corev1 "k8s.io/api/core/v1"
)

// ServiceSpec defines the desired state of a service
// +k8s:openapi-gen=true
type ServiceSpec struct {
	// Replicas is the number of desired replicas.
	// This is a pointer to distinguish between explicit zero and unspecified.
	// Defaults to 1.
	// +optional
	Replicas *int32 `json:"replicas,omitempty" default:"1" protobuf:"varint,1,opt,name=replicas"`

	// optional
	// List of ports to expose on the service
	Ports []int32 `json:"ports,omitempty" protobuf:"varint,2,rep,name=ports"`

	// Template describes the pods that will be created.
	Template corev1.PodTemplateSpec `json:"template" protobuf:"bytes,3,opt,name=template"`
}
