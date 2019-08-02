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

// IsStarting checks if the PolyaxonBuild is statrting
func (instance *PolyaxonBuild) IsStarting() bool {
	return isJobStarting(instance.Status)
}

// IsRunning checks if the PolyaxonBuild is running
func (instance *PolyaxonBuild) IsRunning() bool {
	return isJobRunning(instance.Status)
}

// HasWarning checks if the PolyaxonBuild succeeded
func (instance *PolyaxonBuild) HasWarning() bool {
	return isJobWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonBuild succeeded
func (instance *PolyaxonBuild) IsSucceeded() bool {
	return isJobSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonBuild failed
func (instance *PolyaxonBuild) IsFailed() bool {
	return isJobFailed(instance.Status)
}

// IsStopped checks if the PolyaxonBuild stopped
func (instance *PolyaxonBuild) IsStopped() bool {
	return isJobStopped(instance.Status)
}

// IsDone checks if it the PolyaxonBuild reached a final condition
func (instance *PolyaxonBuild) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonBuild) removeCondition(conditionType PolyaxonBaseJobConditionType) {
	var newConditions []PolyaxonBaseJobCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonBuild) logCondition(condType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxBaseJobConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxBaseJobCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonBuild to statrting
func (instance *PolyaxonBuild) LogStarting() {
	instance.logCondition(JobStarting, corev1.ConditionTrue, "PolyaxonBuildStarted", "Build is starting")
}

// LogRunning sets PolyaxonBuild to running
func (instance *PolyaxonBuild) LogRunning() {
	instance.logCondition(JobRunning, corev1.ConditionTrue, "PolyaxonBuildRunning", "Build is running")
}

// LogWarning sets PolyaxonBuild to Warning
func (instance *PolyaxonBuild) LogWarning(reason, message string) {
	instance.logCondition(JobWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonBuild to succeeded
func (instance *PolyaxonBuild) LogSucceeded() {
	instance.logCondition(JobSucceeded, corev1.ConditionFalse, "PolyaxonBuildSucceeded", "Build has succeded")
}

// LogFailed sets PolyaxonBuild to failed
func (instance *PolyaxonBuild) LogFailed(reason, message string) {
	instance.logCondition(JobFailed, corev1.ConditionFalse, reason, message)
}

// LogStopped sets PolyaxonBuild to stopped
func (instance *PolyaxonBuild) LogStopped(reason, message string) {
	instance.logCondition(JobStopped, corev1.ConditionFalse, reason, message)
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
