// Copyright 2019 Polyaxon, Inc.
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

package dashboard_v1

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"fmt"
	"io"

	"github.com/go-openapi/runtime"

	strfmt "github.com/go-openapi/strfmt"

	service_model "github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

// ListDashboardReader is a Reader for the ListDashboard structure.
type ListDashboardReader struct {
	formats strfmt.Registry
}

// ReadResponse reads a server response into the received o.
func (o *ListDashboardReader) ReadResponse(response runtime.ClientResponse, consumer runtime.Consumer) (interface{}, error) {
	switch response.Code() {
	case 200:
		result := NewListDashboardOK()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 204:
		result := NewListDashboardNoContent()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 403:
		result := NewListDashboardForbidden()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result
	case 404:
		result := NewListDashboardNotFound()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result

	default:
		return nil, runtime.NewAPIError("unknown error", response, response.Code())
	}
}

// NewListDashboardOK creates a ListDashboardOK with default headers values
func NewListDashboardOK() *ListDashboardOK {
	return &ListDashboardOK{}
}

/*ListDashboardOK handles this case with default header values.

A successful response.
*/
type ListDashboardOK struct {
	Payload *service_model.V1ListDashboardsResponse
}

func (o *ListDashboardOK) Error() string {
	return fmt.Sprintf("[GET /api/v1/{owner}/{project}/dashboards][%d] listDashboardOK  %+v", 200, o.Payload)
}

func (o *ListDashboardOK) GetPayload() *service_model.V1ListDashboardsResponse {
	return o.Payload
}

func (o *ListDashboardOK) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	o.Payload = new(service_model.V1ListDashboardsResponse)

	// response payload
	if err := consumer.Consume(response.Body(), o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewListDashboardNoContent creates a ListDashboardNoContent with default headers values
func NewListDashboardNoContent() *ListDashboardNoContent {
	return &ListDashboardNoContent{}
}

/*ListDashboardNoContent handles this case with default header values.

No content.
*/
type ListDashboardNoContent struct {
	Payload interface{}
}

func (o *ListDashboardNoContent) Error() string {
	return fmt.Sprintf("[GET /api/v1/{owner}/{project}/dashboards][%d] listDashboardNoContent  %+v", 204, o.Payload)
}

func (o *ListDashboardNoContent) GetPayload() interface{} {
	return o.Payload
}

func (o *ListDashboardNoContent) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewListDashboardForbidden creates a ListDashboardForbidden with default headers values
func NewListDashboardForbidden() *ListDashboardForbidden {
	return &ListDashboardForbidden{}
}

/*ListDashboardForbidden handles this case with default header values.

You don't have permission to access the resource.
*/
type ListDashboardForbidden struct {
	Payload interface{}
}

func (o *ListDashboardForbidden) Error() string {
	return fmt.Sprintf("[GET /api/v1/{owner}/{project}/dashboards][%d] listDashboardForbidden  %+v", 403, o.Payload)
}

func (o *ListDashboardForbidden) GetPayload() interface{} {
	return o.Payload
}

func (o *ListDashboardForbidden) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewListDashboardNotFound creates a ListDashboardNotFound with default headers values
func NewListDashboardNotFound() *ListDashboardNotFound {
	return &ListDashboardNotFound{}
}

/*ListDashboardNotFound handles this case with default header values.

Resource does not exist.
*/
type ListDashboardNotFound struct {
	Payload interface{}
}

func (o *ListDashboardNotFound) Error() string {
	return fmt.Sprintf("[GET /api/v1/{owner}/{project}/dashboards][%d] listDashboardNotFound  %+v", 404, o.Payload)
}

func (o *ListDashboardNotFound) GetPayload() interface{} {
	return o.Payload
}

func (o *ListDashboardNotFound) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}