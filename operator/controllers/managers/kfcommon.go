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

package managers

import (
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

// generateKFReplica generates a new ReplocaSpec
func generateKFReplica(replicSpec operationv1.KFReplicaSpec) *operationv1.KFReplicaSpec {
	return &operationv1.KFReplicaSpec{
		Replicas:      replicSpec.Replicas,
		RestartPolicy: replicSpec.RestartPolicy,
		Template: corev1.PodTemplateSpec{
			ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}},
			Spec:       replicSpec.Template.Spec,
		},
	}
}
