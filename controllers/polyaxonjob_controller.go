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
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
	"github.com/polyaxon/polyaxon-operator/controllers/utils"
)

// PolyaxonJobReconciler reconciles a PolyaxonJob object
type PolyaxonJobReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
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

func (r *PolyaxonJobReconciler) reconcileJob(instance *corev1alpha1.PolyaxonJob) error {
	log := r.Log
	ctx := context.Background()

	plxJob := utils.GeneratePlxJob(
		instance.Name,
		instance.Namespace,
		instance.Labels,
		instance.Spec.MaxRetries,
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
		log.V(1).Info("Creating Job", "namespace", plxJob.Namespace, "name", plxJob.Name)
		err = r.Create(ctx, plxJob)
		justCreated = true
		if err != nil {
			return err
		}
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
	if len(foundJob.Status.Conditions) > 0 &&
		foundJob.Status.Conditions[0] != instance.Status.JobCondition {
		log.V(1).Info("Updating container state: ", "namespace", instance.Namespace, "name", instance.Name)
		jobCond := foundJob.Status.Conditions[0]
		instance.Status.JobCondition = jobCond
		oldConditions := instance.Status.Conditions
		newCondition := utils.GetPlxJobCondition(jobCond)
		// Append new condition
		if len(oldConditions) == 0 || oldConditions[0].Type != newCondition.Type ||
			oldConditions[0].Reason != newCondition.Reason ||
			oldConditions[0].Message != newCondition.Message {
			log.V(1).Info("Appending to conditions: ", "namespace", instance.Namespace, "name", instance.Name, "type", newCondition.Type, "reason", newCondition.Reason, "message", newCondition.Message)
			instance.Status.Conditions = append([]corev1alpha1.PolyaxonBaseJobCondition{newCondition}, oldConditions...)
		}
		err = r.Status().Update(context.Background(), instance)
		if err != nil {
			return err
		}
	}

	return nil
}

// SetupWithManager register the reconciliation logic
func (r *PolyaxonJobReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&corev1alpha1.PolyaxonJob{}).
		Owns(&batchv1.Job{}).
		Complete(r)
}
