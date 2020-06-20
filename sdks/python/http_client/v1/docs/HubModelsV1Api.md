# polyaxon_sdk.HubModelsV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_hub_model**](HubModelsV1Api.md#create_hub_model) | **POST** /api/v1/orgs/{owner}/models | Create hub model
[**delete_hub_model**](HubModelsV1Api.md#delete_hub_model) | **DELETE** /api/v1/orgs/{owner}/models/{uuid} | Delete hub model
[**get_hub_model**](HubModelsV1Api.md#get_hub_model) | **GET** /api/v1/orgs/{owner}/models/{uuid} | Get hub model
[**list_hub_model_names**](HubModelsV1Api.md#list_hub_model_names) | **GET** /api/v1/orgs/{owner}/models/names | List hub model names
[**list_hub_models**](HubModelsV1Api.md#list_hub_models) | **GET** /api/v1/orgs/{owner}/models | List hub models
[**patch_hub_model**](HubModelsV1Api.md#patch_hub_model) | **PATCH** /api/v1/orgs/{owner}/models/{model.uuid} | Patch hub model
[**update_hub_model**](HubModelsV1Api.md#update_hub_model) | **PUT** /api/v1/orgs/{owner}/models/{model.uuid} | Update hub model


# **create_hub_model**
> V1HubModel create_hub_model(owner, body)

Create hub model

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1HubModel() # V1HubModel | Model body

    try:
        # Create hub model
        api_response = api_instance.create_hub_model(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->create_hub_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1HubModel**](V1HubModel.md)| Model body | 

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_hub_model**
> delete_hub_model(owner, uuid)

Delete hub model

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

    try:
        # Delete hub model
        api_instance.delete_hub_model(owner, uuid)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->delete_hub_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_hub_model**
> V1HubModel get_hub_model(owner, uuid)

Get hub model

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

    try:
        # Get hub model
        api_response = api_instance.get_hub_model(owner, uuid)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->get_hub_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_hub_model_names**
> V1ListHubModelsResponse list_hub_model_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub model names

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

    try:
        # List hub model names
        api_response = api_instance.list_hub_model_names(owner, offset=offset, limit=limit, sort=sort, query=query)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->list_hub_model_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListHubModelsResponse**](V1ListHubModelsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_hub_models**
> V1ListHubModelsResponse list_hub_models(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub models

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

    try:
        # List hub models
        api_response = api_instance.list_hub_models(owner, offset=offset, limit=limit, sort=sort, query=query)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->list_hub_models: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListHubModelsResponse**](V1ListHubModelsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_hub_model**
> V1HubModel patch_hub_model(owner, model_uuid, body)

Patch hub model

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
model_uuid = 'model_uuid_example' # str | UUID
body = polyaxon_sdk.V1HubModel() # V1HubModel | Model body

    try:
        # Patch hub model
        api_response = api_instance.patch_hub_model(owner, model_uuid, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->patch_hub_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **model_uuid** | **str**| UUID | 
 **body** | [**V1HubModel**](V1HubModel.md)| Model body | 

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_hub_model**
> V1HubModel update_hub_model(owner, model_uuid, body)

Update hub model

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.HubModelsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
model_uuid = 'model_uuid_example' # str | UUID
body = polyaxon_sdk.V1HubModel() # V1HubModel | Model body

    try:
        # Update hub model
        api_response = api_instance.update_hub_model(owner, model_uuid, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HubModelsV1Api->update_hub_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **model_uuid** | **str**| UUID | 
 **body** | [**V1HubModel**](V1HubModel.md)| Model body | 

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

