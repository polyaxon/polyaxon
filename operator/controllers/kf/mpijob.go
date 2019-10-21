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

package kf

import (
	"reflect"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"

	mpijobv1 "github.com/kubeflow/mpi-operator/pkg/apis/kubeflow/v1alpha2"
	kfcommonv1 "github.com/kubeflow/tf-operator/pkg/apis/common/v1"
)

// CopyMPIJobFields copies the owned fields from one MPIJob to another
// Returns true if the fields copied from don't match to.
func CopyMPIJobFields(from, to *mpijobv1.MPIJob) bool {
	requireUpdate := false
	for k, v := range to.Labels {
		if from.Labels[k] != v {
			requireUpdate = true
		}
	}
	to.Labels = from.Labels

	if to.Spec.ActiveDeadlineSeconds != from.Spec.ActiveDeadlineSeconds {
		to.Spec.ActiveDeadlineSeconds = from.Spec.ActiveDeadlineSeconds
		requireUpdate = true
	}

	if to.Spec.BackoffLimit != from.Spec.BackoffLimit {
		to.Spec.BackoffLimit = from.Spec.BackoffLimit
		requireUpdate = true
	}

	if to.Spec.CleanPodPolicy != from.Spec.CleanPodPolicy {
		to.Spec.CleanPodPolicy = from.Spec.CleanPodPolicy
		requireUpdate = true
	}

	if !reflect.DeepEqual(to.Spec, from.Spec) {
		requireUpdate = true
		to.Spec = from.Spec
	}

	return requireUpdate
}

// Use kfcommon utils generateKFReplica as soon as MPIJob starts using common repo
func generateMPIReplica(plxKFReplicSpec kfcommonv1.ReplicaSpec) *mpijobv1.ReplicaSpec {
	return &mpijobv1.ReplicaSpec{
		Replicas:      plxKFReplicSpec.Replicas,
		RestartPolicy: mpijobv1.RestartPolicy(plxKFReplicSpec.RestartPolicy),
		Template: corev1.PodTemplateSpec{
			ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}},
			Spec:       plxKFReplicSpec.Template.Spec,
		},
	}
}

// GenerateMPIJob returns a a MPIJob given a a KFSpec
func GenerateMPIJob(
	name string,
	namespace string,
	labels map[string]string,
	spec corev1alpha1.KFSpec,
) *mpijobv1.MPIJob {
	mpiReplicaSpecs := map[mpijobv1.MPIReplicaType]*mpijobv1.ReplicaSpec{}
	for k, v := range spec.ReplicaSpecs {
		mpiReplicaSpecs[mpijobv1.MPIReplicaType(k)] = generateMPIReplica(v)
	}

	// copy all of the labels to the pod including pod default related labels
	for _, replicaSpec := range mpiReplicaSpecs {
		l := &replicaSpec.Template.ObjectMeta.Labels
		for k, v := range labels {
			(*l)[k] = v
		}
	}

	CleanPodPolicy := mpijobv1.CleanPodPolicy(*spec.CleanPodPolicy)
	tfJobSpec := mpijobv1.MPIJobSpec{
		ActiveDeadlineSeconds: spec.ActiveDeadlineSeconds,
		BackoffLimit:          spec.BackoffLimit,
		CleanPodPolicy:        &CleanPodPolicy,
		MPIReplicaSpecs:       mpiReplicaSpecs,
	}

	tfJob := &mpijobv1.MPIJob{
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: tfJobSpec,
	}

	return tfJob
}

// GetKFCommonCondFromMPICond generates a new common Job cond based on the MPIJobCond struct
func GetKFCommonCondFromMPICond(cond mpijobv1.JobCondition) kfcommonv1.JobCondition {
	return kfcommonv1.JobCondition{
		Type:               kfcommonv1.JobConditionType(cond.Type),
		Status:             cond.Status,
		Reason:             cond.Reason,
		Message:            cond.Message,
		LastUpdateTime:     cond.LastUpdateTime,
		LastTransitionTime: cond.LastTransitionTime,
	}
}
