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
	apierrs "k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
	"github.com/polyaxon/polyaxon-operator/controllers/kf"
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
	switch instance.Spec.KFKind {
	case corev1alpha1.TFJob:
		return r.reconcileTFJob(instance)
	case corev1alpha1.PyTorchJob:
		return r.reconcilePytorchJob(instance)
	case corev1alpha1.MPIJob:
		return r.reconcileMPIJob(instance)
	}
	return nil
}

func (r *PolyaxonKFReconciler) reconcileTFJob(instance *corev1alpha1.PolyaxonKF) error {
	log := r.Log
	ctx := context.Background()

	plxJob := kf.GenerateTFJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec,
	)
	if err := ctrl.SetControllerReference(instance, plxJob, r.Scheme); err != nil {
		log.V(1).Info("generateTFJob Error")
		return err
	}
	// Check if the Job already exists
	foundJob := &tfjobv1.TFJob{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: plxJob.Name, Namespace: plxJob.Namespace}, foundJob)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}
		err = r.Create(ctx, plxJob)
		justCreated = true
		if err != nil {
			return err
		}
	} else if err != nil {
		return err
	}

	// Update the job object and write the result back if there are any changes
	if !justCreated && kf.CopyTFJobFields(plxJob, foundJob) {
		log.V(1).Info("Updating TFJob", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	// if condUpdated := r.reconcileJobStatus(instance, *foundJob); condUpdated {
	// 	log.V(1).Info("Reconciling Job status", "namespace", plxJob.Namespace, "name", plxJob.Name)
	// 	err = r.Status().Update(ctx, instance)
	// 	if err != nil {
	// 		return err
	// 	}
	// }

	return nil
}

func (r *PolyaxonKFReconciler) reconcilePytorchJob(instance *corev1alpha1.PolyaxonKF) error {
	log := r.Log
	ctx := context.Background()

	plxJob := kf.GeneratePytorchJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec,
	)
	if err := ctrl.SetControllerReference(instance, plxJob, r.Scheme); err != nil {
		log.V(1).Info("generatePytorchJob Error")
		return err
	}
	// Check if the Job already exists
	foundJob := &pytorchjobv1.PyTorchJob{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: plxJob.Name, Namespace: plxJob.Namespace}, foundJob)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}
		err = r.Create(ctx, plxJob)
		justCreated = true
		if err != nil {
			return err
		}
	} else if err != nil {
		return err
	}

	// Update the job object and write the result back if there are any changes
	if !justCreated && kf.CopyPytorchJobFields(plxJob, foundJob) {
		log.V(1).Info("Updating PytorchJob", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	// if condUpdated := r.reconcileJobStatus(instance, *foundJob); condUpdated {
	// 	log.V(1).Info("Reconciling Job status", "namespace", plxJob.Namespace, "name", plxJob.Name)
	// 	err = r.Status().Update(ctx, instance)
	// 	if err != nil {
	// 		return err
	// 	}
	// }

	return nil
}

func (r *PolyaxonKFReconciler) reconcileMPIJob(instance *corev1alpha1.PolyaxonKF) error {
	log := r.Log
	ctx := context.Background()

	plxJob := kf.GenerateMPIJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec,
	)
	if err := ctrl.SetControllerReference(instance, plxJob, r.Scheme); err != nil {
		log.V(1).Info("generateMPIJob Error")
		return err
	}
	// Check if the Job already exists
	foundJob := &mpijobv1.MPIJob{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: plxJob.Name, Namespace: plxJob.Namespace}, foundJob)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}
		err = r.Create(ctx, plxJob)
		justCreated = true
		if err != nil {
			return err
		}
	} else if err != nil {
		return err
	}

	// Update the job object and write the result back if there are any changes
	if !justCreated && kf.CopyMPIJobFields(plxJob, foundJob) {
		log.V(1).Info("Updating MPIJob", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	// if condUpdated := r.reconcileJobStatus(instance, *foundJob); condUpdated {
	// 	log.V(1).Info("Reconciling Job status", "namespace", plxJob.Namespace, "name", plxJob.Name)
	// 	err = r.Status().Update(ctx, instance)
	// 	if err != nil {
	// 		return err
	// 	}
	// }

	return nil
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonKFReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonKF{}).
		Complete(r)
}
