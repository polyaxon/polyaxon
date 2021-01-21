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
	"context"
	"strconv"
	"time"

	"github.com/pkg/errors"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/labels"

	"sigs.k8s.io/controller-runtime/pkg/client"
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

// ListPods returns the list of pods based on selctor
func ListPods(controllerClient client.Client, namespace string, selector map[string]string) (*corev1.PodList, error) {

	clientOpt := &client.ListOptions{
		Namespace:     namespace,
		LabelSelector: labels.SelectorFromSet(selector),
	}

	opt := []client.ListOption{
		clientOpt,
	}

	podList := &corev1.PodList{}
	return podList, controllerClient.List(context.TODO(), podList, opt...)
}

// HasUnschedulablePods Detects if entity has unschedulable pods
func HasUnschedulablePods(controllerClient client.Client, instance *operationv1.Operation) (operationv1.OperationConditionType, string, string) {
	instanceID, ok := instance.ObjectMeta.Labels["app.kubernetes.io/instance"]
	if !ok {
		return "", "", ""
	}
	labels := map[string]string{
		"app.kubernetes.io/instance": instanceID,
	}
	podsList, err := ListPods(controllerClient, instance.Namespace, labels)
	if err != nil || len(podsList.Items) < 1 {
		return operationv1.OperationStarting, "PodNotReady", "Operation has no pods yet."
	}
	for _, pod := range podsList.Items {
		if pod.Status.Phase == corev1.PodFailed {
			for _, cs := range pod.Status.ContainerStatuses {
				if cs.State.Terminated != nil && cs.State.Terminated.ExitCode > 0 {
					return operationv1.OperationFailed, cs.State.Terminated.Reason + "ExitCode " + strconv.Itoa(int(cs.State.Terminated.ExitCode)), cs.State.Terminated.Message
				}
			}
			return operationv1.OperationFailed, "PodFailed", pod.Status.Message
		}
		if pod.Status.Phase == corev1.PodSucceeded {
			return "", "", ""
		}
		if pod.Status.Phase != corev1.PodRunning && pod.Status.Conditions != nil {
			if pod.Status.InitContainerStatuses != nil {
				for _, cs := range pod.Status.InitContainerStatuses {
					if cs.Ready == false && cs.State.Waiting != nil && cs.State.Waiting.Reason == "ImagePullBackOff" {
						return operationv1.OperationWarning, "InitContainerImagePullBackOff", cs.State.Waiting.Message
					}
				}
			}
			for _, cs := range pod.Status.ContainerStatuses {
				if cs.Ready == false && cs.State.Waiting != nil && cs.State.Waiting.Reason == "ImagePullBackOff" {
					return operationv1.OperationWarning, "ImagePullBackOff", cs.State.Waiting.Message
				}
			}
			for _, cond := range pod.Status.Conditions {
				if (cond.Reason == corev1.PodReasonUnschedulable) ||
					(cond.Type == corev1.PodReady && cond.Status == corev1.ConditionFalse && cond.Reason == "ContainersNotReady") {
					return operationv1.OperationWarning, "ContainersNotReady", cond.Message
				}
			}
		}
		if pod.Status.Phase == corev1.PodReasonUnschedulable {
			return operationv1.OperationWarning, "PodReasonUnschedulable", "Pod is unschedulable"
		}
		if pod.Status.Phase == corev1.PodPending && pod.Status.Conditions == nil {
			return operationv1.OperationWarning, "PodPending", "Pod is still pending without conditions"
		}
	}
	return "", "", ""
}

func ListMatchingOperations(ctx context.Context, c client.Client, pod metav1.Object) ([]*operationv1.Operation, error) {
	// Find any Operation objects that match this pod.
	allOperations := &operationv1.OperationList{}
	err := c.List(ctx, allOperations, &client.ListOptions{Namespace: pod.GetNamespace()})
	if err != nil {
		return nil, errors.Wrapf(err, "error listing operations in %s", pod.GetNamespace())
	}
	operations := []*operationv1.Operation{}
	podLabels := labels.Set(pod.GetLabels())
	for _, m := range allOperations.Items {
		instanceID, ok := m.ObjectMeta.Labels["app.kubernetes.io/instance"]
		if !ok {
			// No slecotor
			return operations, nil
		}
		instanceLabel := map[string]string{
			"app.kubernetes.io/instance": instanceID,
		}
		lebelSelector := &metav1.LabelSelector{
			MatchLabels: instanceLabel,
		}
		selector, err := metav1.LabelSelectorAsSelector(lebelSelector)
		if err != nil {
			// Ignore this operation. Maybe print a warning in the future? This should probably be handled via a validator on Operation.
			continue
		}
		if selector.Matches(podLabels) {
			operation := m
			operations = append(operations, &operation)
		}
	}
	return operations, nil
}
