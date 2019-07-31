# ExperimentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveExperiment**](ExperimentServiceApi.md#archiveExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/archive | Archive experiment
[**bookmarkExperiment**](ExperimentServiceApi.md#bookmarkExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/bookmark | Bookmark experiment
[**createExperiment**](ExperimentServiceApi.md#createExperiment) | **POST** /v1/{owner}/{project}/experiments | Create new experiment
[**createExperimentStatus**](ExperimentServiceApi.md#createExperimentStatus) | **POST** /v1/{owner}/{project}/experiments/{id}/statuses | Create new experiment status
[**deleteExperiment**](ExperimentServiceApi.md#deleteExperiment) | **DELETE** /v1/{owner}/{project}/experiments/{id} | Delete experiment
[**deleteExperiments**](ExperimentServiceApi.md#deleteExperiments) | **DELETE** /v1/{owner}/{project}/experiments/delete | Delete experiments
[**getExperiment**](ExperimentServiceApi.md#getExperiment) | **GET** /v1/{owner}/{project}/experiments/{id} | Get experiment
[**getExperimentCodeRef**](ExperimentServiceApi.md#getExperimentCodeRef) | **GET** /v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**greateExperimentCodeRef**](ExperimentServiceApi.md#greateExperimentCodeRef) | **POST** /v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**listArchivedExperiments**](ExperimentServiceApi.md#listArchivedExperiments) | **GET** /v1/archives/{owner}/experiments | List archived experiments
[**listBookmarkedExperiments**](ExperimentServiceApi.md#listBookmarkedExperiments) | **GET** /v1/bookmarks/{owner}/experiments | List bookmarked experiments
[**listExperimentStatuses**](ExperimentServiceApi.md#listExperimentStatuses) | **GET** /v1/{owner}/{project}/experiments/{id}/statuses | List experiment statuses
[**listExperiments**](ExperimentServiceApi.md#listExperiments) | **GET** /v1/{owner}/{project}/experiments | List experiments
[**restartExperiment**](ExperimentServiceApi.md#restartExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restart | Restart experiment
[**restoreExperiment**](ExperimentServiceApi.md#restoreExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restore | Restore experiment
[**resumeExperiment**](ExperimentServiceApi.md#resumeExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/resume | Resume experiment
[**startExperimentTensorboard**](ExperimentServiceApi.md#startExperimentTensorboard) | **POST** /v1/{owner}/{project}/experiments/{id}/tensorboard/start | Start experiment tensorboard
[**stopExperiment**](ExperimentServiceApi.md#stopExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/stop | Stop experiment
[**stopExperimentTensorboard**](ExperimentServiceApi.md#stopExperimentTensorboard) | **DELETE** /v1/{owner}/{project}/experiments/{id}/tensorboard/stop | Stop experiment tensorboard
[**stopExperiments**](ExperimentServiceApi.md#stopExperiments) | **POST** /v1/{owner}/{project}/experiments/stop | Stop experiments
[**unBookmarkExperiment**](ExperimentServiceApi.md#unBookmarkExperiment) | **DELETE** /v1/{owner}/{project}/experiments/{id}/unbookmark | UnBookmark experiment
[**updateExperiment2**](ExperimentServiceApi.md#updateExperiment2) | **PUT** /v1/{owner}/{project}/experiments/{experiment.id} | Update experiment


<a name="archiveExperiment"></a>
# **archiveExperiment**
> Object archiveExperiment(owner, project, id)

Archive experiment

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

Bookmark experiment

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

Create new experiment

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

<a name="createExperimentStatus"></a>
# **createExperimentStatus**
> V1ExperimentStatus createExperimentStatus(owner, project, id, body)

Create new experiment status

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

Delete experiment

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

Delete experiments

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

Get experiment

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
> Object getExperimentCodeRef(owner, project, id)

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
    Object result = apiInstance.getExperimentCodeRef(owner, project, id);
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

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="greateExperimentCodeRef"></a>
# **greateExperimentCodeRef**
> Object greateExperimentCodeRef(owner, project, id, body)

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
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.greateExperimentCodeRef(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ExperimentServiceApi#greateExperimentCodeRef");
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

<a name="listArchivedExperiments"></a>
# **listArchivedExperiments**
> V1ListExperimentsResponse listArchivedExperiments(owner)

List archived experiments

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

List bookmarked experiments

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

List experiment statuses

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

List experiments

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

Restart experiment

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

Restore experiment

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

Resume experiment

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

Start experiment tensorboard

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

Stop experiment

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

Stop experiment tensorboard

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

Stop experiments

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

UnBookmark experiment

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

Update experiment

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

