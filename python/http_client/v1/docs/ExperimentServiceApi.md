# polyaxon_sdk.ExperimentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_experiment**](ExperimentServiceApi.md#archive_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/archive | Restore build
[**bookmark_experiment**](ExperimentServiceApi.md#bookmark_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/bookmark | UnBookmark build
[**create_experiment**](ExperimentServiceApi.md#create_experiment) | **POST** /api/v1/{owner}/{project}/experiments | Create new build
[**create_experiment_code_ref**](ExperimentServiceApi.md#create_experiment_code_ref) | **POST** /api/v1/{entity.owner}/{entity.project}/experiments/{entity.id}/coderef | Get experiment code ref
[**create_experiment_status**](ExperimentServiceApi.md#create_experiment_status) | **POST** /api/v1/{owner}/{project}/experiments/{id}/statuses | Get job code ref
[**delete_experiment**](ExperimentServiceApi.md#delete_experiment) | **DELETE** /api/v1/{owner}/{project}/experiments/{id} | Delete build
[**delete_experiments**](ExperimentServiceApi.md#delete_experiments) | **DELETE** /api/v1/{owner}/{project}/experiments/delete | Delete builds
[**get_experiment**](ExperimentServiceApi.md#get_experiment) | **GET** /api/v1/{owner}/{project}/experiments/{id} | Get build
[**get_experiment_code_ref**](ExperimentServiceApi.md#get_experiment_code_ref) | **GET** /api/v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**list_archived_experiments**](ExperimentServiceApi.md#list_archived_experiments) | **GET** /api/v1/archives/{owner}/experiments | List archived builds
[**list_bookmarked_experiments**](ExperimentServiceApi.md#list_bookmarked_experiments) | **GET** /api/v1/bookmarks/{owner}/experiments | List bookmarked builds
[**list_experiment_statuses**](ExperimentServiceApi.md#list_experiment_statuses) | **GET** /api/v1/{owner}/{project}/experiments/{id}/statuses | Create build code ref
[**list_experiments**](ExperimentServiceApi.md#list_experiments) | **GET** /api/v1/{owner}/{project}/experiments | List builds
[**patch_experiment**](ExperimentServiceApi.md#patch_experiment) | **PATCH** /api/v1/{owner}/{project}/experiments/{experiment.id} | Patch build
[**restart_experiment**](ExperimentServiceApi.md#restart_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/restart | Restart build
[**restore_experiment**](ExperimentServiceApi.md#restore_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/restore | Bookmark build
[**resume_experiment**](ExperimentServiceApi.md#resume_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/resume | Archive build
[**start_experiment_tensorboard**](ExperimentServiceApi.md#start_experiment_tensorboard) | **POST** /api/v1/{owner}/{project}/experiments/{id}/tensorboard/start | List build statuses
[**stop_experiment**](ExperimentServiceApi.md#stop_experiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/stop | Stop build
[**stop_experiment_tensorboard**](ExperimentServiceApi.md#stop_experiment_tensorboard) | **DELETE** /api/v1/{owner}/{project}/experiments/{id}/tensorboard/stop | Create new build status
[**stop_experiments**](ExperimentServiceApi.md#stop_experiments) | **POST** /api/v1/{owner}/{project}/experiments/stop | Stop builds
[**un_bookmark_experiment**](ExperimentServiceApi.md#un_bookmark_experiment) | **DELETE** /api/v1/{owner}/{project}/experiments/{id}/unbookmark | Get build status
[**update_experiment**](ExperimentServiceApi.md#update_experiment) | **PUT** /api/v1/{owner}/{project}/experiments/{experiment.id} | Update build


# **archive_experiment**
> object archive_experiment(owner, project, id)

Restore build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Restore build
    api_response = api_instance.archive_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->archive_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_experiment**
> object bookmark_experiment(owner, project, id)

UnBookmark build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # UnBookmark build
    api_response = api_instance.bookmark_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->bookmark_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment**
> V1Experiment create_experiment(owner, project, body)

Create new build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = polyaxon_sdk.V1ExperimentBodyRequest() # V1ExperimentBodyRequest | 

try:
    # Create new build
    api_response = api_instance.create_experiment(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->create_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment_code_ref**
> V1CodeReference create_experiment_code_ref(entity_owner, entity_project, entity_id, body)

Get experiment code ref

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_id = 'entity_id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1CodeReferenceBodyRequest() # V1CodeReferenceBodyRequest | 

try:
    # Get experiment code ref
    api_response = api_instance.create_experiment_code_ref(entity_owner, entity_project, entity_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->create_experiment_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1CodeReferenceBodyRequest**](V1CodeReferenceBodyRequest.md)|  | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment_status**
> V1ExperimentStatus create_experiment_status(owner, project, id, body)

Get job code ref

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Get job code ref
    api_response = api_instance.create_experiment_status(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->create_experiment_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1ExperimentStatus**](V1ExperimentStatus.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_experiment**
> object delete_experiment(owner, project, id)

Delete build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Delete build
    api_response = api_instance.delete_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->delete_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_experiments**
> object delete_experiments(owner, project, body)

Delete builds

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Delete builds
    api_response = api_instance.delete_experiments(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->delete_experiments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment**
> V1Experiment get_experiment(owner, project, id)

Get build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get build
    api_response = api_instance.get_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->get_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_code_ref**
> V1CodeReference get_experiment_code_ref(owner, project, id)

Get experiment code ref

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get experiment code ref
    api_response = api_instance.get_experiment_code_ref(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->get_experiment_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_experiments**
> V1ListExperimentsResponse list_archived_experiments(owner)

List archived builds

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # List archived builds
    api_response = api_instance.list_archived_experiments(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->list_archived_experiments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_experiments**
> V1ListExperimentsResponse list_bookmarked_experiments(owner)

List bookmarked builds

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # List bookmarked builds
    api_response = api_instance.list_bookmarked_experiments(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->list_bookmarked_experiments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_experiment_statuses**
> V1ListExperimentStatusesResponse list_experiment_statuses(owner, project, id)

Create build code ref

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Create build code ref
    api_response = api_instance.list_experiment_statuses(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->list_experiment_statuses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1ListExperimentStatusesResponse**](V1ListExperimentStatusesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_experiments**
> V1ListExperimentsResponse list_experiments(owner, project)

List builds

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # List builds
    api_response = api_instance.list_experiments(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->list_experiments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_experiment**
> V1Experiment patch_experiment(owner, project, experiment_id, body)

Patch build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
experiment_id = 'experiment_id_example' # str | Unique integer identifier
body = polyaxon_sdk.V1ExperimentBodyRequest() # V1ExperimentBodyRequest | 

try:
    # Patch build
    api_response = api_instance.patch_experiment(owner, project, experiment_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->patch_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **experiment_id** | **str**| Unique integer identifier | 
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_experiment**
> V1Experiment restart_experiment(owner, project, id, body)

Restart build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Restart build
    api_response = api_instance.restart_experiment(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->restart_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_experiment**
> object restore_experiment(owner, project, id)

Bookmark build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Bookmark build
    api_response = api_instance.restore_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->restore_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_experiment**
> V1Experiment resume_experiment(owner, project, id, body)

Archive build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Archive build
    api_response = api_instance.resume_experiment(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->resume_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_experiment_tensorboard**
> object start_experiment_tensorboard(owner, project, id, body)

List build statuses

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # List build statuses
    api_response = api_instance.start_experiment_tensorboard(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->start_experiment_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiment**
> object stop_experiment(owner, project, id, body)

Stop build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Stop build
    api_response = api_instance.stop_experiment(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->stop_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiment_tensorboard**
> object stop_experiment_tensorboard(owner, project, id)

Create new build status

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Create new build status
    api_response = api_instance.stop_experiment_tensorboard(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->stop_experiment_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiments**
> object stop_experiments(owner, project, body)

Stop builds

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Stop builds
    api_response = api_instance.stop_experiments(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->stop_experiments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **un_bookmark_experiment**
> object un_bookmark_experiment(owner, project, id)

Get build status

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get build status
    api_response = api_instance.un_bookmark_experiment(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->un_bookmark_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_experiment**
> V1Experiment update_experiment(owner, project, experiment_id, body)

Update build

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.ExperimentServiceApi(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
experiment_id = 'experiment_id_example' # str | Unique integer identifier
body = polyaxon_sdk.V1ExperimentBodyRequest() # V1ExperimentBodyRequest | 

try:
    # Update build
    api_response = api_instance.update_experiment(owner, project, experiment_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->update_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **experiment_id** | **str**| Unique integer identifier | 
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

