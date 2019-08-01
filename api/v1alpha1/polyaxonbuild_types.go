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

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// +kubebuilder:object:root=true

// PolyaxonBuild is the Schema for the polyaxonbuilds API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxb
// +kubebuilder:subresource:status
type PolyaxonBuild struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonBaseJobSpec   `json:"spec,omitempty"`
	Status PolyaxonBaseJobStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the build is being deleted
func (instance *PolyaxonBuild) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonBuildFinalizerName registration
const PolyaxonBuildFinalizerName = "build.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonBuild
func (instance *PolyaxonBuild) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonBuildFinalizerName)
}

// AddFinalizer handler for PolyaxonBuild
func (instance *PolyaxonBuild) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonBuildFinalizerName)
}

// RemoveFinalizer handler for PolyaxonBuild
func (instance *PolyaxonBuild) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonBuildFinalizerName)
}

// +kubebuilder:object:root=true

// PolyaxonBuildList contains a list of PolyaxonBuild
type PolyaxonBuildList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonBuild `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonBuild{}, &PolyaxonBuildList{})
}
