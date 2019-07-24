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

// PolyaxonTensorboard is the Schema for the polyaxontensorboards API
// +k8s:openapi-gen=true
// +kubebuilder:subresource:status
type PolyaxonTensorboard struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonDeploymentSpec   `json:"spec,omitempty"`
	Status PolyaxonDeploymentStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the notebook is being deleted
func (instance *PolyaxonTensorboard) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonTensorboardFinalizerName registration
const PolyaxonTensorboardFinalizerName = "tensorboard.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonTensorboard
func (instance *PolyaxonTensorboard) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonTensorboardFinalizerName)
}

// AddFinalizer handler for PolyaxonTensorboard
func (instance *PolyaxonTensorboard) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonTensorboardFinalizerName)
}

// RemoveFinalizer handler for PolyaxonTensorboard
func (instance *PolyaxonTensorboard) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonTensorboardFinalizerName)
}

// +kubebuilder:object:root=true

// PolyaxonTensorboardList contains a list of PolyaxonTensorboard
type PolyaxonTensorboardList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonTensorboard `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonTensorboard{}, &PolyaxonTensorboardList{})
}
