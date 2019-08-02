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

// PolyaxonDeploymentSpec defines the desired state of PolyaxonDeployment
type PolyaxonDeploymentSpec struct {
	// Replicas is the number of desired replicas.
	// This is a pointer to distinguish between explicit zero and unspecified.
	// Defaults to 1.
	// +optional
	Replicas *int32 `json:"replicas,omitempty" default:"1" protobuf:"varint,1,opt,name=replicas"`
	// Template describes the pods that will be created.
	Template corev1.PodTemplateSpec `json:"template" protobuf:"bytes,3,opt,name=template"`
}

// PolyaxonDeploymentStatus defines the observed state of PolyaxonDeployment
type PolyaxonDeploymentStatus struct {
	// Conditions is an array of current conditions
	Conditions []PolyaxonDeploymentCondition `json:"conditions,omitempty"`

	// ReadyReplicas is the number of Pods created by the StatefulSet controller that have a Ready Condition.
	ReadyReplicas int32 `json:"readyReplicas,omitempty"`
}

// PolyaxonDeploymentCondition defines the conditions of PolyaxonDeploymentStatus
type PolyaxonDeploymentCondition struct {
	// Type is the type of the condition.
	Type PolyaxonDeploymentConditionType `json:"type"`

	// Status of the condition, one of True, False, Unknown.
	Status corev1.ConditionStatus `json:"status"`

	// The last time this condition was updated.
	// +optional
	LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty"`

	// Last time the condition transitioned.
	// +optional
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`

	// (brief) reason the container is in the current state
	// +optional
	Reason string `json:"reason,omitempty"`
	// Message regarding why the container is in the current state.
	// +optional
	Message string `json:"message,omitempty"`
}

// PolyaxonDeploymentConditionType maps the conditions a polyaxon deployment once deployed
type PolyaxonDeploymentConditionType string

const (
	// DeploymentStarting means underlaying Deployment has started.
	DeploymentStarting PolyaxonDeploymentConditionType = "Starting"
	// DeploymentRunning means underlaying Deployment is running,
	DeploymentRunning PolyaxonDeploymentConditionType = "Running"
	// DeploymentWarning means underlaying Deployment has some issues.
	DeploymentWarning PolyaxonDeploymentConditionType = "Warning"
	// DeploymentSucceeded means underlaying JDeploymentob has completed successfully.
	DeploymentSucceeded PolyaxonDeploymentConditionType = "Succeeded"
	// DeploymentFailed means underlaying Deployment has failed.
	DeploymentFailed PolyaxonDeploymentConditionType = "Failed"
	// DeploymentStopped means that the Deployment was stopped/killed.
	DeploymentStopped PolyaxonDeploymentConditionType = "Stopped"
)

// newPlxDeploymentCondition makes a new instance of DeploymentCondition
func newPlxDeploymentCondition(conditionType PolyaxonDeploymentConditionType, status corev1.ConditionStatus, reason, message string) PolyaxonDeploymentCondition {
	return PolyaxonDeploymentCondition{
		Type:               conditionType,
		Status:             status,
		LastUpdateTime:     metav1.Now(),
		LastTransitionTime: metav1.Now(),
		Reason:             reason,
		Message:            message,
	}
}

// getOrUpdatePlxDeploymentCondition get new or updated version of current confition or returns nil if nothing changed
func getOrUpdatePlxDeploymentCondition(currentCond *PolyaxonDeploymentCondition, conditionType PolyaxonDeploymentConditionType, status corev1.ConditionStatus, reason, message string) *PolyaxonDeploymentCondition {
	newCond := newPlxDeploymentCondition(conditionType, status, reason, message)

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

// getPlxDeploymentConditionFromStatus returns the condition with the specific type form status.conditions
func getPlxDeploymentConditionFromStatus(status PolyaxonDeploymentStatus, condType PolyaxonDeploymentConditionType) *PolyaxonDeploymentCondition {
	for _, condition := range status.Conditions {
		if condition.Type == condType {
			return &condition
		}
	}
	return nil
}

// hasPlxDeploymentCondition checks if a status has a specific condition type
func hasPlxDeploymentCondition(status PolyaxonDeploymentStatus, condType PolyaxonDeploymentConditionType) bool {
	cond := getPlxDeploymentConditionFromStatus(status, condType)
	if cond != nil && cond.Status == corev1.ConditionTrue {
		return true
	}
	return false
}

func isDepStarting(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentStarting)
}

func isDepRunning(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentRunning)
}

func isDepWarning(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentWarning)
}

func isDepSucceeded(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentSucceeded)
}

func isDepFailed(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentFailed)
}

func isDepStopped(status PolyaxonDeploymentStatus) bool {
	return hasPlxDeploymentCondition(status, DeploymentStopped)
}
