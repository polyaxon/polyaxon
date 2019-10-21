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

// PolyaxonTensorboard is the Schema for the polyaxontensorboards API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxtb
// +kubebuilder:subresource:status
type PolyaxonTensorboard struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PolyaxonDeploymentSpec   `json:"spec,omitempty"`
	Status PolyaxonDeploymentStatus `json:"status,omitempty"`
}

// IsBeingDeleted checks if the Tensorboard is being deleted
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

// IsStarting checks if the PolyaxonTensorboard is statrting
func (instance *PolyaxonTensorboard) IsStarting() bool {
	return isDepStarting(instance.Status)
}

// IsRunning checks if the PolyaxonTensorboard is running
func (instance *PolyaxonTensorboard) IsRunning() bool {
	return isDepRunning(instance.Status)
}

// HasWarning checks if the PolyaxonTensorboard succeeded
func (instance *PolyaxonTensorboard) HasWarning() bool {
	return isDepWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonTensorboard succeeded
func (instance *PolyaxonTensorboard) IsSucceeded() bool {
	return isDepSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonTensorboard failed
func (instance *PolyaxonTensorboard) IsFailed() bool {
	return isDepFailed(instance.Status)
}

// IsStopped checks if the PolyaxonTensorboard stopped
func (instance *PolyaxonTensorboard) IsStopped() bool {
	return isDepStopped(instance.Status)
}

// IsDone checks if it the PolyaxonTensorboard reached a final condition
func (instance *PolyaxonTensorboard) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonTensorboard) removeCondition(conditionType PolyaxonDeploymentConditionType) {
	var newConditions []PolyaxonDeploymentCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonTensorboard) logCondition(condType PolyaxonDeploymentConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxDeploymentConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxDeploymentCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonTensorboard to statrting
func (instance *PolyaxonTensorboard) LogStarting() {
	instance.logCondition(DeploymentStarting, corev1.ConditionTrue, "PolyaxonTensorboardStarted", "Tensorboard is starting")
}

// LogRunning sets PolyaxonTensorboard to running
func (instance *PolyaxonTensorboard) LogRunning() {
	instance.logCondition(DeploymentRunning, corev1.ConditionTrue, "PolyaxonTensorboardRunning", "Tensorboard is running")
}

// LogWarning sets PolyaxonTensorboard to Warning
func (instance *PolyaxonTensorboard) LogWarning(reason, message string) {
	instance.logCondition(DeploymentWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonTensorboard to succeeded
func (instance *PolyaxonTensorboard) LogSucceeded() {
	instance.logCondition(DeploymentSucceeded, corev1.ConditionTrue, "PolyaxonTensorboardSucceeded", "Tensorboard has succeded")
}

// LogFailed sets PolyaxonTensorboard to failed
func (instance *PolyaxonTensorboard) LogFailed(reason, message string) {
	instance.logCondition(DeploymentFailed, corev1.ConditionTrue, reason, message)
}

// LogStopped sets PolyaxonTensorboard to stopped
func (instance *PolyaxonTensorboard) LogStopped(reason, message string) {
	instance.logCondition(DeploymentStopped, corev1.ConditionTrue, reason, message)
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
