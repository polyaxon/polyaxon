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

// PolyaxonJob is the Schema for the polyaxonjobs API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxj
// +kubebuilder:subresource:status
type PolyaxonJob struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonBaseJobSpec   `json:"spec,omitempty"`
	Status PolyaxonBaseJobStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the job is being deleted
func (instance *PolyaxonJob) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonJobFinalizerName registration
const PolyaxonJobFinalizerName = "job.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonJob
func (instance *PolyaxonJob) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonJobFinalizerName)
}

// AddFinalizer handler for PolyaxonJob
func (instance *PolyaxonJob) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonJobFinalizerName)
}

// RemoveFinalizer handler for PolyaxonJob
func (instance *PolyaxonJob) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonJobFinalizerName)
}

// +kubebuilder:object:root=true

// PolyaxonJobList contains a list of PolyaxonJob
type PolyaxonJobList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonJob `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonJob{}, &PolyaxonJobList{})
}
