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
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"

	kfcommonv1 "github.com/kubeflow/tf-operator/pkg/apis/common/v1"
	tfjobv1 "github.com/kubeflow/tf-operator/pkg/apis/tensorflow/v1"
)

// CopyTFJobFields copies the owned fields from one TFJob to another
// Returns true if the fields copied from don't match to.
func CopyTFJobFields(from, to *tfjobv1.TFJob) bool {
	requireUpdate := false
	for k, v := range to.Labels {
		if from.Labels[k] != v {
			requireUpdate = true
		}
	}
	to.Labels = from.Labels

	// TODO: Add copy logic

	return requireUpdate
}

// GenerateTFJob returns a a TFJob given a a KFSpec
func GenerateTFJob(
	name string,
	namespace string,
	labels map[string]string,
	spec corev1alpha1.KFSpec,
) *tfjobv1.TFJob {
	tfReplocSpecs := map[tfjobv1.TFReplicaType]*kfcommonv1.ReplicaSpec{}
	for k, v := range spec.ReplicaSpecs {
		tfReplocSpecs[tfjobv1.TFReplicaType(k)] = &v
	}

	tfJobSpec := tfjobv1.TFJobSpec{
		ActiveDeadlineSeconds:   spec.ActiveDeadlineSeconds,
		BackoffLimit:            spec.MaxRetries,
		CleanPodPolicy:          spec.CleanPodPolicy,
		TTLSecondsAfterFinished: spec.TTLSecondsAfterFinished,
		TFReplicaSpecs:          tfReplocSpecs,
	}

	tfJob := &tfjobv1.TFJob{
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: tfJobSpec,
	}

	return tfJob
}
