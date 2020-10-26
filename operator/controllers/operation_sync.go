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
	"time"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/config"
	"github.com/polyaxon/polyaxon/operator/controllers/plugins"
)

const (
	apiServerDefaultTimeout = 35 * time.Second
)

func (r *OperationReconciler) instanceSyncStatus(instance *operationv1.Operation) error {
	lastCond := instance.Status.Conditions[len(instance.Status.Conditions)-1]
	return r.syncStatus(instance, lastCond)
}

func (r *OperationReconciler) getInstanceInfo(instance *operationv1.Operation) (string, string, string, string, bool) {
	instanceID, ok := instance.ObjectMeta.Labels["app.kubernetes.io/instance"]
	if !ok || instanceID == "" {
		return "", "", "", "", false
	}

	instanceOwner, ok := instance.ObjectMeta.Annotations["operation.polyaxon.com/owner"]
	if !ok || instanceOwner == "" {
		return "", "", "", "", false
	}

	instanceProject, ok := instance.ObjectMeta.Annotations["operation.polyaxon.com/project"]
	if !ok || instanceProject == "" {
		return "", "", "", "", false
	}

	instanceKind, ok := instance.ObjectMeta.Annotations["operation.polyaxon.com/kind"]
	if !ok || instanceKind == "" {
		instanceKind = "operation" // backward compatibility
	}

	return instanceOwner, instanceProject, instanceID, instanceKind, true
}

func (r *OperationReconciler) syncStatus(instance *operationv1.Operation, statusCond operationv1.OperationCondition) error {
	if !config.GetBoolEnv("POLYAXON_AGENT_ENABLED", true) || !instance.SyncStatuses {
		return nil
	}

	log := r.Log

	log.Info("Operation sync status", "Syncing", instance.GetName(), "Status", statusCond.Type)
	owner, project, instanceID, _, ok := r.getInstanceInfo(instance)
	if !ok {
		log.Info("Operation cannot be synced", "Instance", instance.Name, "Uuid Does not exist", instance.GetName())
		return nil
	}
	return plugins.LogPolyaxonRunStatus(owner, project, instanceID, statusCond, r.Log)
}

func (r *OperationReconciler) notify(instance *operationv1.Operation) error {

	if !config.GetBoolEnv("POLYAXON_AGENT_ENABLED", true) || len(instance.Notifications) == 0 {
		return nil
	}

	log := r.Log

	log.Info("Operation notify status", "Notifying", instance.GetName())

	owner, project, instanceID, _, ok := r.getInstanceInfo(instance)
	if !ok {
		log.Info("Operation cannot be synced", "Instance", instance.Name, "Uuid Does not exist", instance.GetName())
		return nil
	}

	name, ok := instance.ObjectMeta.Annotations["operation.polyaxon.com/name"]
	if !ok {
		name = ""
	}

	if len(instance.Status.Conditions) == 0 {
		log.Info("Operation cannot be notified", "Instance", instance.Name, "No conditions", instance.GetName())
		return nil
	}
	lastCond := instance.Status.Conditions[len(instance.Status.Conditions)-1]

	connections := []string{}
	for _, notification := range instance.Notifications {
		if notification.Trigger == operationv1.OperationDoneTrigger || operationv1.OperationConditionType(notification.Trigger) == lastCond.Type {
			connections = append(connections, notification.Connections...)
		}
	}

	if len(connections) == 0 {
		log.Info("Operation no notification", "Instance", instance.Name, "No connections for status", lastCond.Type)
		return nil
	}

	log.Info("Operation notify status", "Status", lastCond.Type, "Instance", instance.GetName())
	return plugins.NotifyPolyaxonRunStatus(instance.Namespace, name, owner, project, instanceID, lastCond, connections, r.Log)
}

func (r *OperationReconciler) collectLogs(instance *operationv1.Operation) error {

	if !config.GetBoolEnv("POLYAXON_AGENT_ENABLED", true) || !instance.CollectLogs {
		return nil
	}

	log := r.Log

	owner, project, instanceID, runKind, ok := r.getInstanceInfo(instance)
	if !ok {
		log.Info("Operation cannot be synced", "Instance", instance.Name, "Uuid Does not exist", instance.GetName())
		return nil
	}

	log.Info("Operation collect logs", "Instance", instance.GetName(), "kind", runKind)
	return plugins.CollectPolyaxonRunLogs(instance.Namespace, owner, project, instanceID, runKind, r.Log)
}
