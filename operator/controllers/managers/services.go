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
	"reflect"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/intstr"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/config"
)

const (
	// DefaultServicePort for service
	DefaultServicePort = 6006
	// DefaultServingPort for service
	DefaultServingPort = 80
	// DefaultServiceReplicas for deployment
	DefaultServiceReplicas = 1
)

// GetReplicas Get replicas for ServiceSpec
func GetReplicas(dreplicas int, service operationv1.ServiceSpec) int32 {
	replicas := int32(dreplicas)
	if service.Replicas != nil {
		replicas = *service.Replicas
	}
	return replicas
}

// CopyServiceFields copies the owned fields from one Service to another
func CopyServiceFields(from, to *corev1.Service) bool {
	requireUpdate := false
	for k, v := range to.Labels {
		if from.Labels[k] != v {
			requireUpdate = true
		}
	}
	to.Labels = from.Labels

	for k, v := range to.Annotations {
		if from.Annotations[k] != v {
			requireUpdate = true
		}
	}
	to.Annotations = from.Annotations

	// Don't copy the entire Spec, because we can't overwrite the clusterIp field

	if !reflect.DeepEqual(to.Spec.Selector, from.Spec.Selector) {
		requireUpdate = true
	}
	to.Spec.Selector = from.Spec.Selector

	if !reflect.DeepEqual(to.Spec.Ports, from.Spec.Ports) {
		requireUpdate = true
	}
	to.Spec.Ports = from.Spec.Ports

	return requireUpdate
}

// GenerateService returns a service given info from a ServiceSpec
func GenerateService(name string, namespace string, labels map[string]string, annotations map[string]string, ports []int32) *corev1.Service {
	sports := []corev1.ServicePort{}

	for _, sp := range ports {
		sports = append(sports, corev1.ServicePort{
			Name:       name,
			Port:       int32(config.GetIntEnv(config.ProxyServicesPort, DefaultServingPort)),
			TargetPort: intstr.FromInt(int(sp)),
			Protocol:   "TCP",
		})
	}

	svc := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:        name,
			Namespace:   namespace,
			Labels:      labels,
			Annotations: annotations,
		},
		Spec: corev1.ServiceSpec{
			Type:     "ClusterIP",
			Selector: labels,
			Ports:    sports,
		},
	}
	return svc
}
