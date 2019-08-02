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

// IsStarting checks if the PolyaxonJob is statrting
func (instance *PolyaxonJob) IsStarting() bool {
	return isJobStarting(instance.Status)
}

// IsRunning checks if the PolyaxonJob is running
func (instance *PolyaxonJob) IsRunning() bool {
	return isJobRunning(instance.Status)
}

// HasWarning checks if the PolyaxonJob succeeded
func (instance *PolyaxonJob) HasWarning() bool {
	return isJobWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonJob succeeded
func (instance *PolyaxonJob) IsSucceeded() bool {
	return isJobSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonJob failed
func (instance *PolyaxonJob) IsFailed() bool {
	return isJobFailed(instance.Status)
}

// IsStopped checks if the PolyaxonJob stopped
func (instance *PolyaxonJob) IsStopped() bool {
	return isJobStopped(instance.Status)
}

// IsDone checks if it the PolyaxonJob reached a final condition
func (instance *PolyaxonJob) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonJob) removeCondition(conditionType PolyaxonBaseJobConditionType) {
	var newConditions []PolyaxonBaseJobCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonJob) logCondition(condType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxBaseJobConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxBaseJobCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonJob to statrting
func (instance *PolyaxonJob) LogStarting() {
	instance.logCondition(JobStarting, corev1.ConditionTrue, "PolyaxonJobStarted", "Job is starting")
}

// LogRunning sets PolyaxonJob to running
func (instance *PolyaxonJob) LogRunning() {
	instance.logCondition(JobRunning, corev1.ConditionTrue, "PolyaxonJobRunning", "Job is running")
}

// LogWarning sets PolyaxonJob to succeeded
func (instance *PolyaxonJob) LogWarning(reason, message string) {
	instance.logCondition(JobWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonJob to succeeded
func (instance *PolyaxonJob) LogSucceeded() {
	instance.logCondition(JobSucceeded, corev1.ConditionFalse, "PolyaxonJobSucceeded", "Job has succeded")
}

// LogFailed sets PolyaxonJob to failed
func (instance *PolyaxonJob) LogFailed(reason, message string) {
	instance.logCondition(JobFailed, corev1.ConditionFalse, reason, message)
}

// LogStopped sets PolyaxonJob to stopped
func (instance *PolyaxonJob) LogStopped(reason, message string) {
	instance.logCondition(JobStopped, corev1.ConditionFalse, reason, message)
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
