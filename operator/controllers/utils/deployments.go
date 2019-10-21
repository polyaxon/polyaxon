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

package utils

import (
	"fmt"
	"reflect"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// CopyDeploymentFields copies the owned fields from one Deployment to another
// Returns true if the fields copied from don't match to.
func CopyDeploymentFields(from, to *appsv1.Deployment) bool {
	requireUpdate := false
	for k, v := range to.Labels {
		if from.Labels[k] != v {
			requireUpdate = true
		}
	}
	to.Labels = from.Labels

	if !reflect.DeepEqual(to.Spec.Template.Spec, from.Spec.Template.Spec) {
		requireUpdate = true
	}
	to.Spec.Template.Spec = from.Spec.Template.Spec

	return requireUpdate
}

// IsPlxDeploymentWarning return true if deploymeny is in warning state
func IsPlxDeploymentWarning(ds appsv1.DeploymentStatus, dc appsv1.DeploymentCondition) bool {
	if dc.Type == appsv1.DeploymentReplicaFailure {
		return true
	}
	if dc.Type == appsv1.DeploymentAvailable && dc.Status == corev1.ConditionFalse {
		return true
	}
	if dc.Type == appsv1.DeploymentProgressing && ds.UnavailableReplicas > 0 {
		return true
	}
	return false
}

// IsPlxDeploymentRunning return true if deploymeny is running
func IsPlxDeploymentRunning(ds appsv1.DeploymentStatus, dc appsv1.DeploymentCondition) bool {
	if dc.Type == appsv1.DeploymentProgressing && ds.AvailableReplicas > 0 && ds.ReadyReplicas > 0 {
		return true
	}
	return false
}

// GeneratePlxDeployment returns a deployment given a PolyaxonDeploymentSpec
func GeneratePlxDeployment(
	name string,
	namespace string,
	labels map[string]string,
	port int,
	replicas int32,
	podSpec corev1.PodSpec,
) (*appsv1.Deployment, error) {
	plxDeployment := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}},
				Spec:       podSpec,
			},
		},
	}
	// copy all of the labels to the pod including poddefault related labels
	l := &plxDeployment.Spec.Template.ObjectMeta.Labels
	for k, v := range labels {
		(*l)[k] = v
	}

	// Check container port
	if len(podSpec.Containers) == 0 {
		return nil, fmt.Errorf("Notebook has no container in Spec %q", &podSpec)
	}
	container := &podSpec.Containers[0]
	if container.Ports == nil {
		container.Ports = []corev1.ContainerPort{
			corev1.ContainerPort{
				ContainerPort: int32(port),
				Name:          "notebook-port",
				Protocol:      "TCP",
			},
		}
	}

	return plxDeployment, nil
}
