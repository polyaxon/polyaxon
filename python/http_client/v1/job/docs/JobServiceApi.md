# swagger_client.JobServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_job**](JobServiceApi.md#archive_job) | **POST** /v1/{owner}/{project}/jobs/{id}/archive | Archive job
[**bookmark_job**](JobServiceApi.md#bookmark_job) | **POST** /v1/{owner}/{project}/jobs/{id}/bookmark | Bookmark job
[**create_job**](JobServiceApi.md#create_job) | **POST** /v1/{owner}/{project}/jobs | Create new job
[**create_job_status**](JobServiceApi.md#create_job_status) | **POST** /v1/{owner}/{project}/jobs/{id}/statuses | Create new job status
[**delete_job**](JobServiceApi.md#delete_job) | **DELETE** /v1/{owner}/{project}/jobs/{id} | Delete job
[**delete_jobs**](JobServiceApi.md#delete_jobs) | **DELETE** /v1/{owner}/{project}/jobs/delete | Delete jobs
[**get_job**](JobServiceApi.md#get_job) | **GET** /v1/{owner}/{project}/jobs/{id} | Get job
[**get_job_code_ref**](JobServiceApi.md#get_job_code_ref) | **GET** /v1/{owner}/{project}/jobs/{id}/coderef | Get job code ref
[**greate_job_code_ref**](JobServiceApi.md#greate_job_code_ref) | **POST** /v1/{entity.owner}/{entity.project}/jobs/{entity.id}/coderef | Get job code ref
[**list_archived_jobs**](JobServiceApi.md#list_archived_jobs) | **GET** /v1/archives/{owner}/jobs | List archived jobs
[**list_bookmarked_jobs**](JobServiceApi.md#list_bookmarked_jobs) | **GET** /v1/bookmarks/{owner}/jobs | List bookmarked jobs
[**list_job_statuses**](JobServiceApi.md#list_job_statuses) | **GET** /v1/{owner}/{project}/jobs/{id}/statuses | List job statuses
[**list_jobs**](JobServiceApi.md#list_jobs) | **GET** /v1/{owner}/{project}/jobs | List jobs
[**restart_job**](JobServiceApi.md#restart_job) | **POST** /v1/{owner}/{project}/jobs/{id}/restart | Restart job
[**restore_job**](JobServiceApi.md#restore_job) | **POST** /v1/{owner}/{project}/jobs/{id}/restore | Restore job
[**resume_job**](JobServiceApi.md#resume_job) | **POST** /v1/{owner}/{project}/jobs/{id}/resume | Resume job
[**stop_job**](JobServiceApi.md#stop_job) | **POST** /v1/{owner}/{project}/jobs/{id}/stop | Stop job
[**stop_jobs**](JobServiceApi.md#stop_jobs) | **POST** /v1/{owner}/{project}/jobs/stop | Stop jobs
[**un_bookmark_job**](JobServiceApi.md#un_bookmark_job) | **DELETE** /v1/{owner}/{project}/jobs/{id}/unbookmark | UnBookmark job
[**update_job2**](JobServiceApi.md#update_job2) | **PUT** /v1/{owner}/{project}/jobs/{job.id} | Update job


# **archive_job**
> object archive_job(owner, project, id)

Archive job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Archive job
    api_response = api_instance.archive_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->archive_job: %s\n" % e)
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

# **bookmark_job**
> object bookmark_job(owner, project, id)

Bookmark job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Bookmark job
    api_response = api_instance.bookmark_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->bookmark_job: %s\n" % e)
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

# **create_job**
> V1Job create_job(owner, project, body)

Create new job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1JobBodyRequest() # V1JobBodyRequest | 

try:
    # Create new job
    api_response = api_instance.create_job(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->create_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1JobBodyRequest**](V1JobBodyRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_job_status**
> V1JobStatus create_job_status(owner, project, id, body)

Create new job status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Create new job status
    api_response = api_instance.create_job_status(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->create_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1JobStatus**](V1JobStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_job**
> object delete_job(owner, project, id)

Delete job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Delete job
    api_response = api_instance.delete_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->delete_job: %s\n" % e)
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

# **delete_jobs**
> object delete_jobs(owner, project, body)

Delete jobs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Delete jobs
    api_response = api_instance.delete_jobs(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->delete_jobs: %s\n" % e)
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

# **get_job**
> V1Job get_job(owner, project, id)

Get job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get job
    api_response = api_instance.get_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->get_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_code_ref**
> V1CodeReference get_job_code_ref(owner, project, id)

Get job code ref

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get job code ref
    api_response = api_instance.get_job_code_ref(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->get_job_code_ref: %s\n" % e)
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

# **greate_job_code_ref**
> V1CodeReference greate_job_code_ref(entity_owner, entity_project, entity_id, body)

Get job code ref

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_id = 'entity_id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1CodeReferenceBodyRequest() # V1CodeReferenceBodyRequest | 

try:
    # Get job code ref
    api_response = api_instance.greate_job_code_ref(entity_owner, entity_project, entity_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->greate_job_code_ref: %s\n" % e)
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

# **list_archived_jobs**
> V1ListJobsResponse list_archived_jobs(owner)

List archived jobs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List archived jobs
    api_response = api_instance.list_archived_jobs(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->list_archived_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_jobs**
> V1ListJobsResponse list_bookmarked_jobs(owner)

List bookmarked jobs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List bookmarked jobs
    api_response = api_instance.list_bookmarked_jobs(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->list_bookmarked_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_job_statuses**
> V1ListJobStatusesResponse list_job_statuses(owner, project, id)

List job statuses

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # List job statuses
    api_response = api_instance.list_job_statuses(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->list_job_statuses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1ListJobStatusesResponse**](V1ListJobStatusesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs**
> V1ListJobsResponse list_jobs(owner, project)

List jobs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # List jobs
    api_response = api_instance.list_jobs(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->list_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_job**
> V1Job restart_job(owner, project, id, body)

Restart job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Restart job
    api_response = api_instance.restart_job(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->restart_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_job**
> object restore_job(owner, project, id)

Restore job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Restore job
    api_response = api_instance.restore_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->restore_job: %s\n" % e)
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

# **resume_job**
> V1Job resume_job(owner, project, id, body)

Resume job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Resume job
    api_response = api_instance.resume_job(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->resume_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_job**
> object stop_job(owner, project, id, body)

Stop job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Stop job
    api_response = api_instance.stop_job(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->stop_job: %s\n" % e)
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

# **stop_jobs**
> object stop_jobs(owner, project, body)

Stop jobs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = swagger_client.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Stop jobs
    api_response = api_instance.stop_jobs(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->stop_jobs: %s\n" % e)
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

# **un_bookmark_job**
> object un_bookmark_job(owner, project, id)

UnBookmark job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # UnBookmark job
    api_response = api_instance.un_bookmark_job(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->un_bookmark_job: %s\n" % e)
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

# **update_job2**
> V1Job update_job2(owner, project, job_id, body)

Update job

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
job_id = 'job_id_example' # str | Unique integer identifier
body = swagger_client.V1JobBodyRequest() # V1JobBodyRequest | 

try:
    # Update job
    api_response = api_instance.update_job2(owner, project, job_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobServiceApi->update_job2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **job_id** | **str**| Unique integer identifier | 
 **body** | [**V1JobBodyRequest**](V1JobBodyRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

