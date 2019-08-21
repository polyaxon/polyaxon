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

// IsStarting checks if the PolyaxonExperiment is statrting
func (instance *PolyaxonExperiment) IsStarting() bool {
	return isJobStarting(instance.Status)
}

// IsRunning checks if the PolyaxonExperiment is running
func (instance *PolyaxonExperiment) IsRunning() bool {
	return isJobRunning(instance.Status)
}

// HasWarning checks if the PolyaxonExperiment succeeded
func (instance *PolyaxonExperiment) HasWarning() bool {
	return isJobWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonExperiment succeeded
func (instance *PolyaxonExperiment) IsSucceeded() bool {
	return isJobSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonExperiment failed
func (instance *PolyaxonExperiment) IsFailed() bool {
	return isJobFailed(instance.Status)
}

// IsStopped checks if the PolyaxonExperiment stopped
func (instance *PolyaxonExperiment) IsStopped() bool {
	return isJobStopped(instance.Status)
}

// IsDone checks if it the PolyaxonExperiment reached a final condition
func (instance *PolyaxonExperiment) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonExperiment) removeCondition(conditionType PolyaxonBaseJobConditionType) {
	var newConditions []PolyaxonBaseJobCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonExperiment) logCondition(condType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxBaseJobConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxBaseJobCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonExperiment to statrting
func (instance *PolyaxonExperiment) LogStarting() {
	instance.logCondition(JobStarting, corev1.ConditionTrue, "PolyaxonExperimentStarted", "Experiment is starting")
}

// LogRunning sets PolyaxonExperiment to running
func (instance *PolyaxonExperiment) LogRunning() {
	instance.logCondition(JobRunning, corev1.ConditionTrue, "PolyaxonExperimentRunning", "Experiment is running")
}

// LogWarning sets PolyaxonExperiment to succeeded
func (instance *PolyaxonExperiment) LogWarning(reason, message string) {
	if reason == "" {
		reason = "PolyaxonExperimentWarning"
	}
	if message == "" {
		message = "Underlaying job has an issue"
	}
	instance.logCondition(JobWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonExperiment to succeeded
func (instance *PolyaxonExperiment) LogSucceeded() {
	instance.logCondition(JobSucceeded, corev1.ConditionTrue, "PolyaxonExperimentSucceeded", "Experiment has succeded")
}

// LogFailed sets PolyaxonExperiment to failed
func (instance *PolyaxonExperiment) LogFailed(reason, message string) {
	instance.logCondition(JobFailed, corev1.ConditionTrue, reason, message)
}

// LogStopped sets PolyaxonExperiment to stopped
func (instance *PolyaxonExperiment) LogStopped(reason, message string) {
	instance.logCondition(JobStopped, corev1.ConditionTrue, reason, message)
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
