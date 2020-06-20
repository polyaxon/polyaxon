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

package plugins

import (
	"fmt"
	"time"

	"github.com/go-logr/logr"
	"github.com/go-openapi/strfmt"

	httpRuntime "github.com/go-openapi/runtime"
	httptransport "github.com/go-openapi/runtime/client"
	netContext "golang.org/x/net/context"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
	"github.com/polyaxon/polyaxon/operator/controllers/config"

	polyaxonSDK "github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_client"
	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_client/runs_v1"
	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

const (
	apiServerDefaultTimeout = 35 * time.Second

	// PolyaxonAuthToken polyaxon auth token
	PolyaxonAuthToken = "POLYAXON_AUTH_TOKEN"

	// PolyaxonAPIHost polyaxon api host
	PolyaxonAPIHost = "POLYAXON_PROXY_API_HOST"

	// PolyaxonAPIPort polyaxon api port
	PolyaxonAPIPort = "POLYAXON_PROXY_API_PORT"

	// PolyaxonStreamsHost polyaxon streams host
	PolyaxonStreamsHost = "POLYAXON_PROXY_STREAMS_HOST"

	// PolyaxonStreamsPort polyaxon api port
	PolyaxonStreamsPort = "POLYAXON_PROXY_STREAMS_PORT"
)

func polyaxonAuth(name, value string) httpRuntime.ClientAuthInfoWriter {
	return httpRuntime.ClientAuthInfoWriterFunc(func(r httpRuntime.ClientRequest, _ strfmt.Registry) error {
		return r.SetHeaderParam("Authorization", name+" "+value)
	})
}

func polyaxonHost(host string, port int) string {
	return fmt.Sprintf("%s:%d", host, port)
}

// NotifyPolyaxonRunStatus creates polyaxon run status
func NotifyPolyaxonRunStatus(namespace, name, owner, project, uuid string, statusCond operationv1.OperationCondition, connections []string, log logr.Logger) error {
	token := config.GetStrEnv(PolyaxonAuthToken, "72d2f09b59b646f6863c464465bf6c80c83fbd992b5e4d8bb3eb194c565023cb")
	host := polyaxonHost(config.GetStrEnv(PolyaxonStreamsHost, "localhost"), config.GetIntEnv(PolyaxonStreamsPort, 8000))

	plxClient := polyaxonSDK.New(httptransport.New(host, "", []string{"http"}), strfmt.Default)
	plxToken := polyaxonAuth("Token", token)

	ctx, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	params := &runs_v1.NotifyRunStatusParams{
		Namespace: namespace,
		Owner:     owner,
		Project:   project,
		UUID:      uuid,
		Body: &service_model.V1EntityNotificationBody{
			Name:        name,
			Connections: connections,
			Condition: &service_model.V1StatusCondition{
				LastTransitionTime: strfmt.DateTime(statusCond.LastTransitionTime.Time),
				LastUpdateTime:     strfmt.DateTime(statusCond.LastUpdateTime.Time),
				Message:            statusCond.Message,
				Reason:             statusCond.Reason,
				Status:             string(statusCond.Status),
				Type:               service_model.V1Statuses(statusCond.Type),
			},
		},
		Context: ctx,
	}
	_, _, err := plxClient.RunsV1.NotifyRunStatus(params, plxToken)
	return err
}

// LogPolyaxonRunStatus creates polyaxon run status
func LogPolyaxonRunStatus(owner, project, uuid string, statusCond operationv1.OperationCondition, log logr.Logger) error {
	token := config.GetStrEnv(PolyaxonAuthToken, "72d2f09b59b646f6863c464465bf6c80c83fbd992b5e4d8bb3eb194c565023cb")
	host := polyaxonHost(config.GetStrEnv(PolyaxonAPIHost, "localhost"), config.GetIntEnv(PolyaxonAPIPort, 8000))

	plxClient := polyaxonSDK.New(httptransport.New(host, "", []string{"http"}), strfmt.Default)
	plxToken := polyaxonAuth("Token", token)

	ctx, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	params := &runs_v1.CreateRunStatusParams{
		Owner:   owner,
		Project: project,
		UUID:    uuid,
		Body: &service_model.V1EntityStatusBodyRequest{
			Condition: &service_model.V1StatusCondition{
				LastTransitionTime: strfmt.DateTime(statusCond.LastTransitionTime.Time),
				LastUpdateTime:     strfmt.DateTime(statusCond.LastUpdateTime.Time),
				Message:            statusCond.Message,
				Reason:             statusCond.Reason,
				Status:             string(statusCond.Status),
				Type:               service_model.V1Statuses(statusCond.Type),
			},
		},
		Context: ctx,
	}
	_, _, err := plxClient.RunsV1.CreateRunStatus(params, plxToken)
	return err
}

// CollectPolyaxonRunLogs archives logs before removing the operation
func CollectPolyaxonRunLogs(namespace, owner, project, uuid string, log logr.Logger) error {
	token := config.GetStrEnv(PolyaxonAuthToken, "72d2f09b59b646f6863c464465bf6c80c83fbd992b5e4d8bb3eb194c565023cb")
	host := polyaxonHost(config.GetStrEnv(PolyaxonStreamsHost, "localhost"), config.GetIntEnv(PolyaxonStreamsPort, 8000))

	plxClient := polyaxonSDK.New(httptransport.New(host, "", []string{"http"}), strfmt.Default)
	plxToken := polyaxonAuth("Token", token)

	ctx, cancel := netContext.WithTimeout(netContext.Background(), apiServerDefaultTimeout)
	defer cancel()

	params := &runs_v1.CollectRunLogsParams{
		Namespace: namespace,
		Owner:     owner,
		Project:   project,
		UUID:      uuid,
		Context:   ctx,
	}
	_, _, err := plxClient.RunsV1.CollectRunLogs(params, plxToken)
	return err
}
