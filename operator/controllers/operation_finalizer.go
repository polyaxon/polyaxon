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

package controllers

import (
	"context"

	corev1 "k8s.io/api/core/v1"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

// AddLogsFinalizer Adds finalizer by the reconciler
func (r *OperationReconciler) AddLogsFinalizer(ctx context.Context, instance *operationv1.Operation) error {
	instance.AddLogsFinalizer()
	return r.Update(ctx, instance)
}

// AddNotificationsFinalizer Adds finalizer by the reconciler
func (r *OperationReconciler) AddNotificationsFinalizer(ctx context.Context, instance *operationv1.Operation) error {
	instance.AddNotificationsFinalizer()
	return r.Update(ctx, instance)
}

func (r *OperationReconciler) handleFinalizers(ctx context.Context, instance *operationv1.Operation) error {
	log := r.Log

	if !instance.IsDone() {
		log.Info("Instance was probably stopped", "Append final status", "Stopping")
		r.syncStatus(
			instance,
			operationv1.NewOperationCondition(
				operationv1.OperationStopped,
				corev1.ConditionTrue,
				"OperationStopped",
				"Job stopped in finalizer",
			),
		)
	}

	if instance.HasLogsFinalizer() {
		if err := r.collectLogs(instance); err != nil {
			log.Info("Error logs collection", "Error", err.Error)
			// TODO: add better error handling
			return nil
		}

		instance.RemoveLogsFinalizer()
		return r.Update(ctx, instance)
	}

	if instance.HasNotificationsFinalizer() {
		if err := r.notify(instance); err != nil {
			log.Info("Error notification", "Error", err.Error)
			// TODO: add better error handling
			return nil
		}

		instance.RemoveNotificationsFinalizer()
		return r.Update(ctx, instance)
	}

	return nil
}
