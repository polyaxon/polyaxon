# JobServiceApi

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
[**greateJobCodeRef**](JobServiceApi.md#greateJobCodeRef) | **POST** /v1/{entity.owner}/{entity.project}/jobs/{entity.id}/coderef | Get job code ref
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.archiveJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#archiveJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.bookmarkJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#bookmarkJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1JobBodyRequest body = new V1JobBodyRequest(); // V1JobBodyRequest | 
try {
    V1Job result = apiInstance.createJob(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#createJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1JobStatus result = apiInstance.createJobStatus(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#createJobStatus");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#deleteJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.deleteJobs(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#deleteJobs");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1Job result = apiInstance.getJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#getJob");
    e.printStackTrace();
}
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
> V1CodeReference getJobCodeRef(owner, project, id)

Get job code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1CodeReference result = apiInstance.getJobCodeRef(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#getJobCodeRef");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **id** | **String**| Unique integer identifier of the entity |

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="greateJobCodeRef"></a>
# **greateJobCodeRef**
> V1CodeReference greateJobCodeRef(entityOwner, entityProject, entityId, body)

Get job code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String entityOwner = "entityOwner_example"; // String | Owner of the namespace
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityId = "entityId_example"; // String | Unique integer identifier of the entity
V1CodeReferenceBodyRequest body = new V1CodeReferenceBodyRequest(); // V1CodeReferenceBodyRequest | 
try {
    V1CodeReference result = apiInstance.greateJobCodeRef(entityOwner, entityProject, entityId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#greateJobCodeRef");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project where the experiement will be assigned |
 **entityId** | **String**| Unique integer identifier of the entity |
 **body** | [**V1CodeReferenceBodyRequest**](V1CodeReferenceBodyRequest.md)|  |

### Return type

[**V1CodeReference**](V1CodeReference.md)

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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListJobsResponse result = apiInstance.listArchivedJobs(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#listArchivedJobs");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListJobsResponse result = apiInstance.listBookmarkedJobs(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#listBookmarkedJobs");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1ListJobStatusesResponse result = apiInstance.listJobStatuses(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#listJobStatuses");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    V1ListJobsResponse result = apiInstance.listJobs(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#listJobs");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1Job result = apiInstance.restartJob(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#restartJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.restoreJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#restoreJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1Job result = apiInstance.resumeJob(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#resumeJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.stopJob(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#stopJob");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1ProjectBodyRequest body = new V1ProjectBodyRequest(); // V1ProjectBodyRequest | 
try {
    Object result = apiInstance.stopJobs(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#stopJobs");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.unBookmarkJob(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#unBookmarkJob");
    e.printStackTrace();
}
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
> V1Job updateJob2(owner, project, jobId, body)

Update job

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.JobServiceApi;


JobServiceApi apiInstance = new JobServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String jobId = "jobId_example"; // String | Unique integer identifier
V1JobBodyRequest body = new V1JobBodyRequest(); // V1JobBodyRequest | 
try {
    V1Job result = apiInstance.updateJob2(owner, project, jobId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#updateJob2");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **jobId** | **String**| Unique integer identifier |
 **body** | [**V1JobBodyRequest**](V1JobBodyRequest.md)|  |

### Return type

[**V1Job**](V1Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

