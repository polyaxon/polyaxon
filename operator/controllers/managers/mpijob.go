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

// CopyMPIJobFields copies the owned fields from one MPIJob to another
// Returns true if the fields copied from don't match to.
func CopyMPIJobFields(from, to *unstructured.Unstructured) bool {
	return CopyUnstructuredSpec(from, to, []string{"labels", "spec"})
}

// GenerateMPIJob returns a MPIJob
func GenerateMPIJob(
	name string,
	namespace string,
	labels map[string]string,
	termination operationv1.TerminationSpec,
	spec operationv1.MPIJobSpec,
) (*unstructured.Unstructured, error) {
	replicaSpecs := map[operationv1.MPIReplicaType]*operationv1.KFReplicaSpec{}
	for k, v := range spec.ReplicaSpecs {
		replicaSpecs[operationv1.MPIReplicaType(k)] = generateKFReplica(v)
	}

	// copy all of the labels to the pod including pod default related labels
	for _, replicaSpec := range replicaSpecs {
		l := &replicaSpec.Template.ObjectMeta.Labels
		for k, v := range labels {
			(*l)[k] = v
		}
	}

	mpiJobSpec := &kfapi.MPIJobSpec{
		ActiveDeadlineSeconds: termination.ActiveDeadlineSeconds,
		BackoffLimit:          termination.BackoffLimit,
		SlotsPerWorker:        spec.SlotsPerWorker,
		CleanPodPolicy:        spec.CleanPodPolicy,
		MPIReplicaSpecs:       replicaSpecs,
	}

	mpiJob := &unstructured.Unstructured{}
	mpiJob.SetAPIVersion(kinds.MPIJobAPIVersion)
	mpiJob.SetKind(kinds.MPIJobKind)
	mpiJob.SetLabels(labels)
	mpiJob.SetName(name)
	mpiJob.SetNamespace(namespace)

	mpiJobManifest, err := runtime.DefaultUnstructuredConverter.ToUnstructured(mpiJobSpec)

	if err != nil {
		return nil, fmt.Errorf("Convert mpijob to unstructured error: %v", err)
	}

	if err := unstructured.SetNestedField(mpiJob.Object, mpiJobManifest, "spec"); err != nil {
		return nil, fmt.Errorf("Set .spec.hosts error: %v", err)
	}

	return mpiJob, nil
}
