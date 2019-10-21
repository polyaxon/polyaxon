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
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	kfcommonv1 "github.com/kubeflow/tf-operator/pkg/apis/common/v1"
)

// generateKFReplica generates a new ReplocaSpec
func generateKFReplica(plxKFReplicSpec kfcommonv1.ReplicaSpec) *kfcommonv1.ReplicaSpec {
	return &kfcommonv1.ReplicaSpec{
		Replicas:      plxKFReplicSpec.Replicas,
		RestartPolicy: plxKFReplicSpec.RestartPolicy,
		Template: corev1.PodTemplateSpec{
			ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}},
			Spec:       plxKFReplicSpec.Template.Spec,
		},
	}
}
