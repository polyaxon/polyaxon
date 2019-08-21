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

// PolyaxonJobReconciler reconciles a PolyaxonJob object
type PolyaxonJobReconciler struct {
	client.Client
	Log       logr.Logger
	Scheme    *runtime.Scheme
	PlxClient *polyaxonSDK.PolyaxonSdk
	PlxToken  openapiRuntime.ClientAuthInfoWriter
}

// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonjobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core.polyaxon.com,resources=polyaxonjobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=batch,resources=jobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=batch,resources=jobs/status,verbs=get;update;patch

// Reconcile logic for PolyaxonJobReconciler
func (r *PolyaxonJobReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("polyaxonjob", req.NamespacedName)

	// Load the instance by name
	instance := &corev1alpha1.PolyaxonJob{}
	if err := r.Get(ctx, req.NamespacedName, instance); err != nil {
		log.V(1).Info("unable to fetch PolyaxonJob", "err", err)
		return ctrl.Result{}, utils.IgnoreNotFound(err)
	}

	// Finalizer
	if instance.IsBeingDeleted() {
		return ctrl.Result{}, r.handleFinalizer(ctx, instance)
	} else if !instance.HasFinalizer() {
		if err := r.addFinalizer(ctx, instance); err != nil {
			return ctrl.Result{}, err
		}
	} else if instance.IsDone() {
		return ctrl.Result{}, r.cleanUp(ctx, instance)
	}

	// Reconcile the underlaying job
	if err := r.reconcileJob(ctx, instance); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

func (r *PolyaxonJobReconciler) reconcileJob(ctx context.Context, instance *corev1alpha1.PolyaxonJob) error {
	log := r.Log

	plxJob := utils.GeneratePlxJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec.BackoffLimit,
		instance.Spec.Template.Spec,
	)
	if err := ctrl.SetControllerReference(instance, plxJob, r.Scheme); err != nil {
		log.V(1).Info("generatePlxJob Error")
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

		log.V(1).Info("Creating Job", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Create(ctx, plxJob)
		if err != nil {
			return err
		}
		justCreated = true
		instance.LogStarting()
		err = r.Status().Update(ctx, instance)
		r.syncStatus(instance)
	} else if err != nil {
		return err
	}
	// Update the job object and write the result back if there are any changes
	if !justCreated && utils.CopyJobFields(plxJob, foundJob) {
		log.V(1).Info("Updating Job", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Update(ctx, foundJob)
		if err != nil {
			return err
		}
	}

	// Check the job status
	if condUpdated := r.reconcileJobStatus(instance, *foundJob); condUpdated {
		log.V(1).Info("Reconciling Job status", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Status().Update(ctx, instance)
		if err != nil {
			return err
		}
		r.syncStatus(instance)
	}

	return nil
}

func (r *PolyaxonJobReconciler) reconcileJobStatus(instance *corev1alpha1.PolyaxonJob, job batchv1.Job) bool {
	now := metav1.Now()
	log := r.Log

	if len(job.Status.Conditions) == 0 {
		if job.Status.Failed > 0 {
			if updated := instance.LogWarning("", ""); updated {
				log.V(1).Info("Build Logging Status Warning")
				return true
			}
		} else if job.Status.Active > 0 {
			if updated := instance.LogRunning(); updated {
				log.V(1).Info("Build Logging Status Running")
				return true
			}
		}
		return false
	}

	newJobCond := job.Status.Conditions[len(job.Status.Conditions)-1]

	if job.Status.Active == 0 && job.Status.Succeeded > 0 && utils.IsPlxJobSucceded(newJobCond) {
		if updated := instance.LogSucceeded(); updated {
			instance.Status.CompletionTime = &now
			log.V(1).Info("Build Logging Status Succeeded")
			return true
		}
	}

	if job.Status.Failed > 0 && utils.IsPlxJobFailed(newJobCond) {
		if updated := instance.LogFailed(newJobCond.Reason, newJobCond.Message); updated {
			instance.Status.CompletionTime = &now
			log.V(1).Info("Build Logging Status Failed")
			return true
		}
	}
	return false
}

func (r *PolyaxonJobReconciler) cleanUp(ctx context.Context, instance *corev1alpha1.PolyaxonJob) error {
	log := r.Log

	// currentTime := metav1.Now()
	// ttl := instance.Spec.TTLSecondsAfterFinished
	// if ttl == nil {
	// 	// do nothing if the cleanup delay is not set
	// 	return nil
	// }
	// duration := time.Second * time.Duration(*ttl)
	// if currentTime.After(instance.Status.CompletionTime.Add(duration)) {
	// 	err := r.Delete(ctx, instance)
	// 	if err != nil {
	// 		log.V(1).Info("Cleanup Build Job", "Error", err)
	// 		return err
	// 	}
	// }
	err := r.Delete(ctx, instance)
	if err != nil {
		log.V(1).Info("Cleanup Job", "Error", err)
		return err
	}
	log.V(1).Info("Job is done, cleanup", "namespace", instance.Namespace, "name", instance.Name)
	return nil
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonJobReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonJob{}).
		Owns(&batchv1.Job{}).
		Complete(r)
}
