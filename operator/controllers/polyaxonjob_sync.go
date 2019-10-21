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
	"strings"
	"time"

	netContext "golang.org/x/net/context"

	"github.com/go-openapi/strfmt"
	corev1alpha1 "github.com/polyaxon/polyaxon/operator/api/v1alpha1"

	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_client/runs_v1"
	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

const (
	apiServerDefaultTimeout = 35 * time.Second
)

// TODO: move this logic to sdk as a high level client

func (r *PolyaxonJobReconciler) syncStatus(instance *corev1alpha1.PolyaxonJob) error {
	log := r.Log

	log.Info("Job sync status", "Syncing", instance.GetName())

	instanceName, ok := instance.ObjectMeta.Labels["app.kubernetes.io/instance"]
	if !ok || instanceName == "" {
		log.Info("Job cannot be synced", "Instance", instance.Name, "Does not exist", instance.GetName())
		return nil
	}
	jobName := strings.Split(instanceName, ".")
	if len(jobName) != 4 {
		log.Info("Job cannot be synced", "Instance", instance.Name, "Job name is not valid", instanceName)
		return nil
	}

	lastCond := instance.Status.Conditions[len(instance.Status.Conditions)-1]
	status := strings.ToLower(string(lastCond.Type))

	return r.createJobStatus(jobName[0], jobName[1], jobName[3], status, lastCond)
}

func (r *PolyaxonJobReconciler) createJobStatus(owner, project, uuid, status string, statusCond corev1alpha1.PolyaxonBaseJobCondition) error {
	ctx, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	params := &runs_v1.CreateRunStatusParams{
		Owner:   owner,
		Project: project,
		UUID:    uuid,
		Body: &service_model.V1StatusCondition{
			LastTransitionTime: strfmt.DateTime(statusCond.LastTransitionTime.Time),
			LastUpdateTime:     strfmt.DateTime(statusCond.LastUpdateTime.Time),
			Message:            statusCond.Message,
			Reason:             statusCond.Reason,
			Status:             string(statusCond.Status),
			Type:               string(statusCond.Type),
		},
		Context: ctx,
	}
	_, err := r.PlxClient.RunsV1.CreateRunStatus(params, r.PlxToken)
	return err
}

func (r *PolyaxonJobReconciler) collectLogs(instance *corev1alpha1.PolyaxonJob) error {
	log := r.Log

	log.Info("Job logs collection", "Finalizer", instance.GetName())

	_, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	// _, err := r.PlxClient.JobService.CreateJobLogs(params, r.PlxToken)
	return nil
}
