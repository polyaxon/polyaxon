/*
Copyright 2018-2021 Polyaxon, Inc.

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
	"math"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	ctrl "sigs.k8s.io/controller-runtime"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

const (
	// DefaultBackOff is the max backoff period, exported for the e2e test
	DefaultBackOff = 10 * time.Second
	// MaxBackOff is the max backoff period, exported for the e2e test
	MaxBackOff = 360 * time.Second
)

// delete the operation
func (r *OperationReconciler) delete(ctx context.Context, instance *operationv1.Operation) error {
	log := r.Log

	err := r.Delete(ctx, instance)
	if err != nil {
		log.V(1).Info("Cleanup Operation", "Error", err)
		return err
	}
	log.V(1).Info("Operation is done, cleanup", "namespace", instance.Namespace, "name", instance.Name)
	return nil
}

// handleTTL checks if operation has tll field set and if it is done and the ttl is exceeded.
func (r *OperationReconciler) handleTTL(ctx context.Context, instance *operationv1.Operation) (ctrl.Result, error) {
	log := r.Log

	currentTime := time.Now()
	ttl := instance.Termination.TTLSecondsAfterFinished
	if ttl == nil {
		// We clean right away
		return ctrl.Result{}, r.delete(ctx, instance)
	}
	duration := time.Second * time.Duration(*ttl)
	futureTime := instance.Status.CompletionTime.Add(duration)
	if currentTime.After(futureTime) {
		log.V(1).Info("Cleanup triggered based on TTLSecondsAfterFinished")
		return ctrl.Result{}, r.delete(ctx, instance)
	}
	// Reschedule another check
	requeueAfter := futureTime.Sub(currentTime)
	log.V(1).Info("Requeue reconciliation", "After", requeueAfter)
	return ctrl.Result{Requeue: true, RequeueAfter: requeueAfter}, nil
}

// handlePastActiveDeadline checks if operation has ActiveDeadlineSeconds field set and if it is exceeded.
func (r *OperationReconciler) handlePastActiveDeadline(ctx context.Context, instance *operationv1.Operation) (*time.Duration, error) {
	log := r.Log

	activeDeadlineSeconds := instance.Termination.ActiveDeadlineSeconds
	startTime := instance.Status.StartTime
	if activeDeadlineSeconds == nil || startTime == nil {
		return nil, nil
	}
	currentTime := metav1.Now()
	duration := currentTime.Time.Sub(startTime.Time)
	allowedDuration := time.Second * time.Duration(*activeDeadlineSeconds)
	if duration >= allowedDuration {
		log.V(1).Info("Cleanup triggered based on ActiveDeadlineSeconds")
		if updated := instance.LogStopped("DeadlineExceeded", "Cleanup triggered based on ActiveDeadlineSeconds, operation was active longer than specified deadline"); updated {
			log.V(1).Info("Operation Logging Status Stopped")
			if statusErr := r.Status().Update(ctx, instance); statusErr != nil {
				return nil, statusErr
			}
			r.instanceSyncStatus(instance)
		}
		return nil, r.delete(ctx, instance)
	}

	if len(instance.Status.Conditions) <= 2 {
		// Reschedule another check
		futureTime := startTime.Add(allowedDuration)
		requeueAfter := futureTime.Sub(currentTime.Time)
		log.V(1).Info("Requeue reconciliation", "After", requeueAfter)
		return &requeueAfter, nil
	}

	return nil, nil
}

func (r *OperationReconciler) getBackOff(backOff int32) time.Duration {
	// The backoff is capped such that 'calculated' value never overflows.
	delay := float64(1) * math.Pow(2, float64(backOff))
	if delay > math.MaxInt64 {
		return MaxBackOff
	}
	return time.Duration(delay)
}
