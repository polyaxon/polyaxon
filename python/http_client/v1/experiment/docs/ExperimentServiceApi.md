# swagger_client.ExperimentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_experiment**](ExperimentServiceApi.md#archive_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/archive | Archive experiment
[**bookmark_experiment**](ExperimentServiceApi.md#bookmark_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/bookmark | Bookmark experiment
[**create_experiment**](ExperimentServiceApi.md#create_experiment) | **POST** /v1/{owner}/{project}/experiments | Create new experiment
[**create_experiment_status**](ExperimentServiceApi.md#create_experiment_status) | **POST** /v1/{owner}/{project}/experiments/{id}/statuses | Create new experiment status
[**delete_experiment**](ExperimentServiceApi.md#delete_experiment) | **DELETE** /v1/{owner}/{project}/experiments/{id} | Delete experiment
[**delete_experiments**](ExperimentServiceApi.md#delete_experiments) | **DELETE** /v1/{owner}/{project}/experiments/delete | Delete experiments
[**get_experiment**](ExperimentServiceApi.md#get_experiment) | **GET** /v1/{owner}/{project}/experiments/{id} | Get experiment
[**get_experiment_code_ref**](ExperimentServiceApi.md#get_experiment_code_ref) | **GET** /v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**greate_experiment_code_ref**](ExperimentServiceApi.md#greate_experiment_code_ref) | **POST** /v1/{entity.owner}/{entity.project}/experiments/{entity.id}/coderef | Get experiment code ref
[**list_archived_experiments**](ExperimentServiceApi.md#list_archived_experiments) | **GET** /v1/archives/{owner}/experiments | List archived experiments
[**list_bookmarked_experiments**](ExperimentServiceApi.md#list_bookmarked_experiments) | **GET** /v1/bookmarks/{owner}/experiments | List bookmarked experiments
[**list_experiment_statuses**](ExperimentServiceApi.md#list_experiment_statuses) | **GET** /v1/{owner}/{project}/experiments/{id}/statuses | List experiment statuses
[**list_experiments**](ExperimentServiceApi.md#list_experiments) | **GET** /v1/{owner}/{project}/experiments | List experiments
[**restart_experiment**](ExperimentServiceApi.md#restart_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restart | Restart experiment
[**restore_experiment**](ExperimentServiceApi.md#restore_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restore | Restore experiment
[**resume_experiment**](ExperimentServiceApi.md#resume_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/resume | Resume experiment
[**start_experiment_tensorboard**](ExperimentServiceApi.md#start_experiment_tensorboard) | **POST** /v1/{owner}/{project}/experiments/{id}/tensorboard/start | Start experiment tensorboard
[**stop_experiment**](ExperimentServiceApi.md#stop_experiment) | **POST** /v1/{owner}/{project}/experiments/{id}/stop | Stop experiment
[**stop_experiment_tensorboard**](ExperimentServiceApi.md#stop_experiment_tensorboard) | **DELETE** /v1/{owner}/{project}/experiments/{id}/tensorboard/stop | Stop experiment tensorboard
[**stop_experiments**](ExperimentServiceApi.md#stop_experiments) | **POST** /v1/{owner}/{project}/experiments/stop | Stop experiments
[**un_bookmark_experiment**](ExperimentServiceApi.md#un_bookmark_experiment) | **DELETE** /v1/{owner}/{project}/experiments/{id}/unbookmark | UnBookmark experiment
[**update_experiment2**](ExperimentServiceApi.md#update_experiment2) | **PUT** /v1/{owner}/{project}/experiments/{experiment.id} | Update experiment


# **archive_experiment**
> object archive_experiment(owner, project, id)

Archive experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Archive experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_experiment**
> object bookmark_experiment(owner, project, id)

Bookmark experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Bookmark experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment**
> V1Experiment create_experiment(owner, project, body)

Create new experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1ExperimentBodyRequest() # V1ExperimentBodyRequest | 

try:
    # Create new experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment_status**
> V1ExperimentStatus create_experiment_status(owner, project, id, body)

Create new experiment status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Create new experiment status
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_experiment**
> object delete_experiment(owner, project, id)

Delete experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Delete experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_experiments**
> object delete_experiments(owner, project, body)

Delete experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Delete experiments
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment**
> V1Experiment get_experiment(owner, project, id)

Get experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get experiment
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

No authorization required

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
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **greate_experiment_code_ref**
> V1CodeReference greate_experiment_code_ref(entity_owner, entity_project, entity_id, body)

Get experiment code ref

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_id = 'entity_id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1CodeReferenceBodyRequest() # V1CodeReferenceBodyRequest | 

try:
    # Get experiment code ref
    api_response = api_instance.greate_experiment_code_ref(entity_owner, entity_project, entity_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->greate_experiment_code_ref: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_experiments**
> V1ListExperimentsResponse list_archived_experiments(owner)

List archived experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List archived experiments
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_experiments**
> V1ListExperimentsResponse list_bookmarked_experiments(owner)

List bookmarked experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List bookmarked experiments
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_experiment_statuses**
> V1ListExperimentStatusesResponse list_experiment_statuses(owner, project, id)

List experiment statuses

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # List experiment statuses
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_experiments**
> V1ListExperimentsResponse list_experiments(owner, project)

List experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # List experiments
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_experiment**
> V1Experiment restart_experiment(owner, project, id, body)

Restart experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Restart experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_experiment**
> object restore_experiment(owner, project, id)

Restore experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Restore experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_experiment**
> V1Experiment resume_experiment(owner, project, id, body)

Resume experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Resume experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_experiment_tensorboard**
> object start_experiment_tensorboard(owner, project, id, body)

Start experiment tensorboard

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Start experiment tensorboard
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiment**
> object stop_experiment(owner, project, id, body)

Stop experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Stop experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiment_tensorboard**
> object stop_experiment_tensorboard(owner, project, id)

Stop experiment tensorboard

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Stop experiment tensorboard
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_experiments**
> object stop_experiments(owner, project, body)

Stop experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = swagger_client.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Stop experiments
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **un_bookmark_experiment**
> object un_bookmark_experiment(owner, project, id)

UnBookmark experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # UnBookmark experiment
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_experiment2**
> V1Experiment update_experiment2(owner, project, experiment_id, body)

Update experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
experiment_id = 'experiment_id_example' # str | Unique integer identifier
body = swagger_client.V1ExperimentBodyRequest() # V1ExperimentBodyRequest | 

try:
    # Update experiment
    api_response = api_instance.update_experiment2(owner, project, experiment_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentServiceApi->update_experiment2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

