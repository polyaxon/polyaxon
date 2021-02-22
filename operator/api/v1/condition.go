/*
Copyright 2018-2021 Polyaxon, Inc.

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

package v1

import (
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// OperationCondition defines the conditions of Operation or OpService
// +k8s:openapi-gen=true
type OperationCondition struct {
	// Type is the type of the condition.
	Type OperationConditionType `json:"type" protobuf:"bytes,1,opt,name=type"`

	// Status of the condition, one of True, False, Unknown.
	Status corev1.ConditionStatus `json:"status" protobuf:"bytes,2,opt,name=status"`

	// The last time this condition was updated.
	// +optional
	LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty" protobuf:"bytes,3,opt,name=lastUpdateTime"`

	// Last time the condition transitioned.
	// +optional
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty" protobuf:"bytes,4,opt,name=lastTransitionTime"`

	// The reason for this container condition.
	// +optional
	Reason string `json:"reason,omitempty" protobuf:"bytes,5,opt,name=reason"`

	// A human readable message indicating details about the transition.
	// +optional
	Message string `json:"message,omitempty" protobuf:"bytes,6,opt,name=message"`
}

// OperationTriggerNotificationType maps the notifiable conditions
// +k8s:openapi-gen=true
type OperationTriggerNotificationType string

const (
	// OperationSucceededTrigger means underlaying Operation has completed successfully.
	OperationSucceededTrigger OperationTriggerNotificationType = "Succeeded"
	// OperationFailedTrigger means underlaying Operation has failed.
	OperationFailedTrigger OperationTriggerNotificationType = "Failed"
	// OperationStoppedTrigger means that the Operation was stopped/killed.
	OperationStoppedTrigger OperationTriggerNotificationType = "Stopped"
	// OperationDoneTrigger means that the Operation was stopped/killed.
	OperationDoneTrigger OperationTriggerNotificationType = "Done"
)

// OperationConditionType maps the conditions of a job or service once deployed
// +k8s:openapi-gen=true
type OperationConditionType string

const (
	// OperationStarting means underlaying Operation has started.
	OperationStarting OperationConditionType = "Starting"
	// OperationRunning means underlaying Operation is running,
	OperationRunning OperationConditionType = "Running"
	// OperationWarning means underlaying Operation has some issues.
	OperationWarning OperationConditionType = "Warning"
	// OperationSucceeded means underlaying Operation has completed successfully.
	OperationSucceeded OperationConditionType = "Succeeded"
	// OperationFailed means underlaying Operation has failed.
	OperationFailed OperationConditionType = "Failed"
	// OperationStopped means that the Operation was stopped/killed.
	OperationStopped OperationConditionType = "Stopped"
)

// NewOperationCondition makes a new instance of OperationCondition
func NewOperationCondition(conditionType OperationConditionType, status corev1.ConditionStatus, reason, message string) OperationCondition {
	return OperationCondition{
		Type:               conditionType,
		Status:             status,
		LastUpdateTime:     metav1.Now(),
		LastTransitionTime: metav1.Now(),
		Reason:             reason,
		Message:            message,
	}
}

func GetFailureMessage(entityMessage string, status OperationConditionType, reason string, message string) string {
	newMessage := entityMessage
	if status == OperationFailed && message != "" {
		newMessage = newMessage + " (Pod: <reason: " + reason + ", message " + message + ")"
	}
	return newMessage
}

// getOrUpdateOperationCondition get new or updated version of current confition or returns nil if nothing changed
func getOrUpdateOperationCondition(currentCond *OperationCondition, conditionType OperationConditionType, status corev1.ConditionStatus, reason, message string) (*OperationCondition, bool) {
	newCond := NewOperationCondition(conditionType, status, reason, message)

	// Do nothing if condition doesn't change
	if currentCond != nil && currentCond.Type == newCond.Type && currentCond.Status == newCond.Status && currentCond.Reason == newCond.Reason {
		// Always update final states
		if currentCond.Type == OperationSucceeded || currentCond.Type == OperationFailed || currentCond.Type == OperationStopped {
			return &newCond, true
		}
		return &newCond, false
	}

	// Do not update lastTransitionTime if the status of the condition doesn't change.
	if currentCond != nil && currentCond.Status == newCond.Status {
		newCond.LastTransitionTime = currentCond.LastTransitionTime
	}

	return &newCond, true
}

// getLastEntityCondition returns the condition with the specific type form status.conditions
func getLastEntityCondition(status OperationStatus, condType OperationConditionType) *OperationCondition {
	if len(status.Conditions) > 0 {
		return &status.Conditions[len(status.Conditions)-1]
	}
	return nil
}

// getEntityConditionFromStatus returns the condition with the specific type form status.conditions
func getEntityConditionFromStatus(status OperationStatus, condType OperationConditionType) *OperationCondition {
	for _, condition := range status.Conditions {
		if condition.Type == condType {
			return &condition
		}
	}
	return nil
}

// hasOperationCondition checks if a status has a specific condition type
func hasOperationCondition(status OperationStatus, condType OperationConditionType) bool {
	cond := getEntityConditionFromStatus(status, condType)
	if cond != nil && cond.Status == corev1.ConditionTrue {
		return true
	}
	return false
}

// hasOperationCondition checks if a status's last codition is of a specific type
func hasLastOperationCondition(status OperationStatus, condType OperationConditionType) bool {
	cond := status.Conditions[len(status.Conditions)-1]
	if cond.Type == condType && cond.Status == corev1.ConditionTrue {
		return true
	}
	return false
}

// isOperationStarting checks if an ml operation status is in starting condition
func isOperationStarting(status OperationStatus) bool {
	return hasLastOperationCondition(status, OperationStarting)
}

// isOperationRunning checks if an ml operation status is in running condition
func isOperationRunning(status OperationStatus) bool {
	return hasLastOperationCondition(status, OperationRunning)
}

// isOperationWarning checks if an ml operation status is in warning condition
func isOperationWarning(status OperationStatus) bool {
	return hasLastOperationCondition(status, OperationWarning)
}

// isOperationSucceeded checks if an ml operation status is succeeded
func isOperationSucceeded(status OperationStatus) bool {
	return hasOperationCondition(status, OperationSucceeded)
}

// isOperationFailed checks if an ml operation status is failed
func isOperationFailed(status OperationStatus) bool {
	return hasOperationCondition(status, OperationFailed)
}

// isOperationStopped checks if an ml operation status is stopped
func isOperationStopped(status OperationStatus) bool {
	return hasOperationCondition(status, OperationStopped)
}
