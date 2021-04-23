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

// IsDeploymentWarning return true if deploymeny is in warning state
func IsDeploymentWarning(ds appsv1.DeploymentStatus, dc appsv1.DeploymentCondition) bool {
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

// IsDeploymentRunning return true if deploymeny is running
func IsDeploymentRunning(ds appsv1.DeploymentStatus, dc appsv1.DeploymentCondition) bool {
	if dc.Type == appsv1.DeploymentProgressing && ds.AvailableReplicas > 0 && ds.ReadyReplicas > 0 {
		return true
	}
	if dc.Type == appsv1.DeploymentAvailable && dc.Status == corev1.ConditionTrue {
		return true
	}
	return false
}

// GenerateDeployment returns a deployment given a MlDeploymentSpec
func GenerateDeployment(
	name string,
	namespace string,
	labels map[string]string,
	annotations map[string]string,
	ports []int32,
	replicas int32,
	spec corev1.PodSpec,
) (*appsv1.Deployment, error) {
	deployment := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:        name,
			Namespace:   namespace,
			Labels:      labels,
			Annotations: annotations,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}, Annotations: map[string]string{}},
				Spec:       spec,
			},
		},
	}
	// copy all of the labels to the pod including poddefault related labels
	l := &deployment.Spec.Template.ObjectMeta.Labels
	for k, v := range labels {
		(*l)[k] = v
	}

	// copy all of the annotations to the pod including poddefault related labels
	a := &deployment.Spec.Template.ObjectMeta.Annotations
	for k, v := range annotations {
		(*a)[k] = v
	}

	// Check container
	if len(spec.Containers) == 0 {
		return nil, fmt.Errorf("Service deployment has no container in Spec %q", &spec)
	}
	container := &spec.Containers[0]

	// check that the container has the ports
	missingPorts := []int32{}
	for _, sp := range ports {

		hasPort := false

		for _, cp := range container.Ports {
			if cp.ContainerPort == sp {
				hasPort = true
				break
			}
		}

		if hasPort {
			continue
		} else {
			missingPorts = append(missingPorts, sp)
		}

	}

	if len(missingPorts) > 0 {
		cports := []corev1.ContainerPort{}

		if container.Ports != nil {
			cports = container.Ports
		}

		for _, mp := range ports {
			cports = append(cports, corev1.ContainerPort{
				ContainerPort: mp,
				Protocol:      "TCP",
			})
		}

		container.Ports = cports
	}

	return deployment, nil
}
