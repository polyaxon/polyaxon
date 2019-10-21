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

package utils

import (
	"time"

	corev1 "k8s.io/api/core/v1"
)

// GetPodPort returns the pod's port from the container definition
func GetPodPort(podSpec corev1.PodSpec, defaultPort int) int {
	port := defaultPort
	containerPorts := podSpec.Containers[0].Ports
	if containerPorts != nil {
		port = int(containerPorts[0].ContainerPort)
	}
	return port
}

func getPodLastTime(pod *corev1.Pod, lastTime *time.Time) (bool, *time.Time, error) {
	timeRaw := pod.ObjectMeta.CreationTimestamp.Time
	if lastTime == nil || lastTime.Before(timeRaw) {
		return true, &timeRaw, nil
	}

	return false, lastTime, nil
}

// GetLastPod returns the last pod bassed on the creation time of the items
func GetLastPod(pods corev1.PodList) (*corev1.Pod, error) {
	lastTime := &time.Time{}
	lastPod := &corev1.Pod{}
	isLast := false
	var err error
	for _, pod := range pods.Items {
		isLast, lastTime, err = getPodLastTime(&pod, lastTime)
		if err != nil {
			return nil, err
		}
		if isLast {
			lastPod = &pod
		}
	}
	return lastPod, nil
}

// Get the pod status
// func getPodStatus(lastPod *corev1.Pod) {
// 	if len(lastPod.Status.ContainerStatuses) > 0 &&
// 		lastPod.Status.ContainerStatuses[0].State != plxNotebook.Status.ContainerState {
// 		log.V(1).Info("Updating container state: ", "namespace", plxNotebook.Namespace, "name", plxNotebook.Name)
// 		cs := lastPod.Status.ContainerStatuses[0].State
// 		plxNotebook.Status.ContainerState = cs
// 		oldConditions := plxNotebook.Status.Conditions
// 		newCondition := getNextCondition(cs)
// 		// Append new condition
// 		if len(oldConditions) == 0 || oldConditions[0].Type != newCondition.Type ||
// 			oldConditions[0].Reason != newCondition.Reason ||
// 			oldConditions[0].Message != newCondition.Message {
// 			log.V(1).Info("Appending to conditions: ", "namespace", plxNotebook.Namespace, "name", plxNotebook.Name, "type", newCondition.Type, "reason", newCondition.Reason, "message", newCondition.Message)
// 			plxNotebook.Status.Conditions = append([]corev1alpha1.PolyaxonDeploymentCondition{newCondition}, oldConditions...)
// 		}
// 		err = r.Status().Update(context.Background(), plxNotebook)
// 		if err != nil {
// 			return ctrl.Result{}, err
// 		}
// 	}
// }
