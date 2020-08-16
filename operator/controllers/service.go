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
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrs "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/managers"
)

// Reconcile logic for Operation
func (r *OperationReconciler) reconcileServiceOp(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	log := r.Log

	ports := managers.GetPodPorts(instance.ServiceSpec.Template.Spec, managers.DefaultServicePort)
	if instance.ServiceSpec.Ports != nil {
		ports = instance.ServiceSpec.Ports
	}

	// Reconcile the underlaying deployment
	if err := r.reconcileDeployment(ctx, instance, ports); err != nil {
		return ctrl.Result{}, err
	}

	// Reconcile the underlaying service
	if err := r.reconcileBaseService(ctx, instance, ports); err != nil {
		return ctrl.Result{}, err
	}

	if duration, err := r.handlePastActiveDeadline(ctx, instance); err != nil || duration != nil {
		if err != nil {
			return ctrl.Result{}, err
		}
		return ctrl.Result{Requeue: true, RequeueAfter: *duration}, nil
	}

	if instance.HasWarning() {
		if err := r.handleServiceBackoffLimit(ctx, instance); err != nil {
			return ctrl.Result{}, err
		}
		log.V(1).Info("service has warning", "Reschdule check in", 30)
		return ctrl.Result{Requeue: true, RequeueAfter: time.Second * time.Duration(30)}, nil
	}

	return ctrl.Result{}, nil
}

func (r *OperationReconciler) reconcileDeployment(ctx context.Context, instance *operationv1.Operation, ports []int32) error {
	log := r.Log

	replicas := managers.GetReplicas(managers.DefaultServiceReplicas, *instance.ServiceSpec)
	deployment, err := managers.GenerateDeployment(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		ports,
		replicas,
		instance.ServiceSpec.Template.Spec,
	)
	if err != nil {
		return err
	}
	log.V(1).Info("SetControllerReference")
	if err := ctrl.SetControllerReference(instance, deployment, r.Scheme); err != nil {
		return err
	}
	// Check if the Deployment already exists
	foundDeployment := &appsv1.Deployment{}
	justCreated := false
	log.V(1).Info("Get Service deployment")
	err = r.Get(ctx, types.NamespacedName{Name: deployment.Name, Namespace: deployment.Namespace}, foundDeployment)
	if instance.IsDone() {
		return nil
	}
	if err != nil && apierrs.IsNotFound(err) {
		log.V(1).Info("Creating Service Deployment", "namespace", deployment.Namespace, "name", deployment.Name)
		err = r.Create(ctx, deployment)
		if err != nil {
			if updated := instance.LogWarning("Error creating Deployment", err.Error()); updated {
				log.V(1).Info("Warning unable to create Deployment")
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
	// Update the deployment object and write the result back if there are any changes
	if !justCreated && managers.CopyDeploymentFields(deployment, foundDeployment) {
		log.V(1).Info("Updating Service Deployment", "namespace", deployment.Namespace, "name", deployment.Name)
		err = r.Update(ctx, foundDeployment)
		if err != nil {
			return err
		}
	}

	// Check the deployment status
	if condUpdated := r.reconcileDeploymentStatus(instance, *foundDeployment); condUpdated {
		log.V(1).Info("Reconciling Service status", "namespace", deployment.Namespace, "name", deployment.Name)
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
		r.instanceSyncStatus(instance)
	}

	return nil
}

func (r *OperationReconciler) reconcileDeploymentStatus(instance *operationv1.Operation, deployment appsv1.Deployment) bool {
	log := r.Log

	if len(deployment.Status.Conditions) == 0 {
		log.V(1).Info("Service No Conditions")
		return false
	}

	newDeploymentCond := deployment.Status.Conditions[len(deployment.Status.Conditions)-1]

	if managers.IsDeploymentWarning(deployment.Status, newDeploymentCond) {
		instance.LogWarning(newDeploymentCond.Reason, newDeploymentCond.Message)
		log.V(1).Info("Service Logging Status Warning")
		return true
	}

	if managers.IsDeploymentRunning(deployment.Status, newDeploymentCond) {
		instance.LogRunning()
		log.V(1).Info("Service Logging Status Running")
		return true
	}
	return false
}

func (r *OperationReconciler) reconcileBaseService(ctx context.Context, instance *operationv1.Operation, ports []int32) error {
	log := r.Log

	service := managers.GenerateService(instance.Name, instance.Namespace, instance.Labels, ports)
	if err := ctrl.SetControllerReference(instance, service, r.Scheme); err != nil {
		log.V(1).Info("generateService Error")
		return err
	}
	// Check if the Service already exists
	foundService := &corev1.Service{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: service.Name, Namespace: service.Namespace}, foundService)
	if err != nil && apierrs.IsNotFound(err) {
		log.V(1).Info("Creating Service", "namespace", service.Namespace, "name", service.Name)
		err = r.Create(ctx, service)
		if err != nil {
			if updated := instance.LogWarning("Error creating Service", err.Error()); updated {
				log.V(1).Info("Warning unable to create Service")
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
	// Update the foundService object and write the result back if there are any changes
	if !justCreated && managers.CopyServiceFields(service, foundService) {
		log.V(1).Info("Updating Service\n", "namespace", service.Namespace, "name", service.Name)
		err = r.Update(ctx, foundService)
		if err != nil {
			return err
		}
	}

	return nil
}

func (r *OperationReconciler) cleanUpService(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	return r.handleTTL(ctx, instance)
}

// handleServiceBackoffLimit checks if service has BackoffLimit and translate it to a warning duration with back-off limit
func (r *OperationReconciler) handleServiceBackoffLimit(ctx context.Context, instance *operationv1.Operation) error {
	log := r.Log

	backoffLimit := instance.Termination.BackoffLimit
	if backoffLimit == nil {
		return nil
	}
	lastTransitionTime := instance.Status.Conditions[len(instance.Status.Conditions)-1].LastTransitionTime
	currentTime := metav1.Now()
	duration := currentTime.Time.Sub(lastTransitionTime.Time)

	if duration >= r.getBackOff(*backoffLimit) {
		log.V(1).Info("Cleanup triggered based on ActiveDeadlineSeconds")
		return r.delete(ctx, instance)
	}

	return nil
}
