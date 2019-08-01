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

// PolyaxonExperiment is the Schema for the polyaxonexperiments API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxxp
// +kubebuilder:subresource:status
type PolyaxonExperiment struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonBaseJobSpec   `json:"spec,omitempty"`
	Status PolyaxonBaseJobStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the experiment is being deleted
func (instance *PolyaxonExperiment) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonExperimentFinalizerName registration
const PolyaxonExperimentFinalizerName = "experiment.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonExperiment
func (instance *PolyaxonExperiment) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonExperimentFinalizerName)
}

// AddFinalizer handler for PolyaxonExperiment
func (instance *PolyaxonExperiment) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonExperimentFinalizerName)
}

// RemoveFinalizer handler for PolyaxonExperiment
func (instance *PolyaxonExperiment) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonExperimentFinalizerName)
}

// +kubebuilder:object:root=true

// PolyaxonExperimentList contains a list of PolyaxonExperiment
type PolyaxonExperimentList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonExperiment `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonExperiment{}, &PolyaxonExperimentList{})
}
