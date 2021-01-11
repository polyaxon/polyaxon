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
	"reflect"

	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
)

// CopyUnstructuredSpec copies the owned fields from one unstructured to another
// Returns true if the fields copied from don't match to.
func CopyUnstructuredSpec(from, to *unstructured.Unstructured, fields []string) bool {
	requireUpdate := false

	for field := range fields {
		if CopyUnstructuredField(from, to, fields[field]) {
			requireUpdate = true
		}
	}
	return requireUpdate
}

// CopyUnstructuredField copies the owned fields from one unstructured to another
// Returns true if the fields copied from don't match to.
func CopyUnstructuredField(from, to *unstructured.Unstructured, field string) bool {
	fromSpec, found, err := unstructured.NestedMap(from.Object, field)
	if !found {
		return false
	}
	if err != nil {
		return false
	}

	toSpec, found, err := unstructured.NestedMap(to.Object, field)
	if !found || err != nil {
		unstructured.SetNestedMap(to.Object, fromSpec, field)
		return true
	}

	requiresUpdate := !reflect.DeepEqual(fromSpec, toSpec)
	if requiresUpdate {
		unstructured.SetNestedMap(to.Object, fromSpec, field)
	}
	return requiresUpdate
}
