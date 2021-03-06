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
	"fmt"
	"io"

	"github.com/go-openapi/runtime"
	"github.com/go-openapi/strfmt"

	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

// InvalidateRunsReader is a Reader for the InvalidateRuns structure.
type InvalidateRunsReader struct {
	formats strfmt.Registry
}

// ReadResponse reads a server response into the received o.
func (o *InvalidateRunsReader) ReadResponse(response runtime.ClientResponse, consumer runtime.Consumer) (interface{}, error) {
	switch response.Code() {
	case 200:
		result := NewInvalidateRunsOK()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 204:
		result := NewInvalidateRunsNoContent()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 403:
		result := NewInvalidateRunsForbidden()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result
	case 404:
		result := NewInvalidateRunsNotFound()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result
	default:
		result := NewInvalidateRunsDefault(response.Code())
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		if response.Code()/100 == 2 {
			return result, nil
		}
		return nil, result
	}
}

// NewInvalidateRunsOK creates a InvalidateRunsOK with default headers values
func NewInvalidateRunsOK() *InvalidateRunsOK {
	return &InvalidateRunsOK{}
}

/* InvalidateRunsOK describes a response with status code 200, with default header values.

A successful response.
*/
type InvalidateRunsOK struct {
}

func (o *InvalidateRunsOK) Error() string {
	return fmt.Sprintf("[POST /api/v1/{owner}/{project}/runs/invalidate][%d] invalidateRunsOK ", 200)
}

func (o *InvalidateRunsOK) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	return nil
}

// NewInvalidateRunsNoContent creates a InvalidateRunsNoContent with default headers values
func NewInvalidateRunsNoContent() *InvalidateRunsNoContent {
	return &InvalidateRunsNoContent{}
}

/* InvalidateRunsNoContent describes a response with status code 204, with default header values.

No content.
*/
type InvalidateRunsNoContent struct {
	Payload interface{}
}

func (o *InvalidateRunsNoContent) Error() string {
	return fmt.Sprintf("[POST /api/v1/{owner}/{project}/runs/invalidate][%d] invalidateRunsNoContent  %+v", 204, o.Payload)
}
func (o *InvalidateRunsNoContent) GetPayload() interface{} {
	return o.Payload
}

func (o *InvalidateRunsNoContent) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewInvalidateRunsForbidden creates a InvalidateRunsForbidden with default headers values
func NewInvalidateRunsForbidden() *InvalidateRunsForbidden {
	return &InvalidateRunsForbidden{}
}

/* InvalidateRunsForbidden describes a response with status code 403, with default header values.

You don't have permission to access the resource.
*/
type InvalidateRunsForbidden struct {
	Payload interface{}
}

func (o *InvalidateRunsForbidden) Error() string {
	return fmt.Sprintf("[POST /api/v1/{owner}/{project}/runs/invalidate][%d] invalidateRunsForbidden  %+v", 403, o.Payload)
}
func (o *InvalidateRunsForbidden) GetPayload() interface{} {
	return o.Payload
}

func (o *InvalidateRunsForbidden) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewInvalidateRunsNotFound creates a InvalidateRunsNotFound with default headers values
func NewInvalidateRunsNotFound() *InvalidateRunsNotFound {
	return &InvalidateRunsNotFound{}
}

/* InvalidateRunsNotFound describes a response with status code 404, with default header values.

Resource does not exist.
*/
type InvalidateRunsNotFound struct {
	Payload interface{}
}

func (o *InvalidateRunsNotFound) Error() string {
	return fmt.Sprintf("[POST /api/v1/{owner}/{project}/runs/invalidate][%d] invalidateRunsNotFound  %+v", 404, o.Payload)
}
func (o *InvalidateRunsNotFound) GetPayload() interface{} {
	return o.Payload
}

func (o *InvalidateRunsNotFound) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewInvalidateRunsDefault creates a InvalidateRunsDefault with default headers values
func NewInvalidateRunsDefault(code int) *InvalidateRunsDefault {
	return &InvalidateRunsDefault{
		_statusCode: code,
	}
}

/* InvalidateRunsDefault describes a response with status code -1, with default header values.

An unexpected error response.
*/
type InvalidateRunsDefault struct {
	_statusCode int

	Payload *service_model.RuntimeError
}

// Code gets the status code for the invalidate runs default response
func (o *InvalidateRunsDefault) Code() int {
	return o._statusCode
}

func (o *InvalidateRunsDefault) Error() string {
	return fmt.Sprintf("[POST /api/v1/{owner}/{project}/runs/invalidate][%d] InvalidateRuns default  %+v", o._statusCode, o.Payload)
}
func (o *InvalidateRunsDefault) GetPayload() *service_model.RuntimeError {
	return o.Payload
}

func (o *InvalidateRunsDefault) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	o.Payload = new(service_model.RuntimeError)

	// response payload
	if err := consumer.Consume(response.Body(), o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}
