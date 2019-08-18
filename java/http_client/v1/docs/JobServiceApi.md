# JobServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveJob**](JobServiceApi.md#archiveJob) | **POST** /v1/{owner}/{project}/jobs/{id}/archive | Restore build
[**bookmarkJob**](JobServiceApi.md#bookmarkJob) | **POST** /v1/{owner}/{project}/jobs/{id}/bookmark | UnBookmark build
[**createJob**](JobServiceApi.md#createJob) | **POST** /v1/{owner}/{project}/jobs | Create new build
[**createJobCodeRef**](JobServiceApi.md#createJobCodeRef) | **POST** /v1/{entity.owner}/{entity.project}/jobs/{entity.id}/coderef | Get job code ref
[**createJobStatus**](JobServiceApi.md#createJobStatus) | **POST** /v1/{owner}/{project}/jobs/{id}/statuses | Get build code ref
[**deleteJob**](JobServiceApi.md#deleteJob) | **DELETE** /v1/{owner}/{project}/jobs/{id} | Delete build
[**deleteJobs**](JobServiceApi.md#deleteJobs) | **DELETE** /v1/{owner}/{project}/jobs/delete | Delete builds
[**getJob**](JobServiceApi.md#getJob) | **GET** /v1/{owner}/{project}/jobs/{id} | Get build
[**getJobCodeRef**](JobServiceApi.md#getJobCodeRef) | **GET** /v1/{owner}/{project}/jobs/{id}/coderef | Create build code ref
[**listArchivedJobs**](JobServiceApi.md#listArchivedJobs) | **GET** /v1/archives/{owner}/jobs | List archived builds
[**listBookmarkedJobs**](JobServiceApi.md#listBookmarkedJobs) | **GET** /v1/bookmarks/{owner}/jobs | List bookmarked builds
[**listJobStatuses**](JobServiceApi.md#listJobStatuses) | **GET** /v1/{owner}/{project}/jobs/{id}/statuses | Create new build status
[**listJobs**](JobServiceApi.md#listJobs) | **GET** /v1/{owner}/{project}/jobs | List builds
[**restartJob**](JobServiceApi.md#restartJob) | **POST** /v1/{owner}/{project}/jobs/{id}/restart | Restart build
[**restoreJob**](JobServiceApi.md#restoreJob) | **POST** /v1/{owner}/{project}/jobs/{id}/restore | Bookmark build
[**resumeJob**](JobServiceApi.md#resumeJob) | **POST** /v1/{owner}/{project}/jobs/{id}/resume | Archive build
[**stopJob**](JobServiceApi.md#stopJob) | **POST** /v1/{owner}/{project}/jobs/{id}/stop | Stop build
[**stopJobs**](JobServiceApi.md#stopJobs) | **POST** /v1/{owner}/{project}/jobs/stop | Stop builds
[**unBookmarkJob**](JobServiceApi.md#unBookmarkJob) | **DELETE** /v1/{owner}/{project}/jobs/{id}/unbookmark | Get build status
[**updateJob2**](JobServiceApi.md#updateJob2) | **PUT** /v1/{owner}/{project}/jobs/{job.id} | Update build


<a name="archiveJob"></a>
# **archiveJob**
> Object archiveJob(owner, project, id)

Restore build

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

UnBookmark build

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

Create new build

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

<a name="createJobCodeRef"></a>
# **createJobCodeRef**
> V1CodeReference createJobCodeRef(entityOwner, entityProject, entityId, body)

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
    V1CodeReference result = apiInstance.createJobCodeRef(entityOwner, entityProject, entityId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobServiceApi#createJobCodeRef");
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

<a name="createJobStatus"></a>
# **createJobStatus**
> V1JobStatus createJobStatus(owner, project, id, body)

Get build code ref

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

Delete build

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

Delete builds

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

Get build

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

Create build code ref

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

<a name="listArchivedJobs"></a>
# **listArchivedJobs**
> V1ListJobsResponse listArchivedJobs(owner)

List archived builds

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

List bookmarked builds

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

Create new build status

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

List builds

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

Restart build

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

Bookmark build

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

Archive build

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

Stop build

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

Stop builds

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

Get build status

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

Update build

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

