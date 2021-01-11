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

	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/kfapi"
	"github.com/polyaxon/polyaxon/operator/controllers/kinds"
)

// CopyTFJobFields copies the owned fields from one TFJob to another
// Returns true if the fields copied from don't match to.
func CopyTFJobFields(from, to *unstructured.Unstructured) bool {
	return CopyUnstructuredSpec(from, to, []string{"labels", "spec"})
}

// GenerateTFJob returns a TFJob
func GenerateTFJob(
	name string,
	namespace string,
	labels map[string]string,
	termination operationv1.TerminationSpec,
	spec operationv1.TFJobSpec,
) (*unstructured.Unstructured, error) {
	replicaSpecs := map[operationv1.TFReplicaType]*operationv1.KFReplicaSpec{}
	for k, v := range spec.ReplicaSpecs {
		replicaSpecs[operationv1.TFReplicaType(k)] = generateKFReplica(v)
	}

	// copy all of the labels to the pod including pod default related labels
	for _, replicaSpec := range replicaSpecs {
		l := &replicaSpec.Template.ObjectMeta.Labels
		for k, v := range labels {
			(*l)[k] = v
		}
	}

	tfJobSpec := &kfapi.TFJobSpec{
		ActiveDeadlineSeconds:   termination.ActiveDeadlineSeconds,
		BackoffLimit:            termination.BackoffLimit,
		TTLSecondsAfterFinished: termination.TTLSecondsAfterFinished,
		CleanPodPolicy:          spec.CleanPodPolicy,
		TFReplicaSpecs:          replicaSpecs,
	}

	tfJob := &unstructured.Unstructured{}
	tfJob.SetAPIVersion(kinds.TFJobAPIVersion)
	tfJob.SetKind(kinds.TFJobKind)
	tfJob.SetLabels(labels)
	tfJob.SetName(name)
	tfJob.SetNamespace(namespace)

	tfJobManifest, err := runtime.DefaultUnstructuredConverter.ToUnstructured(tfJobSpec)

	if err != nil {
		return nil, fmt.Errorf("Convert tfjob to unstructured error: %v", err)
	}

	if err := unstructured.SetNestedField(tfJob.Object, tfJobManifest, "spec"); err != nil {
		return nil, fmt.Errorf("Set .spec.hosts error: %v", err)
	}

	return tfJob, nil
}
