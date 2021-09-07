// Copyright 2018-2021 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Code generated by go-swagger; DO NOT EDIT.

package runs_v1

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"context"
	"net/http"
	"time"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/runtime"
	cr "github.com/go-openapi/runtime/client"
	"github.com/go-openapi/strfmt"

	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

// NewRestoreRunsParams creates a new RestoreRunsParams object,
// with the default timeout for this client.
//
// Default values are not hydrated, since defaults are normally applied by the API server side.
//
// To enforce default values in parameter, use SetDefaults or WithDefaults.
func NewRestoreRunsParams() *RestoreRunsParams {
	return &RestoreRunsParams{
		timeout: cr.DefaultTimeout,
	}
}

// NewRestoreRunsParamsWithTimeout creates a new RestoreRunsParams object
// with the ability to set a timeout on a request.
func NewRestoreRunsParamsWithTimeout(timeout time.Duration) *RestoreRunsParams {
	return &RestoreRunsParams{
		timeout: timeout,
	}
}

// NewRestoreRunsParamsWithContext creates a new RestoreRunsParams object
// with the ability to set a context for a request.
func NewRestoreRunsParamsWithContext(ctx context.Context) *RestoreRunsParams {
	return &RestoreRunsParams{
		Context: ctx,
	}
}

// NewRestoreRunsParamsWithHTTPClient creates a new RestoreRunsParams object
// with the ability to set a custom HTTPClient for a request.
func NewRestoreRunsParamsWithHTTPClient(client *http.Client) *RestoreRunsParams {
	return &RestoreRunsParams{
		HTTPClient: client,
	}
}

/* RestoreRunsParams contains all the parameters to send to the API endpoint
   for the restore runs operation.

   Typically these are written to a http.Request.
*/
type RestoreRunsParams struct {

	/* Body.

	   Uuids of the entities
	*/
	Body *service_model.V1Uuids

	/* Owner.

	   Owner of the namespace
	*/
	Owner string

	/* Project.

	   Project under namesapce
	*/
	Project string

	timeout    time.Duration
	Context    context.Context
	HTTPClient *http.Client
}

// WithDefaults hydrates default values in the restore runs params (not the query body).
//
// All values with no default are reset to their zero value.
func (o *RestoreRunsParams) WithDefaults() *RestoreRunsParams {
	o.SetDefaults()
	return o
}

// SetDefaults hydrates default values in the restore runs params (not the query body).
//
// All values with no default are reset to their zero value.
func (o *RestoreRunsParams) SetDefaults() {
	// no default values defined for this parameter
}

// WithTimeout adds the timeout to the restore runs params
func (o *RestoreRunsParams) WithTimeout(timeout time.Duration) *RestoreRunsParams {
	o.SetTimeout(timeout)
	return o
}

// SetTimeout adds the timeout to the restore runs params
func (o *RestoreRunsParams) SetTimeout(timeout time.Duration) {
	o.timeout = timeout
}

// WithContext adds the context to the restore runs params
func (o *RestoreRunsParams) WithContext(ctx context.Context) *RestoreRunsParams {
	o.SetContext(ctx)
	return o
}

// SetContext adds the context to the restore runs params
func (o *RestoreRunsParams) SetContext(ctx context.Context) {
	o.Context = ctx
}

// WithHTTPClient adds the HTTPClient to the restore runs params
func (o *RestoreRunsParams) WithHTTPClient(client *http.Client) *RestoreRunsParams {
	o.SetHTTPClient(client)
	return o
}

// SetHTTPClient adds the HTTPClient to the restore runs params
func (o *RestoreRunsParams) SetHTTPClient(client *http.Client) {
	o.HTTPClient = client
}

// WithBody adds the body to the restore runs params
func (o *RestoreRunsParams) WithBody(body *service_model.V1Uuids) *RestoreRunsParams {
	o.SetBody(body)
	return o
}

// SetBody adds the body to the restore runs params
func (o *RestoreRunsParams) SetBody(body *service_model.V1Uuids) {
	o.Body = body
}

// WithOwner adds the owner to the restore runs params
func (o *RestoreRunsParams) WithOwner(owner string) *RestoreRunsParams {
	o.SetOwner(owner)
	return o
}

// SetOwner adds the owner to the restore runs params
func (o *RestoreRunsParams) SetOwner(owner string) {
	o.Owner = owner
}

// WithProject adds the project to the restore runs params
func (o *RestoreRunsParams) WithProject(project string) *RestoreRunsParams {
	o.SetProject(project)
	return o
}

// SetProject adds the project to the restore runs params
func (o *RestoreRunsParams) SetProject(project string) {
	o.Project = project
}

// WriteToRequest writes these params to a swagger request
func (o *RestoreRunsParams) WriteToRequest(r runtime.ClientRequest, reg strfmt.Registry) error {

	if err := r.SetTimeout(o.timeout); err != nil {
		return err
	}
	var res []error
	if o.Body != nil {
		if err := r.SetBodyParam(o.Body); err != nil {
			return err
		}
	}

	// path param owner
	if err := r.SetPathParam("owner", o.Owner); err != nil {
		return err
	}

	// path param project
	if err := r.SetPathParam("project", o.Project); err != nil {
		return err
	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}