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

import (
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("Helpers", func() {

	BeforeEach(func() {
		// Add any setup steps that needs to be executed before each test
	})

	AfterEach(func() {
		// Add any teardown steps that needs to be executed after each test
	})

	Context("Helpers", func() {
		It("should contain string", func() {
			slice1 := []string{"foo", "bar", "moo"}
			slice2 := []string{"foo2", "boo2", "moo2"}

			for _, str := range slice1 {
				Expect(containsString(slice1, str)).To(BeTrue())
			}

			for _, str := range slice2 {
				Expect(containsString(slice1, str)).To(BeFalse())
			}
		})

		It("should remove string", func() {
			slice := []string{"foo", "bar", "moo"}
			before := len(slice)

			for _, str := range slice {
				Expect(containsString(removeString(slice, str), str)).To(BeFalse())
			}

			for _, str := range slice {
				Expect(len(slice)).To(BeIdenticalTo(before))
				slice = removeString(slice, str)
				Expect(len(slice)).To(BeIdenticalTo(before - 1))
				before--
			}

			Expect(len(slice)).To(BeIdenticalTo(0))
		})
	})
})
