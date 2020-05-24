/*
Copyright 2018-2020 Polyaxon, Inc.

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

// +kubebuilder:object:root=true

// Operation is the Schema for the operations API
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=op
// +kubebuilder:subresource:status
type Operation struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Specifies the number of retries before marking this job failed.
	// +optional
	Termination TerminationSpec `json:"termination,omitempty" protobuf:"bytes,2,opt,name=termination"`

	// Flag to set a finalizer for collecting logs
	// +optional
	CollectLogs bool `json:"collectLogs" protobuf:"bytes,3,opt,name=collectLogs"`

	// Flag to set tell if Polyaxon should sync statuses with control plane
	// +optional
	SyncStatuses bool `json:"syncStatuses" protobuf:"bytes,4,opt,name=syncStatuses"`

	// List of notigications for this operation
	// +optional
	Notifications []NotificationSpec `json:"notifications,omitempty" protobuf:"bytes,5,opt,name=notifications"`

	// Specification of the desired behavior of a job.
	// +optional
	BatchJobSpec *BatchJobSpec `json:"batchJobSpec,omitempty" protobuf:"bytes,6,opt,name=batchJobSpec"`

	// Specification of the desired behavior of a Service.
	ServiceSpec *ServiceSpec `json:"serviceSpec,omitempty" protobuf:"bytes,7,opt,name=serviceSpec"`

	// Specification of the desired behavior of a TFJob.
	TFJobSpec *TFJobSpec `json:"tfJobSpec,omitempty" protobuf:"bytes,8,opt,name=batchJobSpec"`

	// Specification of the desired behavior of a PytorchJob.
	PytorchJobSpec *PytorchJobSpec `json:"pytorchJobSpec,omitempty" protobuf:"bytes,9,opt,name=pytorchJobSpec"`

	// Specification of the desired behavior of a MPIJob.
	MPIJobSpec *MPIJobSpec `json:"mpiJobSpec,omitempty" protobuf:"bytes,10,opt,name=mpiJobSpec"`

	// Current status of an op.
	// +optional
	Status OperationStatus `json:"status,omitempty" protobuf:"bytes,11,opt,name=status"`
}

// NotificationSpec is definition of how to send notification for new status of this operation
// +k8s:openapi-gen=true
type NotificationSpec struct {
	Connections []string                         `json:"connections" protobuf:"bytes,1,opt,name=connections"`
	Trigger     OperationTriggerNotificationType `json:"trigger" protobuf:"bytes,2,opt,name=trigger"`
}

// IsBeingDeleted checks if the job is being deleted
func (instance *Operation) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// IsStarting checks if the Operation is statrting
func (instance *Operation) IsStarting() bool {
	return isOperationStarting(instance.Status)
}

// IsRunning checks if the Operation is running
func (instance *Operation) IsRunning() bool {
	return isOperationRunning(instance.Status)
}

// HasWarning checks if the Operation succeeded
func (instance *Operation) HasWarning() bool {
	return isOperationWarning(instance.Status)
}

// IsSucceeded checks if the Operation succeeded
func (instance *Operation) IsSucceeded() bool {
	return isOperationSucceeded(instance.Status)
}

// IsFailed checks if the Operation failed
func (instance *Operation) IsFailed() bool {
	return isOperationFailed(instance.Status)
}

// IsStopped checks if the Operation stopped
func (instance *Operation) IsStopped() bool {
	return isOperationStopped(instance.Status)
}

// IsDone checks if it the Operation reached a final condition
func (instance *Operation) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *Operation) removeCondition(conditionType OperationConditionType) {
	var newConditions []OperationCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *Operation) logCondition(condType OperationConditionType, status corev1.ConditionStatus, reason, message string) bool {
	currentCond := getMlEnittyConditionFromStatus(instance.Status, condType)
	cond := getOrUpdateOperationCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
		return true
	}
	return false
}

// LogStarting sets Operation to statrting
func (instance *Operation) LogStarting() bool {
	return instance.logCondition(OperationStarting, corev1.ConditionTrue, "OperationStarted", "Job is starting")
}

// LogRunning sets Operation to running
func (instance *Operation) LogRunning() bool {
	return instance.logCondition(OperationRunning, corev1.ConditionTrue, "OperationRunning", "Job is running")
}

// LogWarning sets Operation to succeeded
func (instance *Operation) LogWarning(reason, message string) bool {
	if reason == "" {
		reason = "OperationWarning"
	}
	if message == "" {
		message = "Underlaying job has an issue"
	}
	return instance.logCondition(OperationWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets Operation to succeeded
func (instance *Operation) LogSucceeded() bool {
	return instance.logCondition(OperationSucceeded, corev1.ConditionTrue, "OperationSucceeded", "Job has succeeded")
}

// LogFailed sets Operation to failed
func (instance *Operation) LogFailed(reason, message string) bool {
	return instance.logCondition(OperationFailed, corev1.ConditionTrue, reason, message)
}

// LogStopped sets Operation to stopped
func (instance *Operation) LogStopped(reason, message string) bool {
	return instance.logCondition(OperationStopped, corev1.ConditionTrue, reason, message)
}

// +kubebuilder:object:root=true

// OperationList contains a list of Operation
type OperationList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Operation `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Operation{}, &OperationList{})
}
