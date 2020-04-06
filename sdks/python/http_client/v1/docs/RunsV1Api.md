# polyaxon_sdk.RunsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_run_artifact**](RunsV1Api.md#get_run_artifact) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifact | Get run artifact
[**get_run_artifacts**](RunsV1Api.md#get_run_artifacts) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts | Get run artifacts
[**runs_v1_archive_run**](RunsV1Api.md#runs_v1_archive_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**runs_v1_bookmark_run**](RunsV1Api.md#runs_v1_bookmark_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**runs_v1_bookmark_runs**](RunsV1Api.md#runs_v1_bookmark_runs) | **POST** /api/v1/{owner}/{project}/runs/bookmark | Bookmark runs
[**runs_v1_collect_run_logs**](RunsV1Api.md#runs_v1_collect_run_logs) | **POST** /streams/v1/{namespace}/_internal/{owner}/{project}/runs/{uuid}/logs | Collect run logs
[**runs_v1_copy_run**](RunsV1Api.md#runs_v1_copy_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/copy | Restart run with copy
[**runs_v1_create_run**](RunsV1Api.md#runs_v1_create_run) | **POST** /api/v1/{owner}/{project}/runs | Create new run
[**runs_v1_create_run_artifacts_lineage**](RunsV1Api.md#runs_v1_create_run_artifacts_lineage) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Create bulk run run artifacts lineage
[**runs_v1_create_run_status**](RunsV1Api.md#runs_v1_create_run_status) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**runs_v1_delete_run**](RunsV1Api.md#runs_v1_delete_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**runs_v1_delete_run_artifact_lineage**](RunsV1Api.md#runs_v1_delete_run_artifact_lineage) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Delete run artifact lineage
[**runs_v1_delete_runs**](RunsV1Api.md#runs_v1_delete_runs) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**runs_v1_get_multi_run_events**](RunsV1Api.md#runs_v1_get_multi_run_events) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/multi/events/{kind} | Get multi runs events
[**runs_v1_get_run**](RunsV1Api.md#runs_v1_get_run) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**runs_v1_get_run_artifact_lineage**](RunsV1Api.md#runs_v1_get_run_artifact_lineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Get run artifacts lineage
[**runs_v1_get_run_artifacts_lineage**](RunsV1Api.md#runs_v1_get_run_artifacts_lineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Get run artifacts lineage
[**runs_v1_get_run_artifacts_lineage_names**](RunsV1Api.md#runs_v1_get_run_artifacts_lineage_names) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/names | Get run artifacts lineage names
[**runs_v1_get_run_artifacts_tree**](RunsV1Api.md#runs_v1_get_run_artifacts_tree) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts/tree | Get run artifacts tree
[**runs_v1_get_run_events**](RunsV1Api.md#runs_v1_get_run_events) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/events/{kind} | Get run events
[**runs_v1_get_run_logs**](RunsV1Api.md#runs_v1_get_run_logs) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/logs | Get run logs
[**runs_v1_get_run_namespace**](RunsV1Api.md#runs_v1_get_run_namespace) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/namespace | Get Run namespace
[**runs_v1_get_run_resources**](RunsV1Api.md#runs_v1_get_run_resources) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/resources | Get run resources events
[**runs_v1_get_run_settings**](RunsV1Api.md#runs_v1_get_run_settings) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/settings | Get Run settings
[**runs_v1_get_run_statuses**](RunsV1Api.md#runs_v1_get_run_statuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**runs_v1_get_runs_artifacts_lineage**](RunsV1Api.md#runs_v1_get_runs_artifacts_lineage) | **GET** /api/v1/{owner}/{project}/runs/artifacts_lineage | Get runs artifacts lineage
[**runs_v1_impersonate_token**](RunsV1Api.md#runs_v1_impersonate_token) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/impersonate | Impersonate run token
[**runs_v1_invalidate_run**](RunsV1Api.md#runs_v1_invalidate_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Invalidate run
[**runs_v1_invalidate_runs**](RunsV1Api.md#runs_v1_invalidate_runs) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**runs_v1_list_archived_runs**](RunsV1Api.md#runs_v1_list_archived_runs) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**runs_v1_list_bookmarked_runs**](RunsV1Api.md#runs_v1_list_bookmarked_runs) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**runs_v1_list_runs**](RunsV1Api.md#runs_v1_list_runs) | **GET** /api/v1/{owner}/{project}/runs | List runs
[**runs_v1_list_runs_io**](RunsV1Api.md#runs_v1_list_runs_io) | **GET** /api/v1/{owner}/{project}/runs/io | List runs io
[**runs_v1_notify_run_status**](RunsV1Api.md#runs_v1_notify_run_status) | **POST** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/notify | Notify run status
[**runs_v1_patch_run**](RunsV1Api.md#runs_v1_patch_run) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**runs_v1_restart_run**](RunsV1Api.md#runs_v1_restart_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/restart | Restart run
[**runs_v1_restore_run**](RunsV1Api.md#runs_v1_restore_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**runs_v1_resume_run**](RunsV1Api.md#runs_v1_resume_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/resume | Resume run
[**runs_v1_start_run_tensorboard**](RunsV1Api.md#runs_v1_start_run_tensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**runs_v1_stop_run**](RunsV1Api.md#runs_v1_stop_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**runs_v1_stop_run_tensorboard**](RunsV1Api.md#runs_v1_stop_run_tensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**runs_v1_stop_runs**](RunsV1Api.md#runs_v1_stop_runs) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**runs_v1_tag_runs**](RunsV1Api.md#runs_v1_tag_runs) | **POST** /api/v1/{owner}/{project}/runs/tag | Tag runs
[**runs_v1_unbookmark_run**](RunsV1Api.md#runs_v1_unbookmark_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**runs_v1_update_run**](RunsV1Api.md#runs_v1_update_run) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run
[**upload_run_artifact**](RunsV1Api.md#upload_run_artifact) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts/upload | Upload an artifact file to a store via run access
[**upload_run_logs**](RunsV1Api.md#upload_run_logs) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/logs/upload | Upload a logs file to a store via run access


# **get_run_artifact**
> str get_run_artifact(namespace, owner, project, uuid, path=path, stream=stream)

Get run artifact

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
path = 'path_example' # str | Artifact filepath. (optional)
stream = true # bool | Whether to stream the file. (optional)

try:
    # Get run artifact
    api_response = api_instance.get_run_artifact(namespace, owner, project, uuid, path=path, stream=stream)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_artifact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **path** | **str**| Artifact filepath. | [optional] 
 **stream** | **bool**| Whether to stream the file. | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_artifacts**
> str get_run_artifacts(namespace, owner, project, uuid, path=path)

Get run artifacts

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
path = 'path_example' # str | Artifact filepath. (optional)

try:
    # Get run artifacts
    api_response = api_instance.get_run_artifacts(namespace, owner, project, uuid, path=path)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_artifacts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **path** | **str**| Artifact filepath. | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_archive_run**
> runs_v1_archive_run(owner, project, uuid)

Archive run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Archive run
    api_instance.runs_v1_archive_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_archive_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_bookmark_run**
> runs_v1_bookmark_run(owner, project, uuid)

Bookmark run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Bookmark run
    api_instance.runs_v1_bookmark_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_bookmark_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_bookmark_runs**
> runs_v1_bookmark_runs(owner, project, body)

Bookmark runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Bookmark runs
    api_instance.runs_v1_bookmark_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_bookmark_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_collect_run_logs**
> runs_v1_collect_run_logs(namespace, owner, project, uuid)

Collect run logs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | 
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Collect run logs
    api_instance.runs_v1_collect_run_logs(namespace, owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_collect_run_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_copy_run**
> V1Run runs_v1_copy_run(entity_owner, entity_project, entity_uuid, body)

Restart run with copy

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project
entity_uuid = 'entity_uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Restart run with copy
    api_response = api_instance.runs_v1_copy_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_copy_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project | 
 **entity_uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_create_run**
> V1Run runs_v1_create_run(owner, project, body)

Create new run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
body = polyaxon_sdk.V1OperationBody() # V1OperationBody | operation object

try:
    # Create new run
    api_response = api_instance.runs_v1_create_run(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_create_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **body** | [**V1OperationBody**](V1OperationBody.md)| operation object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_create_run_artifacts_lineage**
> runs_v1_create_run_artifacts_lineage(owner, project, uuid, body)

Create bulk run run artifacts lineage

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1RunArtifacts() # V1RunArtifacts | Run Artifacts

try:
    # Create bulk run run artifacts lineage
    api_instance.runs_v1_create_run_artifacts_lineage(owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_create_run_artifacts_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1RunArtifacts**](V1RunArtifacts.md)| Run Artifacts | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_create_run_status**
> V1Status runs_v1_create_run_status(owner, project, uuid, body)

Create new run status

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1EntityStatusBodyRequest() # V1EntityStatusBodyRequest | 

try:
    # Create new run status
    api_response = api_instance.runs_v1_create_run_status(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_create_run_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1EntityStatusBodyRequest**](V1EntityStatusBodyRequest.md)|  | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_delete_run**
> runs_v1_delete_run(owner, project, uuid)

Delete run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete run
    api_instance.runs_v1_delete_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_delete_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_delete_run_artifact_lineage**
> runs_v1_delete_run_artifact_lineage(owner, project, uuid, name, namespace=namespace)

Delete run artifact lineage

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
name = 'name_example' # str | Artifact name
namespace = 'namespace_example' # str | namespace. (optional)

try:
    # Delete run artifact lineage
    api_instance.runs_v1_delete_run_artifact_lineage(owner, project, uuid, name, namespace=namespace)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_delete_run_artifact_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **name** | **str**| Artifact name | 
 **namespace** | **str**| namespace. | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_delete_runs**
> runs_v1_delete_runs(owner, project, body)

Delete runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Delete runs
    api_instance.runs_v1_delete_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_delete_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_multi_run_events**
> V1EventsResponse runs_v1_get_multi_run_events(namespace, owner, project, kind, names=names, runs=runs, orient=orient)

Get multi runs events

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
kind = 'kind_example' # str | The artifact kind
names = 'names_example' # str | Names query param. (optional)
runs = 'runs_example' # str | Runs query param. (optional)
orient = 'orient_example' # str | Orient query param. (optional)

try:
    # Get multi runs events
    api_response = api_instance.runs_v1_get_multi_run_events(namespace, owner, project, kind, names=names, runs=runs, orient=orient)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_multi_run_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **kind** | **str**| The artifact kind | 
 **names** | **str**| Names query param. | [optional] 
 **runs** | **str**| Runs query param. | [optional] 
 **orient** | **str**| Orient query param. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run**
> V1Run runs_v1_get_run(owner, project, uuid)

Get run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get run
    api_response = api_instance.runs_v1_get_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_artifact_lineage**
> V1RunArtifact runs_v1_get_run_artifact_lineage(owner, project, uuid, name, namespace=namespace)

Get run artifacts lineage

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
name = 'name_example' # str | Artifact name
namespace = 'namespace_example' # str | namespace. (optional)

try:
    # Get run artifacts lineage
    api_response = api_instance.runs_v1_get_run_artifact_lineage(owner, project, uuid, name, namespace=namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_artifact_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **name** | **str**| Artifact name | 
 **namespace** | **str**| namespace. | [optional] 

### Return type

[**V1RunArtifact**](V1RunArtifact.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_artifacts_lineage**
> V1ListRunArtifactsResponse runs_v1_get_run_artifacts_lineage(owner, project, uuid, limit=limit, sort=sort, query=query)

Get run artifacts lineage

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # Get run artifacts lineage
    api_response = api_instance.runs_v1_get_run_artifacts_lineage(owner, project, uuid, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_artifacts_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_artifacts_lineage_names**
> V1ListRunArtifactsResponse runs_v1_get_run_artifacts_lineage_names(owner, project, uuid, limit=limit, sort=sort, query=query)

Get run artifacts lineage names

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # Get run artifacts lineage names
    api_response = api_instance.runs_v1_get_run_artifacts_lineage_names(owner, project, uuid, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_artifacts_lineage_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_artifacts_tree**
> V1ArtifactTree runs_v1_get_run_artifacts_tree(namespace, owner, project, uuid, path=path)

Get run artifacts tree

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
path = 'path_example' # str | Path query param. (optional)

try:
    # Get run artifacts tree
    api_response = api_instance.runs_v1_get_run_artifacts_tree(namespace, owner, project, uuid, path=path)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_artifacts_tree: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **path** | **str**| Path query param. | [optional] 

### Return type

[**V1ArtifactTree**](V1ArtifactTree.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_events**
> V1EventsResponse runs_v1_get_run_events(namespace, owner, project, uuid, kind, names=names, orient=orient)

Get run events

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
kind = 'kind_example' # str | The artifact kind
names = 'names_example' # str | Names query param. (optional)
orient = 'orient_example' # str | Orient query param. (optional)

try:
    # Get run events
    api_response = api_instance.runs_v1_get_run_events(namespace, owner, project, uuid, kind, names=names, orient=orient)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **kind** | **str**| The artifact kind | 
 **names** | **str**| Names query param. | [optional] 
 **orient** | **str**| Orient query param. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_logs**
> V1Logs runs_v1_get_run_logs(namespace, owner, project, uuid, last_time=last_time, last_file=last_file)

Get run logs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | 
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
last_time = '2013-10-20T19:20:30+01:00' # datetime | last time. (optional)
last_file = 'last_file_example' # str | last file. (optional)

try:
    # Get run logs
    api_response = api_instance.runs_v1_get_run_logs(namespace, owner, project, uuid, last_time=last_time, last_file=last_file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **last_time** | **datetime**| last time. | [optional] 
 **last_file** | **str**| last file. | [optional] 

### Return type

[**V1Logs**](V1Logs.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_namespace**
> V1RunSettings runs_v1_get_run_namespace(owner, project, uuid)

Get Run namespace

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get Run namespace
    api_response = api_instance.runs_v1_get_run_namespace(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_namespace: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1RunSettings**](V1RunSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_resources**
> V1EventsResponse runs_v1_get_run_resources(namespace, owner, project, uuid, names=names, tail=tail)

Get run resources events

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
names = 'names_example' # str | Names query param. (optional)
tail = true # bool | Query param flag to tail the values. (optional)

try:
    # Get run resources events
    api_response = api_instance.runs_v1_get_run_resources(namespace, owner, project, uuid, names=names, tail=tail)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **names** | **str**| Names query param. | [optional] 
 **tail** | **bool**| Query param flag to tail the values. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_settings**
> V1RunSettings runs_v1_get_run_settings(owner, project, uuid)

Get Run settings

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get Run settings
    api_response = api_instance.runs_v1_get_run_settings(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1RunSettings**](V1RunSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_run_statuses**
> V1Status runs_v1_get_run_statuses(owner, project, uuid)

Get run status

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get run status
    api_response = api_instance.runs_v1_get_run_statuses(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_run_statuses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_get_runs_artifacts_lineage**
> runs_v1_get_runs_artifacts_lineage(owner, project)

Get runs artifacts lineage

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Get runs artifacts lineage
    api_instance.runs_v1_get_runs_artifacts_lineage(owner, project)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_get_runs_artifacts_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_impersonate_token**
> V1Auth runs_v1_impersonate_token(owner, project, uuid)

Impersonate run token

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Impersonate run token
    api_response = api_instance.runs_v1_impersonate_token(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_impersonate_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_invalidate_run**
> runs_v1_invalidate_run(owner, project, uuid, body)

Invalidate run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1ProjectEntityResourceRequest() # V1ProjectEntityResourceRequest | 

try:
    # Invalidate run
    api_instance.runs_v1_invalidate_run(owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_invalidate_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_invalidate_runs**
> runs_v1_invalidate_runs(owner, project, body)

Invalidate runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Invalidate runs
    api_instance.runs_v1_invalidate_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_invalidate_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_list_archived_runs**
> V1ListRunsResponse runs_v1_list_archived_runs(user, offset=offset, limit=limit, sort=sort, query=query)

List archived runs for user

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | User
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.runs_v1_list_archived_runs(user, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_list_archived_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| User | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_list_bookmarked_runs**
> V1ListRunsResponse runs_v1_list_bookmarked_runs(user, offset=offset, limit=limit, sort=sort, query=query)

List bookmarked runs for user

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | User
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.runs_v1_list_bookmarked_runs(user, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_list_bookmarked_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| User | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_list_runs**
> V1ListRunsResponse runs_v1_list_runs(owner, project, offset=offset, limit=limit, sort=sort, query=query)

List runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List runs
    api_response = api_instance.runs_v1_list_runs(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_list_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_list_runs_io**
> V1ListRunsResponse runs_v1_list_runs_io(owner, project, offset=offset, limit=limit, sort=sort, query=query)

List runs io

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List runs io
    api_response = api_instance.runs_v1_list_runs_io(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_list_runs_io: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_notify_run_status**
> runs_v1_notify_run_status(namespace, owner, project, uuid, body)

Notify run status

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
namespace = 'namespace_example' # str | Na,espace
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
uuid = 'uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1EntityNotificationBody() # V1EntityNotificationBody | 

try:
    # Notify run status
    api_instance.runs_v1_notify_run_status(namespace, owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_notify_run_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| Na,espace | 
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1EntityNotificationBody**](V1EntityNotificationBody.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_patch_run**
> V1Run runs_v1_patch_run(owner, project, run_uuid, body)

Patch run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
run_uuid = 'run_uuid_example' # str | UUID
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Patch run
    api_response = api_instance.runs_v1_patch_run(owner, project, run_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_patch_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **run_uuid** | **str**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_restart_run**
> V1Run runs_v1_restart_run(entity_owner, entity_project, entity_uuid, body)

Restart run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project
entity_uuid = 'entity_uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Restart run
    api_response = api_instance.runs_v1_restart_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_restart_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project | 
 **entity_uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_restore_run**
> runs_v1_restore_run(owner, project, uuid)

Restore run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Restore run
    api_instance.runs_v1_restore_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_restore_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_resume_run**
> V1Run runs_v1_resume_run(entity_owner, entity_project, entity_uuid, body)

Resume run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project
entity_uuid = 'entity_uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Resume run
    api_response = api_instance.runs_v1_resume_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_resume_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project | 
 **entity_uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_start_run_tensorboard**
> runs_v1_start_run_tensorboard(owner, project, uuid, body)

Start run tensorboard

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity
body = polyaxon_sdk.V1ProjectEntityResourceRequest() # V1ProjectEntityResourceRequest | 

try:
    # Start run tensorboard
    api_instance.runs_v1_start_run_tensorboard(owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_start_run_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_stop_run**
> runs_v1_stop_run(owner, project, uuid)

Stop run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Stop run
    api_instance.runs_v1_stop_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_stop_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_stop_run_tensorboard**
> runs_v1_stop_run_tensorboard(owner, project, uuid)

Stop run tensorboard

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Stop run tensorboard
    api_instance.runs_v1_stop_run_tensorboard(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_stop_run_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_stop_runs**
> runs_v1_stop_runs(owner, project, body)

Stop runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Stop runs
    api_instance.runs_v1_stop_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_stop_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_tag_runs**
> runs_v1_tag_runs(owner, project, body)

Tag runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Tag runs
    api_instance.runs_v1_tag_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_tag_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_unbookmark_run**
> runs_v1_unbookmark_run(owner, project, uuid)

Unbookmark run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Unbookmark run
    api_instance.runs_v1_unbookmark_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_unbookmark_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **runs_v1_update_run**
> V1Run runs_v1_update_run(owner, project, run_uuid, body)

Update run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the run will be assigned
run_uuid = 'run_uuid_example' # str | UUID
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Update run
    api_response = api_instance.runs_v1_update_run(owner, project, run_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->runs_v1_update_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the run will be assigned | 
 **run_uuid** | **str**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_run_artifact**
> upload_run_artifact(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)

Upload an artifact file to a store via run access

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project having access to the store
uuid = 'uuid_example' # str | Unique integer identifier of the entity
uploadfile = '/path/to/file.txt' # file | The file to upload.
path = 'path_example' # str | File path query params. (optional)
overwrite = true # bool | File path query params. (optional)

try:
    # Upload an artifact file to a store via run access
    api_instance.upload_run_artifact(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)
except ApiException as e:
    print("Exception when calling RunsV1Api->upload_run_artifact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project having access to the store | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **uploadfile** | **file**| The file to upload. | 
 **path** | **str**| File path query params. | [optional] 
 **overwrite** | **bool**| File path query params. | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_run_logs**
> upload_run_logs(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)

Upload a logs file to a store via run access

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project having access to the store
uuid = 'uuid_example' # str | Unique integer identifier of the entity
uploadfile = '/path/to/file.txt' # file | The file to upload.
path = 'path_example' # str | File path query params. (optional)
overwrite = true # bool | File path query params. (optional)

try:
    # Upload a logs file to a store via run access
    api_instance.upload_run_logs(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)
except ApiException as e:
    print("Exception when calling RunsV1Api->upload_run_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project having access to the store | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **uploadfile** | **file**| The file to upload. | 
 **path** | **str**| File path query params. | [optional] 
 **overwrite** | **bool**| File path query params. | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

