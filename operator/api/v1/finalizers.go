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

package v1

// OperationLogsFinalizer registration
const OperationLogsFinalizer = "operation.logs.finalizers.polyaxon.com"

// HasLogsFinalizer check for Operation
func (instance *Operation) HasLogsFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, OperationLogsFinalizer)
}

// AddLogsFinalizer handler for Operation
func (instance *Operation) AddLogsFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, OperationLogsFinalizer)
}

// RemoveLogsFinalizer handler for Operation
func (instance *Operation) RemoveLogsFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, OperationLogsFinalizer)
}

// OperationNotificationsFinalizer registration
const OperationNotificationsFinalizer = "operation.notifications.finalizers.polyaxon.com"

// HasNotificationsFinalizer check for Operation
func (instance *Operation) HasNotificationsFinalizer() bool {
	return containsString(instance.ObjectMeta.Finalizers, OperationNotificationsFinalizer)
}

// AddNotificationsFinalizer handler for Operation
func (instance *Operation) AddNotificationsFinalizer() {
	instance.ObjectMeta.Finalizers = append(instance.ObjectMeta.Finalizers, OperationNotificationsFinalizer)
}

// RemoveNotificationsFinalizer handler for Operation
func (instance *Operation) RemoveNotificationsFinalizer() {
	instance.ObjectMeta.Finalizers = removeString(instance.ObjectMeta.Finalizers, OperationNotificationsFinalizer)
}
