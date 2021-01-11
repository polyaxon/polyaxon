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

package kfapi

import (
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

// JobStatus represents the current observed state of the training Job.
type JobStatus struct {
	// Conditions is an array of current observed job conditions.
	Conditions []JobCondition `json:"conditions"`

	// ReplicaStatuses is map of ReplicaType and ReplicaStatus,
	// specifies the status of each replica.
	ReplicaStatuses map[ReplicaType]*ReplicaStatus `json:"replicaStatuses"`

	// Represents time when the job was acknowledged by the job controller.
	// It is not guaranteed to be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	StartTime *metav1.Time `json:"startTime,omitempty"`

	// Represents time when the job was completed. It is not guaranteed to
	// be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	CompletionTime *metav1.Time `json:"completionTime,omitempty"`

	// Represents last time when the job was reconciled. It is not guaranteed to
	// be set in happens-before order across separate operations.
	// It is represented in RFC3339 form and is in UTC.
	LastReconcileTime *metav1.Time `json:"lastReconcileTime,omitempty"`
}

// ReplicaType represents the type of the replica. Each operator needs to define its
// own set of ReplicaTypes.
type ReplicaType string

// JobCondition describes the state of the job at a certain point.
type JobCondition struct {
	// Type of job condition.
	Type JobConditionType `json:"type"`
	// Status of the condition, one of True, False, Unknown.
	Status corev1.ConditionStatus `json:"status"`
	// The reason for the condition's last transition.
	Reason string `json:"reason,omitempty"`
	// A human readable message indicating details about the transition.
	Message string `json:"message,omitempty"`
	// The last time this condition was updated.
	LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty"`
	// Last time the condition transitioned from one status to another.
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`
}

// JobConditionType defines all kinds of types of JobStatus.
type JobConditionType string

const (
	// JobCreated means the job has been accepted by the system,
	// but one or more of the pods/services has not been started.
	// This includes time before pods being scheduled and launched.
	JobCreated JobConditionType = "Created"

	// JobRunning means all sub-resources (e.g. services/pods) of this job
	// have been successfully scheduled and launched.
	// The training is running without error.
	JobRunning JobConditionType = "Running"

	// JobRestarting means one or more sub-resources (e.g. services/pods) of this job
	// reached phase failed but maybe restarted according to it's restart policy
	// which specified by user in v1.PodTemplateSpec.
	// The training is freezing/pending.
	JobRestarting JobConditionType = "Restarting"

	// JobSucceeded means all sub-resources (e.g. services/pods) of this job
	// reached phase have terminated in success.
	// The training is complete without error.
	JobSucceeded JobConditionType = "Succeeded"

	// JobFailed means one or more sub-resources (e.g. services/pods) of this job
	// reached phase failed with no restarting.
	// The training has failed its execution.
	JobFailed JobConditionType = "Failed"
)

// ReplicaStatus represents the current observed state of the replica.
type ReplicaStatus struct {
	// The number of actively running pods.
	Active int32 `json:"active,omitempty"`

	// The number of pods which reached phase Succeeded.
	Succeeded int32 `json:"succeeded,omitempty"`

	// The number of pods which reached phase Failed.
	Failed int32 `json:"failed,omitempty"`
}

// MPIJobSpec resource definiton.
type MPIJobSpec struct {

	// Specifies the number of slots per worker used in hostfile.
	// Defaults to 1.
	// +optional
	SlotsPerWorker *int32 `json:"slotsPerWorker,omitempty"`

	// Specifies the number of retries before marking this job failed.
	// Defaults to 6.
	// +optional
	BackoffLimit *int32 `json:"backoffLimit,omitempty"`

	// Specifies the duration in seconds relative to the start time that
	// the job may be active before the system tries to terminate it.
	// Note that this takes precedence over `BackoffLimit` field.
	// +optional
	ActiveDeadlineSeconds *int64 `json:"activeDeadlineSeconds,omitempty"`

	// CleanPodPolicy defines the policy that whether to kill pods after the job completes.
	// Defaults to None.
	CleanPodPolicy *operationv1.CleanPodPolicy `json:"cleanPodPolicy,omitempty"`

	// `MPIReplicaSpecs` contains maps from `MPIReplicaType` to `ReplicaSpec` that
	// specify the MPI replicas to run.
	MPIReplicaSpecs map[operationv1.MPIReplicaType]*operationv1.KFReplicaSpec `json:"mpiReplicaSpecs"`

	// MainContainer specifies name of the main container which
	// executes the MPI code.
	MainContainer string `json:"mainContainer,omitempty"`
}

// PyTorchJobSpec is a desired state description of the PyTorchJob.
type PyTorchJobSpec struct {
	// Specifies the duration (in seconds) since startTime during which the job can remain active
	// before it is terminated. Must be a positive integer.
	// This setting applies only to pods where restartPolicy is OnFailure or Always.
	// +optional
	ActiveDeadlineSeconds *int64 `json:"activeDeadlineSeconds,omitempty"`

	// Number of retries before marking this job as failed.
	// +optional
	BackoffLimit *int32 `json:"backoffLimit,omitempty"`

	// Defines the policy for cleaning up pods after the PyTorchJob completes.
	// Defaults to None.
	CleanPodPolicy *operationv1.CleanPodPolicy `json:"cleanPodPolicy,omitempty"`

	// Defines the TTL for cleaning up finished PyTorchJobs (temporary
	// before Kubernetes adds the cleanup controller).
	// It may take extra ReconcilePeriod seconds for the cleanup, since
	// reconcile gets called periodically.
	// Defaults to infinite.
	TTLSecondsAfterFinished *int32 `json:"ttlSecondsAfterFinished,omitempty"`

	// A map of PyTorchReplicaType (type) to ReplicaSpec (value). Specifies the PyTorch cluster configuration.
	// For example,
	//   {
	//     "Master": PyTorchReplicaSpec,
	//     "Worker": PyTorchReplicaSpec,
	//   }
	PyTorchReplicaSpecs map[operationv1.PyTorchReplicaType]*operationv1.KFReplicaSpec `json:"pytorchReplicaSpecs"`
}

// TFJobSpec is a desired state description of the TFJob.
type TFJobSpec struct {
	// Specifies the duration (in seconds) since startTime during which the job can remain active
	// before it is terminated. Must be a positive integer.
	// This setting applies only to pods where restartPolicy is OnFailure or Always.
	// +optional
	ActiveDeadlineSeconds *int64 `json:"activeDeadlineSeconds,omitempty"`

	// Number of retries before marking this job as failed.
	// +optional
	BackoffLimit *int32 `json:"backoffLimit,omitempty"`

	// Defines the policy for cleaning up pods after the TFJob completes.
	// Defaults to Running.
	CleanPodPolicy *operationv1.CleanPodPolicy `json:"cleanPodPolicy,omitempty"`

	// Defines the TTL for cleaning up finished TFJobs (temporary
	// before kubernetes adds the cleanup controller).
	// It may take extra ReconcilePeriod seconds for the cleanup, since
	// reconcile gets called periodically.
	// Defaults to infinite.
	TTLSecondsAfterFinished *int32 `json:"ttlSecondsAfterFinished,omitempty"`

	// A map of TFReplicaType (type) to ReplicaSpec (value). Specifies the TF cluster configuration.
	// For example,
	//   {
	//     "PS": ReplicaSpec,
	//     "Worker": ReplicaSpec,
	//   }
	TFReplicaSpecs map[operationv1.TFReplicaType]*operationv1.KFReplicaSpec `json:"tfReplicaSpecs"`
}
