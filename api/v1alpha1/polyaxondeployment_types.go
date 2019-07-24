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
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// PolyaxonDeploymentSpec defines the desired state of PolyaxonDeployment
type PolyaxonDeploymentSpec struct {
	// Template describes the pods that will be created.
	Template corev1.PodTemplateSpec `json:"template" protobuf:"bytes,3,opt,name=template"`
	// Replicas is the number of desired replicas.
	// This is a pointer to distinguish between explicit zero and unspecified.
	// Defaults to 1.
	// +optional
	Replicas *int32 `json:"replicas,omitempty" protobuf:"varint,1,opt,name=replicas"`
}

// PolyaxonDeploymentStatus defines the observed state of PolyaxonDeployment
type PolyaxonDeploymentStatus struct {
	// Conditions is an array of current conditions
	Conditions []PolyaxonDeploymentCondition `json:"conditions,omitempty"`
	// ReadyReplicas is the number of Pods created by the StatefulSet controller that have a Ready Condition.
	ReadyReplicas int32 `json:"readyReplicas,omitempty"`
	// DeploymentCondition is the state of underlying deployment.
	DeploymentCondition appsv1.DeploymentCondition `json:"deploymentCondition,omitempty"`
}

// PolyaxonDeploymentCondition defines the conditions of PolyaxonDeploymentStatus
type PolyaxonDeploymentCondition struct {
	// Type is the type of the condition. Possible values are Running|Warning|Terminated
	Type string `json:"type"`
	// Last time we probed the condition.
	// +optional
	LastProbeTime metav1.Time `json:"lastProbeTime,omitempty"`
	// (brief) reason the container is in the current state
	// +optional
	Reason string `json:"reason,omitempty"`
	// Message regarding why the container is in the current state.
	// +optional
	Message string `json:"message,omitempty"`
}
