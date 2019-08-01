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

// TODO: (Mourad) integerate this it when https://github.com/kubernetes/kubernetes/issues/28486 has been fixed
// Optional number of failed pods to retain. This will be especially good for when restart is True since the underlaying pods will disapear.

// PolyaxonBaseJobSpec defines the desired state of PolyaxonPod
type PolyaxonBaseJobSpec struct {
	// Specifies the number of retries before marking this job failed.
	// +optional
	MaxRetries *int32 `json:"maxRetries,omitempty" default:"1" protobuf:"varint,1,opt,name=replicas"`
	// Template describes the pods that will be created.
	Template corev1.PodTemplateSpec `json:"template" protobuf:"bytes,3,opt,name=template"`
}

// PolyaxonBaseJobStatus defines the observed state of PolyaxonBaseJob
type PolyaxonBaseJobStatus struct {
	// The latest available observations of an object's current state.
	// +optional
	// +patchMergeKey=type
	// +patchStrategy=merge
	Conditions []PolyaxonBaseJobCondition `json:"conditions,omitempty" patchStrategy:"merge" patchMergeKey:"type" protobuf:"bytes,1,rep,name=conditions"`

	// Represents the time when the job was acknowledged by the controller.
	// It is not guaranteed to be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	StartTime *metav1.Time `json:"startTime,omitempty"`

	// Represents the time when the job was completed. It is not guaranteed to
	// be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	CompletionTime *metav1.Time `json:"completionTime,omitempty"`

	// Represents the last time when the job was reconciled.
	// It is not guaranteed to be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	LastReconcileTime *metav1.Time `json:"lastReconcileTime,omitempty"`
}

// PolyaxonBaseJobCondition defines the conditions of PolyaxonBaseJobStatus
type PolyaxonBaseJobCondition struct {
	// Type is the type of the condition. Possible values are Running|Warning|Stopped|Succeeded|Failed
	Type PolyaxonBaseJobConditionType `json:"type"`

	// Status of the condition, one of True, False, Unknown.
	Status corev1.ConditionStatus `json:"status"`

	// The last time this condition was updated.
	// +optional
	LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty"`

	// Last time the condition transitioned.
	// +optional
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`

	// The reasonfor this container condition.
	// +optional
	Reason string `json:"reason,omitempty"`

	// A human readable message indicating details about the transition.
	// +optional
	Message string `json:"message,omitempty"`
}

// PolyaxonBaseJobConditionType maps the conditions a polyaxon job once deployed on
type PolyaxonBaseJobConditionType string

const (
	// JobStarting means underlaying Job has started.
	JobStarting PolyaxonBaseJobConditionType = "Starting"
	// JobRunning means underlaying Job is running,
	JobRunning PolyaxonBaseJobConditionType = "Running"
	// JobWarning means underlaying Job has some issues.
	JobWarning PolyaxonBaseJobConditionType = "Warning"
	// JobSucceeded means underlaying Job has completed successfully.
	JobSucceeded PolyaxonBaseJobConditionType = "Succeeded"
	// JobFailed means underlaying Job has failed.
	JobFailed PolyaxonBaseJobConditionType = "Failed"
	// JobStopped means that the Job was stopped/killed.
	JobStopped PolyaxonBaseJobConditionType = "Stopped"
)

// newPlxBaseJobCondition makes a new instance of PlxBaseJobcondition
func newPlxBaseJobCondition(conditionType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) PolyaxonBaseJobCondition {
	return PolyaxonBaseJobCondition{
		Type:               conditionType,
		Status:             status,
		LastUpdateTime:     metav1.Now(),
		LastTransitionTime: metav1.Now(),
		Reason:             reason,
		Message:            message,
	}
}

// getOrUpdatePlxBaseJobCondition get new or updated version of current confition or returns nil if nothing changed
func getOrUpdatePlxBaseJobCondition(currentCond *PolyaxonBaseJobCondition, conditionType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) *PolyaxonBaseJobCondition {
	newCond := newPlxBaseJobCondition(conditionType, status, reason, message)

	// Do nothing if condition doesn't change
	if currentCond != nil && currentCond.Status == newCond.Status && currentCond.Reason == newCond.Reason {
		return nil
	}

	// Do not update lastTransitionTime if the status of the condition doesn't change.
	if currentCond != nil && currentCond.Status == newCond.Status {
		newCond.LastTransitionTime = currentCond.LastTransitionTime
	}

	return &newCond
}

// getPlxBaseJobConditionFromStatus returns the condition with the specific type form status.conditions
func getPlxBaseJobConditionFromStatus(status PolyaxonBaseJobStatus, condType PolyaxonBaseJobConditionType) *PolyaxonBaseJobCondition {
	for _, condition := range status.Conditions {
		if condition.Type == condType {
			return &condition
		}
	}
	return nil
}

// hasPlxBaseJobCondition checks if a status has a specific condition type
func hasPlxBaseJobCondition(status PolyaxonBaseJobStatus, condType PolyaxonBaseJobConditionType) bool {
	cond := getPlxBaseJobConditionFromStatus(status, condType)
	if cond != nil && cond.Status == corev1.ConditionTrue {
		return true
	}
	return false
}

func isStarting(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobStarting)
}

func isRunning(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobRunning)
}

func hasWarning(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobWarning)
}

func isSucceeded(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobSucceeded)
}

func isFailed(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobFailed)
}

func isStopped(status PolyaxonBaseJobStatus) bool {
	return hasPlxBaseJobCondition(status, JobStopped)
}
