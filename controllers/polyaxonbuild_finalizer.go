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

package controllers

import (
	"context"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
)

func (r *PolyaxonBuildReconciler) addFinalizer(instance *corev1alpha1.PolyaxonBuild) error {
	instance.AddFinalizer()
	return r.Update(context.Background(), instance)
}

func (r *PolyaxonBuildReconciler) handleFinalizer(instance *corev1alpha1.PolyaxonBuild) error {
	if !instance.HasFinalizer() {
		return nil
	}

	if err := r.setStatus(instance); err != nil {
		return err
	}
	instance.RemoveFinalizer()
	return r.Update(context.Background(), instance)
}

func (r *PolyaxonBuildReconciler) setStatus(instance *corev1alpha1.PolyaxonBuild) error {
	log := r.Log

	log.Info("Build end", "Reconciliation", instance.GetName())

	// Add logic to send status update to experiment based on the rel_url metadata
	// rel_url := instance.Status.Metadata.owner/project/experimentId
	// if it fails just let it be
	// return r.APIClient.Experiments().setStatus(owner, project, experimentId
	return nil
}
