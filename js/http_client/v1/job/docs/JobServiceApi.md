# JobService.JobServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveJob**](JobServiceApi.md#archiveJob) | **POST** /v1/{owner}/{project}/jobs/{id}/archive | Archive job
[**bookmarkJob**](JobServiceApi.md#bookmarkJob) | **POST** /v1/{owner}/{project}/jobs/{id}/bookmark | Bookmark job
[**createJob**](JobServiceApi.md#createJob) | **POST** /v1/{owner}/{project}/jobs | Create new job
[**createJobStatus**](JobServiceApi.md#createJobStatus) | **POST** /v1/{owner}/{project}/jobs/{id}/statuses | Create new job status
[**deleteJob**](JobServiceApi.md#deleteJob) | **DELETE** /v1/{owner}/{project}/jobs/{id} | Delete job
[**deleteJobs**](JobServiceApi.md#deleteJobs) | **DELETE** /v1/{owner}/{project}/jobs/delete | Delete jobs
[**getJob**](JobServiceApi.md#getJob) | **GET** /v1/{owner}/{project}/jobs/{id} | Get job
[**getJobCodeRef**](JobServiceApi.md#getJobCodeRef) | **GET** /v1/{owner}/{project}/jobs/{id}/coderef | Get job code ref
[**greateJobCodeRef**](JobServiceApi.md#greateJobCodeRef) | **POST** /v1/{owner}/{project}/jobs/{id}/coderef | Get job code ref
[**listArchivedJobs**](JobServiceApi.md#listArchivedJobs) | **GET** /v1/archives/{owner}/jobs | List archived jobs
[**listBookmarkedJobs**](JobServiceApi.md#listBookmarkedJobs) | **GET** /v1/bookmarks/{owner}/jobs | List bookmarked jobs
[**listJobStatuses**](JobServiceApi.md#listJobStatuses) | **GET** /v1/{owner}/{project}/jobs/{id}/statuses | List job statuses
[**listJobs**](JobServiceApi.md#listJobs) | **GET** /v1/{owner}/{project}/jobs | List jobs
[**restartJob**](JobServiceApi.md#restartJob) | **POST** /v1/{owner}/{project}/jobs/{id}/restart | Restart job
[**restoreJob**](JobServiceApi.md#restoreJob) | **POST** /v1/{owner}/{project}/jobs/{id}/restore | Restore job
[**resumeJob**](JobServiceApi.md#resumeJob) | **POST** /v1/{owner}/{project}/jobs/{id}/resume | Resume job
[**stopJob**](JobServiceApi.md#stopJob) | **POST** /v1/{owner}/{project}/jobs/{id}/stop | Stop job
[**stopJobs**](JobServiceApi.md#stopJobs) | **POST** /v1/{owner}/{project}/jobs/stop | Stop jobs
[**unBookmarkJob**](JobServiceApi.md#unBookmarkJob) | **DELETE** /v1/{owner}/{project}/jobs/{id}/unbookmark | UnBookmark job
[**updateJob2**](JobServiceApi.md#updateJob2) | **PUT** /v1/{owner}/{project}/jobs/{job.id} | Update job


<a name="archiveJob"></a>
# **archiveJob**
> Object archiveJob(owner, project, id)

Archive job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.archiveJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="bookmarkJob"></a>
# **bookmarkJob**
> Object bookmarkJob(owner, project, id)

Bookmark job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.bookmarkJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createJob"></a>
# **createJob**
> V1Job createJob(owner, project, body)

Create new job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new JobService.V1JobBodyRequest(); // V1JobBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createJob(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **body** | [**V1JobBodyRequest**](V1JobBodyRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createJobStatus"></a>
# **createJobStatus**
> V1JobStatus createJobStatus(owner, project, id, body)

Create new job status

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createJobStatus(owner, project, id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1JobStatus**](V1JobStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteJob"></a>
# **deleteJob**
> Object deleteJob(owner, project, id)

Delete job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteJobs"></a>
# **deleteJobs**
> Object deleteJobs(owner, project, body)

Delete jobs

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteJobs(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getJob"></a>
# **getJob**
> V1Job getJob(owner, project, id)

Get job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getJobCodeRef"></a>
# **getJobCodeRef**
> Object getJobCodeRef(owner, project, id)

Get job code ref

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getJobCodeRef(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="greateJobCodeRef"></a>
# **greateJobCodeRef**
> Object greateJobCodeRef(owner, project, id, body)

Get job code ref

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.greateJobCodeRef(owner, project, id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArchivedJobs"></a>
# **listArchivedJobs**
> V1ListJobsResponse listArchivedJobs(owner)

List archived jobs

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArchivedJobs(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedJobs"></a>
# **listBookmarkedJobs**
> V1ListJobsResponse listBookmarkedJobs(owner)

List bookmarked jobs

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listBookmarkedJobs(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listJobStatuses"></a>
# **listJobStatuses**
> V1ListJobStatusesResponse listJobStatuses(owner, project, id)

List job statuses

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listJobStatuses(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1ListJobStatusesResponse**](V1ListJobStatusesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listJobs"></a>
# **listJobs**
> V1ListJobsResponse listJobs(owner, project)

List jobs

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listJobs(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

[**V1ListJobsResponse**](V1ListJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restartJob"></a>
# **restartJob**
> V1Job restartJob(owner, project, id, body)

Restart job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restartJob(owner, project, id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restoreJob"></a>
# **restoreJob**
> Object restoreJob(owner, project, id)

Restore job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restoreJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="resumeJob"></a>
# **resumeJob**
> V1Job resumeJob(owner, project, id, body)

Resume job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.resumeJob(owner, project, id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopJob"></a>
# **stopJob**
> Object stopJob(owner, project, id, body)

Stop job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new JobService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopJob(owner, project, id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopJobs"></a>
# **stopJobs**
> Object stopJobs(owner, project, body)

Stop jobs

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new JobService.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopJobs(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="unBookmarkJob"></a>
# **unBookmarkJob**
> Object unBookmarkJob(owner, project, id)

UnBookmark job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.unBookmarkJob(owner, project, id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **id** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateJob2"></a>
# **updateJob2**
> V1Job updateJob2(owner, project, job_id, body)

Update job

### Example
```javascript
var JobService = require('job_service');

var apiInstance = new JobService.JobServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var job_id = "job_id_example"; // String | Unique integer identifier

var body = new JobService.V1JobBodyRequest(); // V1JobBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateJob2(owner, project, job_id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **job_id** | **String**| Unique integer identifier | 
 **body** | [**V1JobBodyRequest**](V1JobBodyRequest.md)|  | 

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

