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

package config

// These tests use Ginkgo (BDD-style Go testing framework). Refer to
// http://onsi.github.io/ginkgo/ to learn more about Ginkgo.

import (
	"os"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("Config", func() {

	BeforeEach(func() {
		// Add any setup steps that needs to be executed before each test
	})

	AfterEach(func() {
		// Add any teardown steps that needs to be executed after each test
	})

	Context("Config", func() {
		It("Config texts should get default", func() {
			Expect(GetStrEnv("TEST", "")).To(BeIdenticalTo(""))
			Expect(GetStrEnv("test", "test")).To(BeIdenticalTo("test"))
		})

		It("Config texts should get from envs", func() {
			os.Setenv("TEST", "foo")
			Expect(GetStrEnv("TEST", "")).To(BeIdenticalTo("foo"))
			Expect(GetStrEnv("TEST", "test")).To(BeIdenticalTo("foo"))
		})

		It("Config bool should get default", func() {
			Expect(GetBoolEnv("TEST", false)).To(BeFalse())
			Expect(GetBoolEnv("test", true)).To(BeTrue())
		})

		It("Config bool should get from envs", func() {
			os.Setenv("TEST", "true")
			Expect(GetBoolEnv("TEST", false)).To(BeTrue())
			Expect(GetBoolEnv("TEST", true)).To(BeTrue())

			os.Setenv("TEST", "false")
			Expect(GetBoolEnv("TEST", false)).To(BeFalse())
			Expect(GetBoolEnv("TEST", true)).To(BeFalse())
		})

		It("Config int should get default", func() {
			Expect(GetIntEnv("TEST", 0)).To(BeIdenticalTo(0))
			Expect(GetIntEnv("test", 10)).To(BeIdenticalTo(10))
		})

		It("Config int should get from envs", func() {
			os.Setenv("TEST", "100")
			Expect(GetIntEnv("TEST", 0)).To(BeIdenticalTo(100))
			Expect(GetIntEnv("TEST", 10)).To(BeIdenticalTo(100))
		})
	})
})
