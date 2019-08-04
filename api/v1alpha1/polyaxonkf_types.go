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

	kfcommonv1 "github.com/kubeflow/tf-operator/pkg/apis/common/v1"
)

// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// KFSpec defines the desired state of PolyaxonKFJob
type KFSpec struct {
	// Specifies the Kubeflow kind opertor to use
	KFKind KFKind `json:"kfKind"`

	// Specifies the number of retries before marking this job failed.
	// +optional
	MaxRetries *int32 `json:"maxRetries,omitempty" default:"1" protobuf:"varint,1,opt,name=replicas"`

	// Specifies the duration (in seconds) since startTime during which the job can remain active
	// before it is terminated. Must be a positive integer.
	// This setting applies only to pods where restartPolicy is OnFailure or Always.
	// +optional
	ActiveDeadlineSeconds *int64 `json:"activeDeadlineSeconds,omitempty"`

	// Defines the policy for cleaning up pods after the Job completes.
	// Defaults to Running.
	CleanPodPolicy *kfcommonv1.CleanPodPolicy `json:"cleanPodPolicy,omitempty"`

	// Defines the TTL for cleaning up finished Jobs (temporary
	// before kubernetes adds the cleanup controller)
	TTLSecondsAfterFinished *int32 `json:"ttlSecondsAfterFinished,omitempty"`

	// `ReplicaSpecs` contains maps from `KFReplicaType` to `ReplicaSpec` that
	// specify the corresponding replicas to run.
	ReplicaSpecs map[KFReplicaType]kfcommonv1.ReplicaSpec `json:"replicaSpecs"`
	// NOTE: The usage of map[KFReplicaType]kfcommonv1.ReplicaSpec instead of map[KFReplicaType]*kfcommonv1.ReplicaSpec
	// is to avoid an apimachinery error: map values must be a named type, not *ast.StarExpr
	// so replicaSpecs must be passed by ref (&) when generating corresponding jobs
}

// KFReplicaType is the type for KF Replica.
type KFReplicaType kfcommonv1.ReplicaType

const (
	// KFReplicaTypeLauncher is the type for launcher replica.
	KFReplicaTypeLauncher KFReplicaType = "Launcher"

	// KFReplicaTypeWorker is the type for worker replicas.
	KFReplicaTypeWorker KFReplicaType = "Worker"

	// KFReplicaTypePS is the type for parameter servers.
	KFReplicaTypePS KFReplicaType = "PS"

	// KFReplicaTypeChief is the type for chief worker.
	KFReplicaTypeChief KFReplicaType = "Chief"

	// TFReplicaTypeMaster is the type for master worker.
	TFReplicaTypeMaster KFReplicaType = "Master"

	// KFReplicaTypeEval is the type for evaluation replica (TF).
	KFReplicaTypeEval KFReplicaType = "Evaluator"

	// KFReplicaTypeScheduler is the type for scheduler replica (MXNet).
	KFReplicaTypeScheduler KFReplicaType = "Scheduler"

	// KFReplicaTypeServer is the type for parameter servers (MXNet).
	KFReplicaTypeServer KFReplicaType = "Server"
)

// +kubebuilder:object:root=true

// PolyaxonKF is the Schema for the polyaxonkfs API to manage Kubeflow operators
// +k8s:openapi-gen=true
// +kubebuilder:resource:shortName=plxkf
// +kubebuilder:subresource:status
type PolyaxonKF struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	// KFSpec represent the spec to pass to the underlaying KubeFlow operator
	// This vaidation of the spec is handled by the corresponding operator
	Spec   KFSpec                `json:"spec,omitempty"`
	Status PolyaxonBaseJobStatus `json:"status,omitempty"`
}

// KFKind represents the valid Kubeflow kinds
type KFKind string

const (
	// TFJob represent the Tensorflow operator
	TFJob KFKind = "TFJob"
	// PyTorchJob represent the PyTorch operator
	PyTorchJob KFKind = "PyTorchJob"
	// MPIJob represent the MPI operator
	MPIJob KFKind = "MPIJob"
	// MXJob represent the MXNet operator
	MXJob KFKind = "MXJob"
	// XGBoostJob represent the XGBoost operator
	XGBoostJob KFKind = "XGBoostJob"
)

// IsBeingDeleted checks if the kf is being deleted
func (instance *PolyaxonKF) IsBeingDeleted() bool {
	return !instance.ObjectMeta.DeletionTimestamp.IsZero()
}

// PolyaxonKFFinalizerName registration
const PolyaxonKFFinalizerName = "kf.finalizers.polyaxon.com"

// HasFinalizer check for PolyaxonKF
func (instance *PolyaxonKF) HasFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, PolyaxonKFFinalizerName)
}

// AddFinalizer handler for PolyaxonKF
func (instance *PolyaxonKF) AddFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, PolyaxonKFFinalizerName)
}

// RemoveFinalizer handler for PolyaxonKF
func (instance *PolyaxonKF) RemoveFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, PolyaxonKFFinalizerName)
}

// IsStarting checks if the PolyaxonKF is statrting
func (instance *PolyaxonKF) IsStarting() bool {
	return isJobStarting(instance.Status)
}

// IsRunning checks if the PolyaxonKF is running
func (instance *PolyaxonKF) IsRunning() bool {
	return isJobRunning(instance.Status)
}

// HasWarning checks if the PolyaxonKF succeeded
func (instance *PolyaxonKF) HasWarning() bool {
	return isJobWarning(instance.Status)
}

// IsSucceeded checks if the PolyaxonKF succeeded
func (instance *PolyaxonKF) IsSucceeded() bool {
	return isJobSucceeded(instance.Status)
}

// IsFailed checks if the PolyaxonKF failed
func (instance *PolyaxonKF) IsFailed() bool {
	return isJobFailed(instance.Status)
}

// IsStopped checks if the PolyaxonKF stopped
func (instance *PolyaxonKF) IsStopped() bool {
	return isJobStopped(instance.Status)
}

// IsDone checks if it the PolyaxonKF reached a final condition
func (instance *PolyaxonKF) IsDone() bool {
	return instance.IsSucceeded() || instance.IsFailed() || instance.IsStopped()
}

func (instance *PolyaxonKF) removeCondition(conditionType PolyaxonBaseJobConditionType) {
	var newConditions []PolyaxonBaseJobCondition
	for _, c := range instance.Status.Conditions {

		if c.Type == conditionType {
			continue
		}

		newConditions = append(newConditions, c)
	}
	instance.Status.Conditions = newConditions
}

func (instance *PolyaxonKF) logCondition(condType PolyaxonBaseJobConditionType, status corev1.ConditionStatus, reason, message string) {
	currentCond := getPlxBaseJobConditionFromStatus(instance.Status, condType)
	cond := getOrUpdatePlxBaseJobCondition(currentCond, condType, status, reason, message)
	if cond != nil {
		instance.removeCondition(condType)
		instance.Status.Conditions = append(instance.Status.Conditions, *cond)
	}
}

// LogStarting sets PolyaxonKF to statrting
func (instance *PolyaxonKF) LogStarting() {
	instance.logCondition(JobStarting, corev1.ConditionTrue, "PolyaxonKFStarted", "KF is starting")
}

// LogRunning sets PolyaxonKF to running
func (instance *PolyaxonKF) LogRunning() {
	instance.logCondition(JobRunning, corev1.ConditionTrue, "PolyaxonKFRunning", "KF is running")
}

// LogWarning sets PolyaxonKF to Warning
func (instance *PolyaxonKF) LogWarning(reason, message string) {
	instance.logCondition(JobWarning, corev1.ConditionTrue, reason, message)
}

// LogSucceeded sets PolyaxonKF to succeeded
func (instance *PolyaxonKF) LogSucceeded() {
	instance.logCondition(JobSucceeded, corev1.ConditionFalse, "PolyaxonKFSucceeded", "KF has succeded")
}

// LogFailed sets PolyaxonKF to failed
func (instance *PolyaxonKF) LogFailed(reason, message string) {
	instance.logCondition(JobFailed, corev1.ConditionFalse, reason, message)
}

// LogStopped sets PolyaxonKF to stopped
func (instance *PolyaxonKF) LogStopped(reason, message string) {
	instance.logCondition(JobStopped, corev1.ConditionFalse, reason, message)
}

// +kubebuilder:object:root=true

// PolyaxonKFList contains a list of PolyaxonKF
type PolyaxonKFList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PolyaxonKF `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PolyaxonKF{}, &PolyaxonKFList{})
}
