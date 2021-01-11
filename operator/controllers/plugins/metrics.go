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

package plugins

import (
	"context"

	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/metrics"

	"github.com/prometheus/client_golang/prometheus"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

// Metrics exposed by the operator
type Metrics struct {
	cli                     client.Client
	OperationsRunning       *prometheus.GaugeVec
	OperationsCreated       *prometheus.CounterVec
	OperationsFailedCreated *prometheus.CounterVec
}

// NewMetrics prometheus initializer
func NewMetrics(cli client.Client) *Metrics {
	m := &Metrics{
		cli: cli,
		OperationsRunning: prometheus.NewGaugeVec(
			prometheus.GaugeOpts{
				Name: "operations_running",
				Help: "Current running operations in the cluster",
			},
			[]string{"namespace"},
		),
		OperationsCreated: prometheus.NewCounterVec(
			prometheus.CounterOpts{
				Name: "operations_created",
				Help: "Total nuber of operations created",
			},
			[]string{"namespace"},
		),
		OperationsFailedCreated: prometheus.NewCounterVec(
			prometheus.CounterOpts{
				Name: "notebook_create_failed_total",
				Help: "Total nuber of operations creation failures",
			},
			[]string{"namespace"},
		),
	}

	metrics.Registry.MustRegister(m)
	return m
}

// Describe implements the prometheus.Collector interface.
func (m *Metrics) Describe(ch chan<- *prometheus.Desc) {
	m.OperationsRunning.Describe(ch)
	m.OperationsCreated.Describe(ch)
	m.OperationsFailedCreated.Describe(ch)
}

// Collect implements the prometheus.Collector interface.
func (m *Metrics) Collect(ch chan<- prometheus.Metric) {
	m.scrape()
	m.OperationsRunning.Collect(ch)
	m.OperationsCreated.Collect(ch)
	m.OperationsFailedCreated.Collect(ch)
}

// scrape gets current running operations.
func (m *Metrics) scrape() {
	operations := &operationv1.OperationList{}
	err := m.cli.List(context.TODO(), operations)
	if err != nil {
		return
	}
	stsCache := make(map[string]float64)
	for _, op := range operations.Items {
		stsCache[op.Namespace]++
	}

	for ns, op := range stsCache {
		m.OperationsRunning.WithLabelValues(ns).Set(op)
	}
}
