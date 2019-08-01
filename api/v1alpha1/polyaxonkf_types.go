/*
Copyright 2019 Polyaxon, Inc.

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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// +kubebuilder:object:root=true

// PolyaxonKF is the Schema for the polyaxonkfs API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxkf
// +kubebuilder:subresource:status
type PolyaxonKF struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	// KFSpec represent the spec to pass to the underlaying KF operator
	KFSpec string                `json:"runSpec,omitempty"`
	Status PolyaxonBaseJobStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// PolyaxonKFList contains a list of PolyaxonKF
type PolyaxonKFList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonKF `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonKF{}, &PolyaxonKFList{})
}
