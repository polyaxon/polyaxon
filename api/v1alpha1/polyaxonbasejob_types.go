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
	batchv1 "k8s.io/api/batch/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// TODO: (Mourad) integerate this it when https://github.com/kubernetes/kubernetes/issues/28486 has been fixed
// Optional number of failed pods to retain. This will be especially good for when restart is True since the underlaying pods will disapear.

// PolyaxonBaseJobSpec defines the desired state of PolyaxonPod
type PolyaxonBaseJobSpec struct {
	// Specifies the number of retries before marking this job failed.
	// +optional
	MaxRetries *int32 `json:"maxRetries,omitempty" protobuf:"varint,1,opt,name=replicas"`
	// Template describes the pods that will be created.
	Template corev1.PodTemplateSpec `json:"template" protobuf:"bytes,3,opt,name=template"`
}

// PolyaxonBaseJobStatus defines the observed state of PolyaxonBaseJob
type PolyaxonBaseJobStatus struct {
	// The latest available observations of an object's current state.
	// +optional
	// +patchMergeKey=type
	// +patchStrategy=merge
	Conditions []PolyaxonBaseJobCondition `json:"conditions,omitempty" patchStrategy:"merge" patchMergeKey:"type" protobuf:"bytes,1,rep,name=conditions"`

	// JobCondition is the state of underlying job.
	// +optional
	JobCondition batchv1.JobCondition `json:"deploymentCondition,omitempty"`
}

// PolyaxonBaseJobCondition defines the conditions of PolyaxonBaseJobStatus
type PolyaxonBaseJobCondition struct {
	// Type is the type of the condition. Possible values are Running|Warning|Terminated|Succeeded|Failed
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
