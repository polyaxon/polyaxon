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
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrs "k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	"github.com/go-logr/logr"
	corev1alpha1 "github.com/polyaxon/polyaxon/operator/api/v1alpha1"
	"github.com/polyaxon/polyaxon/operator/controllers/utils"

	openapiRuntime "github.com/go-openapi/runtime"
	polyaxonSDK "github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_client"
)

const (
	// DefaultTensorboardPort for tensorboards
	DefaultTensorboardPort = 6006
	// DefaultTensorboardReplicas for tensorboard deployment
	DefaultTensorboardReplicas = 1
)

// PolyaxonTensorboardReconciler reconciles a PolyaxonTensorboard object
type PolyaxonTensorboardReconciler struct {
	client.Client
	Log       logr.Logger
	Scheme    *runtime.Scheme
	PlxClient *polyaxonSDK.PolyaxonSdk
	PlxToken  openapiRuntime.ClientAuthInfoWriter
}

// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxontensorboards,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxontensorboards/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=services/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments/status,verbs=get;update;patch

// Reconcile logic for PolyaxonTensorboard
func (r *PolyaxonTensorboardReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("polyaxontensorboard", req.NamespacedName)

	// Load the PolyaxonTensorboard by name
	instance := &corev1alpha1.PolyaxonTensorboard{}
	if err := r.Get(ctx, req.NamespacedName, instance); err != nil {
		log.V(1).Info("unable to fetch PolyaxonTensorboard", "err", err)
		return ctrl.Result{}, utils.IgnoreNotFound(err)
	}

	// Finalizer
	if instance.IsBeingDeleted() {
		if err := r.handleFinalizer(instance); err != nil {
			return ctrl.Result{}, err
		}
	} else if !instance.HasFinalizer() {
		if err := r.addFinalizer(instance); err != nil {
			return ctrl.Result{}, err
		}
	}

	// Reconcile the underlaying deployment
	if err := r.reconcileDeployment(instance); err != nil {
		return ctrl.Result{}, err
	}

	// Reconcile the underlaying service
	if err := r.reconcileservice(instance); err != nil {
		return ctrl.Result{}, err
	}

	if instance.HasWarning() { // TODO: (mourad) Add should stop implementation
		log.V(1).Info("Tensorboard has warning", "Reschdule check in", 30)
		return ctrl.Result{Requeue: true, RequeueAfter: time.Second * time.Duration(30)}, nil
	}

	return ctrl.Result{}, nil
}

func (r *PolyaxonTensorboardReconciler) reconcileDeployment(instance *corev1alpha1.PolyaxonTensorboard) error {
	log := r.Log
	ctx := context.Background()

	replicas := utils.GetReplicas(DefaultTensorboardReplicas, instance.Spec)
	plxDeployment, err := utils.GeneratePlxDeployment(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		DefaultTensorboardPort,
		replicas,
		instance.Spec.Template.Spec,
	)
	if err != nil {
		return err
	}
	log.V(1).Info("SetControllerReference")
	if err := ctrl.SetControllerReference(instance, plxDeployment, r.Scheme); err != nil {
		return err
	}
	// Check if the Deployment already exists
	foundDeployment := &appsv1.Deployment{}
	justCreated := false
	log.V(1).Info("Get Tensorboard deployment")
	err = r.Get(ctx, types.NamespacedName{Name: plxDeployment.Name, Namespace: plxDeployment.Namespace}, foundDeployment)
	if instance.IsDone() {
		return nil
	}
	if err != nil && apierrs.IsNotFound(err) {
		log.V(1).Info("Creating Tensorboard Deployment", "namespace", plxDeployment.Namespace, "name", plxDeployment.Name)
		err = r.Create(ctx, plxDeployment)
		if err != nil {
			return err
		}
		justCreated = true
		instance.LogStarting()
	} else if err != nil {
		return err
	}
	// Update the deployment object and write the result back if there are any changes
	if !justCreated && utils.CopyDeploymentFields(plxDeployment, foundDeployment) {
		log.V(1).Info("Updating Tensorboard Deployment", "namespace", plxDeployment.Namespace, "name", plxDeployment.Name)
		err = r.Update(ctx, foundDeployment)
		if err != nil {
			return err
		}
	}

	// Update the readyReplicas if the status is changed
	if foundDeployment.Status.ReadyReplicas != instance.Status.ReadyReplicas {
		log.V(1).Info("Updating Tensorboard Status", "namespace", instance.Namespace, "name", instance.Name)
		instance.Status.ReadyReplicas = foundDeployment.Status.ReadyReplicas
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
	}

	// Check the deployment status
	if condUpdated := r.reconcileDeploymentStatus(instance, *foundDeployment); condUpdated {
		log.V(1).Info("Reconciling Tensorboard Job status", "namespace", plxDeployment.Namespace, "name", plxDeployment.Name)
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
	}

	return nil
}

func (r *PolyaxonTensorboardReconciler) reconcileDeploymentStatus(instance *corev1alpha1.PolyaxonTensorboard, deployment appsv1.Deployment) bool {
	log := r.Log

	if len(deployment.Status.Conditions) == 0 {
		return false
	}

	newDeploymentCond := deployment.Status.Conditions[len(deployment.Status.Conditions)-1]

	if utils.IsPlxDeploymentWarning(deployment.Status, newDeploymentCond) {
		instance.LogWarning(newDeploymentCond.Reason, newDeploymentCond.Message)
		log.V(1).Info("Tensorboard Logging Status Warning")
		return true
	}

	if utils.IsPlxDeploymentRunning(deployment.Status, newDeploymentCond) {
		instance.LogRunning()
		log.V(1).Info("Tensorboard Logging Status Running")
		return true
	}
	return false
}

func (r *PolyaxonTensorboardReconciler) reconcileservice(instance *corev1alpha1.PolyaxonTensorboard) error {
	log := r.Log
	ctx := context.Background()

	port := utils.GetPodPort(instance.Spec.Template.Spec, DefaultTensorboardPort)
	plxService := utils.GeneratePlxService(instance.Name, instance.Namespace, instance.Labels, port)
	if err := ctrl.SetControllerReference(instance, plxService, r.Scheme); err != nil {
		log.V(1).Info("generateService Error")
		return err
	}
	// Check if the Service already exists
	foundService := &corev1.Service{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: plxService.Name, Namespace: plxService.Namespace}, foundService)
	if err != nil && apierrs.IsNotFound(err) {
		log.V(1).Info("Creating Service", "namespace", plxService.Namespace, "name", plxService.Name)
		err = r.Create(ctx, plxService)
		justCreated = true
		if err != nil {
			return err
		}
	} else if err != nil {
		return err
	}
	// Update the foundService object and write the result back if there are any changes
	if !justCreated && utils.CopyServiceFields(plxService, foundService) {
		log.V(1).Info("Updating Service\n", "namespace", plxService.Namespace, "name", plxService.Name)
		err = r.Update(ctx, foundService)
		if err != nil {
			return err
		}
	}

	return nil
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonTensorboardReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonTensorboard{}).
		Owns(&appsv1.Deployment{}).
		Owns(&corev1.Service{}).
		Complete(r)
}
