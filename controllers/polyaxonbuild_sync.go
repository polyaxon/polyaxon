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

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"

	"github.com/polyaxon/polyaxon-sdks/go/http_client/v1/service_client/build_service"
	"github.com/polyaxon/polyaxon-sdks/go/http_client/v1/service_model"
)

const (
	apiServerDefaultTimeout = 35 * time.Second
)

// TODO: move this logic to sdk as a high level client

func (r *PolyaxonBuildReconciler) syncStatus(instance *corev1alpha1.PolyaxonBuild) error {
	log := r.Log

	log.Info("Build sync status", "Syncing", instance.GetName())

	ctx, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	lastCond := instance.Status.Conditions[len(instance.Status.Conditions)-1]

	jobName := strings.Split(instance.ObjectMeta.Labels["job_name"], ".")
	params := &build_service.CreateBuildStatusParams{
		Owner:   jobName[0],
		Project: jobName[1],
		ID:      jobName[3],
		Body: &service_model.V1EntityStatusRequest{
			Status: strings.ToLower(string(lastCond.Type)),
		},
		Context: ctx,
	}
	_, err := r.PlxClient.BuildService.CreateBuildStatus(params, r.PlxToken)
	return err
}

func (r *PolyaxonBuildReconciler) collectLogs(instance *corev1alpha1.PolyaxonBuild) error {
	log := r.Log

	log.Info("Build logs collection", "Finalizer", instance.GetName())

	_, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	// _, err := r.PlxClient.BuildService.CreateBuildLogs(params, r.PlxToken)
	return nil
}
