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

package managers

import (
	"time"

	corev1 "k8s.io/api/core/v1"
)

// GetPodPorts returns the pod's port from the container definition
func GetPodPorts(podSpec corev1.PodSpec, defaultPort int) []int32 {
	ports := []int32{int32(defaultPort)}
	containerPorts := podSpec.Containers[0].Ports
	if containerPorts != nil {
		ports = []int32{}
		for _, cp := range containerPorts {
			ports = append(ports, cp.ContainerPort)
		}
	}
	return ports
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
