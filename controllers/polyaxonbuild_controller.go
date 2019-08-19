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
	batchv1 "k8s.io/api/batch/v1"
	apierrs "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
	"github.com/polyaxon/polyaxon-operator/controllers/utils"

	openapiRuntime "github.com/go-openapi/runtime"
	polyaxonSDK "github.com/polyaxon/polyaxon-sdks/go/http_client/v1/service_client"
)

// PolyaxonBuildReconciler reconciles a PolyaxonBuild object
type PolyaxonBuildReconciler struct {
	client.Client
	Log       logr.Logger
	Scheme    *runtime.Scheme
	PlxClient *polyaxonSDK.PolyaxonSdk
	PlxToken  openapiRuntime.ClientAuthInfoWriter
}

// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonbuilds,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonbuilds/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=batch,resources=jobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=batch,resources=jobs/status,verbs=get;update;patch

// Reconcile logic for PolyaxonBuildReconciler
func (r *PolyaxonBuildReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("polyaxonbuild", req.NamespacedName)

	// Load the instance by name
	instance := &corev1alpha1.PolyaxonBuild{}
	if err := r.Get(ctx, req.NamespacedName, instance); err != nil {
		log.V(1).Info("unable to fetch PolyaxonBuild", "err", err)
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

	// Reconcile the underlaying job
	if err := r.reconcileJob(instance); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

func (r *PolyaxonBuildReconciler) reconcileJob(instance *corev1alpha1.PolyaxonBuild) error {
	log := r.Log
	ctx := context.Background()

	plxJob := utils.GeneratePlxJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec.BackoffLimit,
		instance.Spec.Template.Spec,
	)
	if err := ctrl.SetControllerReference(instance, plxJob, r.Scheme); err != nil {
		log.V(1).Info("generatePlxJob Error", "plxJob", plxJob)
		return err
	}
	// Check if the Job already exists
	foundJob := &batchv1.Job{}
	justCreated := false
	err := r.Get(ctx, types.NamespacedName{Name: plxJob.Name, Namespace: plxJob.Namespace}, foundJob)
	if err != nil && apierrs.IsNotFound(err) {
		if instance.IsDone() {
			return nil
		}

		log.V(1).Info("Creating Build Job", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Create(ctx, plxJob)
		if err != nil {
			return err
		}
		justCreated = true
		instance.LogStarting()
	} else if err != nil {
		return err
	}
	// Update the job object and write the result back if there are any changes
	if !justCreated && utils.CopyJobFields(plxJob, foundJob) {
		log.V(1).Info("Updating Build Job", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	if condUpdated := r.reconcileJobStatus(instance, *foundJob); condUpdated {
		log.V(1).Info("Reconciling Build Job status", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
	}

	return nil
}

func (r *PolyaxonBuildReconciler) reconcileJobStatus(instance *corev1alpha1.PolyaxonBuild, job batchv1.Job) bool {
	now := metav1.Now()
	log := r.Log

	if len(job.Status.Conditions) == 0 {
		if job.Status.Failed > 0 {
			instance.LogWarning("", "")
			log.V(1).Info("Build Logging Status Warning")
			return true
		} else if job.Status.Active > 0 {
			instance.LogRunning()
			log.V(1).Info("Build Logging Status Running")
			return true
		}
		return false
	}

	newJobCond := job.Status.Conditions[len(job.Status.Conditions)-1]

	if job.Status.Active == 0 && job.Status.Succeeded > 0 && utils.IsPlxJobSucceded(newJobCond) {
		instance.LogSucceeded()
		instance.Status.CompletionTime = &now
		log.V(1).Info("Build Logging Status Succeeded")
		return true
	}

	if job.Status.Failed > 0 && utils.IsPlxJobFailed(newJobCond) {
		instance.LogFailed(newJobCond.Reason, newJobCond.Message)
		instance.Status.CompletionTime = &now
		log.V(1).Info("Build Logging Status Failed")
		return true
	}
	return false
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonBuildReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonBuild{}).
		Owns(&batchv1.Job{}).
		Complete(r)
}
