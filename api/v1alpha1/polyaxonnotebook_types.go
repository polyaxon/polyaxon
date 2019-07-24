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

// PolyaxonNotebook is the Schema for the polyaxonnotebooks API
// +k8s:openapi-gen=true
// +kubebuilder:subresource:status
type PolyaxonNotebook struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonDeploymentSpec   `json:"spec,omitempty"`
	Status PolyaxonDeploymentStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the notebook is being deleted
func (instance *PolyaxonNotebook) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonNotebookFinalizerName registration
const PolyaxonNotebookFinalizerName = "notebook.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonNotebook
func (instance *PolyaxonNotebook) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonNotebookFinalizerName)
}

// AddFinalizer handler for PolyaxonNotebook
func (instance *PolyaxonNotebook) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonNotebookFinalizerName)
}

// RemoveFinalizer handler for PolyaxonNotebook
func (instance *PolyaxonNotebook) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonNotebookFinalizerName)
}

// +kubebuilder:object:root=true

// PolyaxonNotebookList contains a list of PolyaxonNotebook
type PolyaxonNotebookList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonNotebook `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonNotebook{}, &PolyaxonNotebookList{})
}
