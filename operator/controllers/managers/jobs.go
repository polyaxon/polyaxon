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

	batchv1 "k8s.io/api/batch/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

const (
	// DefaultBackoffLimit for Jobs
	DefaultBackoffLimit = 0
	// DefaultRestartPolicy for Jobs
	DefaultRestartPolicy = "Never"
)

// CopyJobFields copies the owned fields from one Job to another
// Returns true if the fields copied from don't match to.
func CopyJobFields(from, to *batchv1.Job) bool {
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

	if to.Spec.TTLSecondsAfterFinished != from.Spec.TTLSecondsAfterFinished {
		to.Spec.TTLSecondsAfterFinished = from.Spec.TTLSecondsAfterFinished
		requireUpdate = true
	}

	if !reflect.DeepEqual(to.Spec.Template.Spec, from.Spec.Template.Spec) {
		requireUpdate = true
		to.Spec.Template.Spec = from.Spec.Template.Spec
	}

	return requireUpdate
}

// IsJobSucceeded return true if job is running
func IsJobSucceeded(jc batchv1.JobCondition) bool {
	return jc.Type == batchv1.JobComplete && jc.Status == corev1.ConditionTrue
}

// IsJobFailed return true if job is running
func IsJobFailed(jc batchv1.JobCondition) bool {
	return jc.Type == batchv1.JobFailed && jc.Status == corev1.ConditionTrue
}

// GenerateJob returns a batch job given a OperationSpec
func GenerateJob(
	name string,
	namespace string,
	labels map[string]string,
	annotations map[string]string,
	backoffLimit *int32,
	activeDeadlineSeconds *int64,
	ttlSecondsAfterFinished *int32,
	podSpec corev1.PodSpec,
) *batchv1.Job {
	jobBackoffLimit := backoffLimit
	if backoffLimit == nil {
		defaultBackoffLimit := int32(DefaultBackoffLimit)
		jobBackoffLimit = &defaultBackoffLimit
	}

	if podSpec.RestartPolicy == "" {
		podSpec.RestartPolicy = DefaultRestartPolicy
	}

	job := &batchv1.Job{
		ObjectMeta: metav1.ObjectMeta{
			Name:        name,
			Namespace:   namespace,
			Labels:      labels,
			Annotations: annotations,
		},
		Spec: batchv1.JobSpec{
			BackoffLimit:            jobBackoffLimit,
			ActiveDeadlineSeconds:   activeDeadlineSeconds,
			TTLSecondsAfterFinished: ttlSecondsAfterFinished,
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{Labels: map[string]string{}, Annotations: map[string]string{}},
				Spec:       podSpec,
			},
		},
	}

	// copy all of the labels to the pod including poddefault related labels
	l := &job.Spec.Template.ObjectMeta.Labels
	for k, v := range labels {
		(*l)[k] = v
	}

	// copy all of the annotations to the pod including poddefault related labels
	a := &job.Spec.Template.ObjectMeta.Annotations
	for k, v := range annotations {
		(*a)[k] = v
	}

	return job
}
