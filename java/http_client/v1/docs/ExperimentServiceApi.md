# ExperimentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveExperiment**](ExperimentServiceApi.md#archiveExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/archive | Restore build
[**bookmarkExperiment**](ExperimentServiceApi.md#bookmarkExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/bookmark | UnBookmark build
[**createExperiment**](ExperimentServiceApi.md#createExperiment) | **POST** /api/v1/{owner}/{project}/experiments | Create new build
[**createExperimentCodeRef**](ExperimentServiceApi.md#createExperimentCodeRef) | **POST** /api/v1/{entity.owner}/{entity.project}/experiments/{entity.id}/coderef | Get experiment code ref
[**createExperimentStatus**](ExperimentServiceApi.md#createExperimentStatus) | **POST** /api/v1/{owner}/{project}/experiments/{id}/statuses | Get job code ref
[**deleteExperiment**](ExperimentServiceApi.md#deleteExperiment) | **DELETE** /api/v1/{owner}/{project}/experiments/{id} | Delete build
[**deleteExperiments**](ExperimentServiceApi.md#deleteExperiments) | **DELETE** /api/v1/{owner}/{project}/experiments/delete | Delete builds
[**getExperiment**](ExperimentServiceApi.md#getExperiment) | **GET** /api/v1/{owner}/{project}/experiments/{id} | Get build
[**getExperimentCodeRef**](ExperimentServiceApi.md#getExperimentCodeRef) | **GET** /api/v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**listArchivedExperiments**](ExperimentServiceApi.md#listArchivedExperiments) | **GET** /api/v1/archives/{owner}/experiments | List archived builds
[**listBookmarkedExperiments**](ExperimentServiceApi.md#listBookmarkedExperiments) | **GET** /api/v1/bookmarks/{owner}/experiments | List bookmarked builds
[**listExperimentStatuses**](ExperimentServiceApi.md#listExperimentStatuses) | **GET** /api/v1/{owner}/{project}/experiments/{id}/statuses | Create build code ref
[**listExperiments**](ExperimentServiceApi.md#listExperiments) | **GET** /api/v1/{owner}/{project}/experiments | List builds
[**restartExperiment**](ExperimentServiceApi.md#restartExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/restart | Restart build
[**restoreExperiment**](ExperimentServiceApi.md#restoreExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/restore | Bookmark build
[**resumeExperiment**](ExperimentServiceApi.md#resumeExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/resume | Archive build
[**startExperimentTensorboard**](ExperimentServiceApi.md#startExperimentTensorboard) | **POST** /api/v1/{owner}/{project}/experiments/{id}/tensorboard/start | List build statuses
[**stopExperiment**](ExperimentServiceApi.md#stopExperiment) | **POST** /api/v1/{owner}/{project}/experiments/{id}/stop | Stop build
[**stopExperimentTensorboard**](ExperimentServiceApi.md#stopExperimentTensorboard) | **DELETE** /api/v1/{owner}/{project}/experiments/{id}/tensorboard/stop | Create new build status
[**stopExperiments**](ExperimentServiceApi.md#stopExperiments) | **POST** /api/v1/{owner}/{project}/experiments/stop | Stop builds
[**unBookmarkExperiment**](ExperimentServiceApi.md#unBookmarkExperiment) | **DELETE** /api/v1/{owner}/{project}/experiments/{id}/unbookmark | Get build status
[**updateExperiment2**](ExperimentServiceApi.md#updateExperiment2) | **PUT** /api/v1/{owner}/{project}/experiments/{experiment.id} | Update build


<a name="archiveExperiment"></a>
# **archiveExperiment**
> Object archiveExperiment(owner, project, id)

Restore build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.archiveExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#archiveExperiment");
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

<a name="bookmarkExperiment"></a>
# **bookmarkExperiment**
> Object bookmarkExperiment(owner, project, id)

UnBookmark build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.bookmarkExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#bookmarkExperiment");
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

<a name="createExperiment"></a>
# **createExperiment**
> V1Experiment createExperiment(owner, project, body)

Create new build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1ExperimentBodyRequest body = new V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 
try {
    V1Experiment result = apiInstance.createExperiment(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#createExperiment");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  |

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createExperimentCodeRef"></a>
# **createExperimentCodeRef**
> V1CodeReference createExperimentCodeRef(entityOwner, entityProject, entityId, body)

Get experiment code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String entityOwner = "entityOwner_example"; // String | Owner of the namespace
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityId = "entityId_example"; // String | Unique integer identifier of the entity
V1CodeReferenceBodyRequest body = new V1CodeReferenceBodyRequest(); // V1CodeReferenceBodyRequest | 
try {
    V1CodeReference result = apiInstance.createExperimentCodeRef(entityOwner, entityProject, entityId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#createExperimentCodeRef");
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

<a name="createExperimentStatus"></a>
# **createExperimentStatus**
> V1ExperimentStatus createExperimentStatus(owner, project, id, body)

Get job code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1ExperimentStatus result = apiInstance.createExperimentStatus(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#createExperimentStatus");
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

[**V1ExperimentStatus**](V1ExperimentStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteExperiment"></a>
# **deleteExperiment**
> Object deleteExperiment(owner, project, id)

Delete build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#deleteExperiment");
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

<a name="deleteExperiments"></a>
# **deleteExperiments**
> Object deleteExperiments(owner, project, body)

Delete builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.deleteExperiments(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#deleteExperiments");
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

<a name="getExperiment"></a>
# **getExperiment**
> V1Experiment getExperiment(owner, project, id)

Get build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1Experiment result = apiInstance.getExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#getExperiment");
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

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getExperimentCodeRef"></a>
# **getExperimentCodeRef**
> V1CodeReference getExperimentCodeRef(owner, project, id)

Get experiment code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1CodeReference result = apiInstance.getExperimentCodeRef(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#getExperimentCodeRef");
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

<a name="listArchivedExperiments"></a>
# **listArchivedExperiments**
> V1ListExperimentsResponse listArchivedExperiments(owner)

List archived builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListExperimentsResponse result = apiInstance.listArchivedExperiments(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#listArchivedExperiments");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedExperiments"></a>
# **listBookmarkedExperiments**
> V1ListExperimentsResponse listBookmarkedExperiments(owner)

List bookmarked builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListExperimentsResponse result = apiInstance.listBookmarkedExperiments(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#listBookmarkedExperiments");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listExperimentStatuses"></a>
# **listExperimentStatuses**
> V1ListExperimentStatusesResponse listExperimentStatuses(owner, project, id)

Create build code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1ListExperimentStatusesResponse result = apiInstance.listExperimentStatuses(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#listExperimentStatuses");
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

[**V1ListExperimentStatusesResponse**](V1ListExperimentStatusesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listExperiments"></a>
# **listExperiments**
> V1ListExperimentsResponse listExperiments(owner, project)

List builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    V1ListExperimentsResponse result = apiInstance.listExperiments(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#listExperiments");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |

### Return type

[**V1ListExperimentsResponse**](V1ListExperimentsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restartExperiment"></a>
# **restartExperiment**
> V1Experiment restartExperiment(owner, project, id, body)

Restart build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1Experiment result = apiInstance.restartExperiment(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#restartExperiment");
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

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restoreExperiment"></a>
# **restoreExperiment**
> Object restoreExperiment(owner, project, id)

Bookmark build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.restoreExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#restoreExperiment");
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

<a name="resumeExperiment"></a>
# **resumeExperiment**
> V1Experiment resumeExperiment(owner, project, id, body)

Archive build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1Experiment result = apiInstance.resumeExperiment(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#resumeExperiment");
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

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="startExperimentTensorboard"></a>
# **startExperimentTensorboard**
> Object startExperimentTensorboard(owner, project, id, body)

List build statuses

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.startExperimentTensorboard(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#startExperimentTensorboard");
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

<a name="stopExperiment"></a>
# **stopExperiment**
> Object stopExperiment(owner, project, id, body)

Stop build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.stopExperiment(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#stopExperiment");
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

<a name="stopExperimentTensorboard"></a>
# **stopExperimentTensorboard**
> Object stopExperimentTensorboard(owner, project, id)

Create new build status

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.stopExperimentTensorboard(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#stopExperimentTensorboard");
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

<a name="stopExperiments"></a>
# **stopExperiments**
> Object stopExperiments(owner, project, body)

Stop builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1ProjectBodyRequest body = new V1ProjectBodyRequest(); // V1ProjectBodyRequest | 
try {
    Object result = apiInstance.stopExperiments(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#stopExperiments");
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

<a name="unBookmarkExperiment"></a>
# **unBookmarkExperiment**
> Object unBookmarkExperiment(owner, project, id)

Get build status

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.unBookmarkExperiment(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#unBookmarkExperiment");
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

<a name="updateExperiment2"></a>
# **updateExperiment2**
> V1Experiment updateExperiment2(owner, project, experimentId, body)

Update build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.ExperimentServiceApi;


ExperimentServiceApi apiInstance = new ExperimentServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String experimentId = "experimentId_example"; // String | Unique integer identifier
V1ExperimentBodyRequest body = new V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 
try {
    V1Experiment result = apiInstance.updateExperiment2(owner, project, experimentId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#updateExperiment2");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **experimentId** | **String**| Unique integer identifier |
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  |

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

