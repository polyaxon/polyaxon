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

func (r *OperationReconciler) reconcileVirtualService(ctx context.Context, instance *operationv1.Operation) error {
	log := r.Log

	virtualservice, err := managers.GenerateVirtualService(instance.Name, instance.Namespace)
	if err != nil {
		log.V(1).Info("generateVirtualService Error")
		return err
	}
	if err := ctrl.SetControllerReference(instance, virtualservice, r.Scheme); err != nil {
		log.V(1).Info("SetControllerReference Error")
		return err
	}

	// Check if the Service already exists
	foundVirtualService := &unstructured.Unstructured{}
	foundVirtualService.SetAPIVersion(kinds.IstioAPIVersion)
	foundVirtualService.SetKind(kinds.IstioVirtualServiceKind)
	justCreated := false
	err = r.Get(ctx, types.NamespacedName{Name: instance.Name, Namespace: instance.Namespace}, foundVirtualService)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}
		log.V(1).Info("Creating Virtual Service", "namespace", instance.Namespace, "name", instance.Name)
		err = r.Create(ctx, virtualservice)
		if err != nil {
			if updated := instance.LogWarning("Error creating VirtualService", err.Error()); updated {
				log.V(1).Info("Warning unable to create VirtualService")
				if statusErr := r.Status().Update(ctx, instance); statusErr != nil {
					return statusErr
				}
				r.instanceSyncStatus(instance)
			}
			return err
		}
		justCreated = true
	} else if err != nil {
		return err
	}

	// Update the servuce object and write the result back if there are any changes
	if !justCreated && managers.CopyVirtualService(virtualservice, foundVirtualService) {
		log.V(1).Info("Updating virtual service\n", "namespace", instance.Namespace, "name", instance.Name)
		err = r.Update(ctx, foundVirtualService)
		if err != nil {
			return err
		}
	}

	return nil
}
