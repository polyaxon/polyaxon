/*
Copyright 2018-2020 Polyaxon, Inc.

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

	apierrs "k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/kinds"
	"github.com/polyaxon/polyaxon/operator/controllers/managers"
)

func (r *OperationReconciler) reconcileTFJobOp(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	// Reconcile the underlaying job
	return ctrl.Result{}, r.reconcileTFJob(ctx, instance)
}

func (r *OperationReconciler) reconcileTFJob(ctx context.Context, instance *operationv1.Operation) error {
	log := r.Log

	job, err := managers.GenerateTFJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Termination,
		*instance.TFJobSpec,
	)
	if err != nil {
		log.V(1).Info("GenerateTFJob Error")
		return err
	}

	if err := ctrl.SetControllerReference(instance, job, r.Scheme); err != nil {
		log.V(1).Info("SetControllerReference Error")
		return err
	}

	// Check if the Job already exists
	foundJob := &unstructured.Unstructured{}
	foundJob.SetAPIVersion(kinds.TFJobAPIVersion)
	foundJob.SetKind(kinds.TFJobKind)
	justCreated := false
	err = r.Get(ctx, types.NamespacedName{Name: instance.Name, Namespace: instance.Namespace}, foundJob)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}
		log.V(1).Info("Creating TFJob", "namespace", instance.Namespace, "name", instance.Name)
		err = r.Create(ctx, job)
		if err != nil {
			if updated := instance.LogWarning("Error creating TFJob", err.Error()); updated {
				log.V(1).Info("Warning unable to create TFJob")
				if statusErr := r.Status().Update(ctx, instance); statusErr != nil {
					return statusErr
				}
				r.instanceSyncStatus(instance)
			}
			return err
		}
		justCreated = true
		instance.LogStarting()
		err = r.Status().Update(ctx, instance)
		r.instanceSyncStatus(instance)
	} else if err != nil {
		return err
	}

	// Update the job object and write the result back if there are any changes
	if !justCreated && managers.CopyTFJobFields(job, foundJob) {
		log.V(1).Info("Updating TFJob", "namespace", instance.Namespace, "name", instance.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	condUpdated, err := r.reconcileTFJobStatus(instance, *foundJob)
	if err != nil {
		log.V(1).Info("reconcileTFJobStatus Error")
		return err
	}
	if condUpdated {
		log.V(1).Info("Reconciling Job status", "namespace", instance.Namespace, "name", instance.Name)
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
		r.instanceSyncStatus(instance)
	}

	return nil
}

func (r *OperationReconciler) reconcileTFJobStatus(instance *operationv1.Operation, job unstructured.Unstructured) (bool, error) {
	return r.reconcileKFJobStatus(instance, job)
}

func (r *OperationReconciler) cleanUpTFJob(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	return ctrl.Result{}, nil
}
