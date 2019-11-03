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
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// +kubebuilder:object:root=true

// PolyaxonNotebook is the Schema for the polyaxonnotebooks API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxnb
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

// IsStarting checks if the PolyaxonNotebook is statrting
func (instance *PolyaxonNotebook) IsStarting() bool {
	return isDepStarting(instance.Status)
}

// IsRunning checks if the PolyaxonNotebook is running
func (instance *PolyaxonNotebook) IsRunning() bool {
	return isDepRunning(instance.Status)
}

// HasWarning checks if the PolyaxonNotebook succeeded
func (instance *PolyaxonNotebook) HasWarning() bool {
	return isDepWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonNotebook succeeded
func (instance *PolyaxonNotebook) IsSucceeded() bool {
	return isDepSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonNotebook failed
func (instance *PolyaxonNotebook) IsFailed() bool {
	return isDepFailed(instance.Status)
}

// IsStopped checks if the PolyaxonNotebook stopped
func (instance *PolyaxonNotebook) IsStopped() bool {
	return isDepStopped(instance.Status)
}

// IsDone checks if it the PolyaxonNotebook reached a final condition
func (instance *PolyaxonNotebook) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonNotebook) removeCondition(conditionType PolyaxonDeploymentConditionType) {
	var newConditions []PolyaxonDeploymentCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonNotebook) logCondition(condType PolyaxonDeploymentConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxDeploymentConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxDeploymentCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonNotebook to statrting
func (instance *PolyaxonNotebook) LogStarting() {
	instance.logCondition(DeploymentStarting, corev1.ConditionTrue, "PolyaxonNotebookStarted", "Notebook is starting")
}

// LogRunning sets PolyaxonNotebook to running
func (instance *PolyaxonNotebook) LogRunning() {
	instance.logCondition(DeploymentRunning, corev1.ConditionTrue, "PolyaxonNotebookRunning", "Notebook is running")
}

// LogWarning sets PolyaxonNotebook to Warning
func (instance *PolyaxonNotebook) LogWarning(reason, message string) {
	instance.logCondition(DeploymentWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonNotebook to succeeded
func (instance *PolyaxonNotebook) LogSucceeded() {
	instance.logCondition(DeploymentSucceeded, corev1.ConditionTrue, "PolyaxonNotebookSucceeded", "Notebook has succeeded")
}

// LogFailed sets PolyaxonNotebook to failed
func (instance *PolyaxonNotebook) LogFailed(reason, message string) {
	instance.logCondition(DeploymentFailed, corev1.ConditionTrue, reason, message)
}

// LogStopped sets PolyaxonNotebook to stopped
func (instance *PolyaxonNotebook) LogStopped(reason, message string) {
	instance.logCondition(DeploymentStopped, corev1.ConditionTrue, reason, message)
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
