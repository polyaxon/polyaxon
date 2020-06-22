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

	"github.com/go-logr/logr"
	appsv1 "k8s.io/api/apps/v1"
	batchv1 "k8s.io/api/batch/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/config"
	"github.com/polyaxon/polyaxon/operator/controllers/kinds"
	"github.com/polyaxon/polyaxon/operator/controllers/utils"
)

// OperationReconciler reconciles a Operation object
type OperationReconciler struct {
	client.Client
	Log       logr.Logger
	Scheme    *runtime.Scheme
	Namespace string
}

// +kubebuilder:rbac:groups=core.polyaxon.com,resources=operations,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core.polyaxon.com,resources=operations/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=batch,resources=jobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=batch,resources=jobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=services/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=kubeflow.org,resources=tfjobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=kubeflow.org,resources=tfjobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=kubeflow.org,resources=pytorchjobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=kubeflow.org,resources=pytorchjobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=kubeflow.org,resources=mpijobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=kubeflow.org,resources=mpijobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=networking.istio.io,resources=virtualservices,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=networking.istio.io,resources=virtualservices/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=networking.istio.io,resources=destinationrules,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=networking.istio.io,resources=destinationrules/status,verbs=get;update;patch

// Reconcile logic for OperationReconciler
func (r *OperationReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("operator", req.NamespacedName)

	// Load the instance by name
	instance := &operationv1.Operation{}
	if err := r.Get(ctx, req.NamespacedName, instance); err != nil {
		log.V(1).Info("unable to fetch Operation", "err", err)
		return ctrl.Result{}, utils.IgnoreNotFound(err)
	}

	// Finalizer
	if instance.IsBeingDeleted() {
		return ctrl.Result{}, r.handleFinalizers(ctx, instance)
	} else if !instance.HasLogsFinalizer() {
		if err := r.AddLogsFinalizer(ctx, instance); err != nil {
			return ctrl.Result{}, err
		}
	} else if !instance.HasNotificationsFinalizer() {
		if err := r.AddNotificationsFinalizer(ctx, instance); err != nil {
			return ctrl.Result{}, err
		}
	} else if instance.IsDone() {
		return r.cleanUpOperation(ctx, instance)
	}

	// Reconcile the underlaying runtime
	return r.reconcileOperation(ctx, instance)
}

func (r *OperationReconciler) reconcileOperation(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	if instance.BatchJobSpec != nil {
		return r.reconcileJobOp(ctx, instance)
	} else if instance.ServiceSpec != nil {
		return r.reconcileServiceOp(ctx, instance)
	} else if instance.TFJobSpec != nil {
		return r.reconcileTFJobOp(ctx, instance)
	} else if instance.PytorchJobSpec != nil {
		return r.reconcilePytorchJobOp(ctx, instance)
	} else if instance.MPIJobSpec != nil {
		return r.reconcileMPIJobOp(ctx, instance)
	}
	return ctrl.Result{}, nil
}

func (r *OperationReconciler) cleanUpOperation(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	if instance.BatchJobSpec != nil {
		return r.cleanUpJob(ctx, instance)
	} else if instance.ServiceSpec != nil {
		return r.cleanUpService(ctx, instance)
	} else if instance.TFJobSpec != nil {
		return r.cleanUpTFJob(ctx, instance)
	} else if instance.PytorchJobSpec != nil {
		return r.cleanUpPytorchJob(ctx, instance)
	} else if instance.MPIJobSpec != nil {
		return r.cleanUpMPIJob(ctx, instance)
	}
	return ctrl.Result{}, nil
}

// SetupWithManager register the reconciliation logic
func (r *OperationReconciler) SetupWithManager(mgr ctrl.Manager) error {
	controllerManager := ctrl.NewControllerManagedBy(mgr).For(&operationv1.Operation{})
	controllerManager.Owns(&batchv1.Job{})
	controllerManager.Owns(&appsv1.Deployment{})
	controllerManager.Owns(&corev1.Service{})

	if config.GetBoolEnv(config.TFJobEnabled, false) {
		tfJob := &unstructured.Unstructured{}
		tfJob.SetAPIVersion(kinds.TFJobAPIVersion)
		tfJob.SetKind(kinds.TFJobKind)
		controllerManager.Owns(tfJob)
	}
	if config.GetBoolEnv(config.PytorchJobEnabled, false) {
		pytorchJob := &unstructured.Unstructured{}
		pytorchJob.SetAPIVersion(kinds.PytorchJobAPIVersion)
		pytorchJob.SetKind(kinds.PytorchJobKind)
		controllerManager.Owns(pytorchJob)
	}
	if config.GetBoolEnv(config.MPIJobEnabled, false) {
		mpiJob := &unstructured.Unstructured{}
		mpiJob.SetAPIVersion(kinds.MPIJobAPIVersion)
		mpiJob.SetKind(kinds.MPIJobKind)
		controllerManager.Owns(mpiJob)
	}
	if config.GetBoolEnv(config.IstioEnabled, false) {
		istioVirtualService := &unstructured.Unstructured{}
		istioVirtualService.SetAPIVersion(kinds.IstioAPIVersion)
		istioVirtualService.SetKind(kinds.IstioVirtualServiceKind)
		controllerManager.Owns(istioVirtualService)
	}
	if config.GetBoolEnv(config.SparkJobEnabled, false) {
		sparkJob := &unstructured.Unstructured{}
		sparkJob.SetAPIVersion(kinds.SparkAPIVersion)
		sparkJob.SetKind(kinds.SparkApplicationKind)
		controllerManager.Owns(sparkJob)
	}
	return controllerManager.Complete(r)
}
