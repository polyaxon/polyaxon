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

	"github.com/go-logr/logr"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
	"github.com/polyaxon/polyaxon-operator/controllers/utils"

	mpijobv1 "github.com/kubeflow/mpi-operator/pkg/apis/kubeflow/v1alpha2"
	pytorchjobv1 "github.com/kubeflow/pytorch-operator/pkg/apis/pytorch/v1"
	tfjobv1 "github.com/kubeflow/tf-operator/pkg/apis/tensorflow/v1"
)

// PolyaxonKFReconciler reconciles a PolyaxonKF object
type PolyaxonKFReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonkfs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonkfs/status,verbs=get;update;patch

// Reconcile logic for PolyaxonKFReconciler
func (r *PolyaxonKFReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("polyaxonkf", req.NamespacedName)

	// Load the instance by name
	instance := &corev1alpha1.PolyaxonKF{}
	if err := r.Get(ctx, req.NamespacedName, instance); err != nil {
		log.V(1).Info("unable to fetch PolyaxonKF", "err", err)
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

	// Reconcile the underlaying KubeFlow entity
	if err := r.reconcileKF(instance); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

func (r *PolyaxonKFReconciler) reconcileKF(instance *corev1alpha1.PolyaxonKF) error {
	// Check if the Job already exists
	_ = &mpijobv1.MPIJob{}
	_ = &pytorchjobv1.PyTorchJob{}
	_ = &tfjobv1.TFJob{}
	return nil
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonKFReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonKF{}).
		Complete(r)
}
