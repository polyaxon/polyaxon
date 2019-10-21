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

func (r *PolyaxonJobReconciler) addFinalizer(ctx context.Context, instance *corev1alpha1.PolyaxonJob) error {
	instance.AddFinalizer()
	return r.Update(ctx, instance)
}

func (r *PolyaxonJobReconciler) handleFinalizer(ctx context.Context, instance *corev1alpha1.PolyaxonJob) error {
	if !instance.HasFinalizer() {
		return nil
	}

	if err := r.collectLogs(instance); err != nil {
		return err
	}
	instance.RemoveFinalizer()
	return r.Update(ctx, instance)
}
