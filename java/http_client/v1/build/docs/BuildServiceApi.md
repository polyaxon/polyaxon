# BuildServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveBuild**](BuildServiceApi.md#archiveBuild) | **POST** /v1/{owner}/{project}/builds/{id}/archive | Archive build
[**bookmarkBuild**](BuildServiceApi.md#bookmarkBuild) | **POST** /v1/{owner}/{project}/builds/{id}/bookmark | Bookmark build
[**createBuild**](BuildServiceApi.md#createBuild) | **POST** /v1/{owner}/{project}/builds | Create new build
[**createBuildStatus**](BuildServiceApi.md#createBuildStatus) | **POST** /v1/{owner}/{project}/builds/{id}/statuses | Create new build status
[**deleteBuild**](BuildServiceApi.md#deleteBuild) | **DELETE** /v1/{owner}/{project}/builds/{id} | Delete build
[**deleteBuilds**](BuildServiceApi.md#deleteBuilds) | **DELETE** /v1/{owner}/{project}/builds/delete | Delete builds
[**getBuild**](BuildServiceApi.md#getBuild) | **GET** /v1/{owner}/{project}/builds/{id} | Get build
[**getBuildCodeRef**](BuildServiceApi.md#getBuildCodeRef) | **GET** /v1/{owner}/{project}/builds/{id}/coderef | Get build code ref
[**greateBuildCodeRef**](BuildServiceApi.md#greateBuildCodeRef) | **POST** /v1/{owner}/{project}/builds/{id}/coderef | Get build code ref
[**listArchivedBuilds**](BuildServiceApi.md#listArchivedBuilds) | **GET** /v1/archives/{owner}/builds | List archived builds
[**listBookmarkedBuilds**](BuildServiceApi.md#listBookmarkedBuilds) | **GET** /v1/bookmarks/{owner}/builds | List bookmarked builds
[**listBuildStatuses**](BuildServiceApi.md#listBuildStatuses) | **GET** /v1/{owner}/{project}/builds/{id}/statuses | List build statuses
[**listBuilds**](BuildServiceApi.md#listBuilds) | **GET** /v1/{owner}/{project}/builds | List builds
[**restartBuild**](BuildServiceApi.md#restartBuild) | **POST** /v1/{owner}/{project}/builds/{id}/restart | Restart build
[**restoreBuild**](BuildServiceApi.md#restoreBuild) | **POST** /v1/{owner}/{project}/builds/{id}/restore | Restore build
[**stopBuild**](BuildServiceApi.md#stopBuild) | **POST** /v1/{owner}/{project}/builds/{id}/stop | Stop build
[**stopBuilds**](BuildServiceApi.md#stopBuilds) | **POST** /v1/{owner}/{project}/builds/stop | Stop builds
[**unBookmarkBuild**](BuildServiceApi.md#unBookmarkBuild) | **DELETE** /v1/{owner}/{project}/builds/{id}/unbookmark | UnBookmark build
[**updateBuild2**](BuildServiceApi.md#updateBuild2) | **PUT** /v1/{owner}/{project}/builds/{build.id} | Update build


<a name="archiveBuild"></a>
# **archiveBuild**
> Object archiveBuild(owner, project, id)

Archive build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.archiveBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#archiveBuild");
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

<a name="bookmarkBuild"></a>
# **bookmarkBuild**
> Object bookmarkBuild(owner, project, id)

Bookmark build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.bookmarkBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#bookmarkBuild");
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

<a name="createBuild"></a>
# **createBuild**
> V1Build createBuild(owner, project, body)

Create new build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1BuildBodyRequest body = new V1BuildBodyRequest(); // V1BuildBodyRequest | 
try {
    V1Build result = apiInstance.createBuild(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#createBuild");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **body** | [**V1BuildBodyRequest**](V1BuildBodyRequest.md)|  |

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createBuildStatus"></a>
# **createBuildStatus**
> V1BuildStatus createBuildStatus(owner, project, id, body)

Create new build status

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1BuildStatus result = apiInstance.createBuildStatus(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#createBuildStatus");
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

[**V1BuildStatus**](V1BuildStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteBuild"></a>
# **deleteBuild**
> Object deleteBuild(owner, project, id)

Delete build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#deleteBuild");
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

<a name="deleteBuilds"></a>
# **deleteBuilds**
> Object deleteBuilds(owner, project, body)

Delete builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.deleteBuilds(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#deleteBuilds");
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

<a name="getBuild"></a>
# **getBuild**
> V1Build getBuild(owner, project, id)

Get build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1Build result = apiInstance.getBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#getBuild");
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

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getBuildCodeRef"></a>
# **getBuildCodeRef**
> Object getBuildCodeRef(owner, project, id)

Get build code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.getBuildCodeRef(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#getBuildCodeRef");
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

<a name="greateBuildCodeRef"></a>
# **greateBuildCodeRef**
> Object greateBuildCodeRef(owner, project, id, body)

Get build code ref

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.greateBuildCodeRef(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#greateBuildCodeRef");
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

<a name="listArchivedBuilds"></a>
# **listArchivedBuilds**
> V1ListBuildsResponse listArchivedBuilds(owner)

List archived builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListBuildsResponse result = apiInstance.listArchivedBuilds(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#listArchivedBuilds");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedBuilds"></a>
# **listBookmarkedBuilds**
> V1ListBuildsResponse listBookmarkedBuilds(owner)

List bookmarked builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1ListBuildsResponse result = apiInstance.listBookmarkedBuilds(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#listBookmarkedBuilds");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBuildStatuses"></a>
# **listBuildStatuses**
> V1ListBuildStatusesResponse listBuildStatuses(owner, project, id)

List build statuses

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    V1ListBuildStatusesResponse result = apiInstance.listBuildStatuses(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#listBuildStatuses");
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

[**V1ListBuildStatusesResponse**](V1ListBuildStatusesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBuilds"></a>
# **listBuilds**
> V1ListBuildsResponse listBuilds(owner, project)

List builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    V1ListBuildsResponse result = apiInstance.listBuilds(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#listBuilds");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restartBuild"></a>
# **restartBuild**
> V1Build restartBuild(owner, project, id, body)

Restart build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    V1Build result = apiInstance.restartBuild(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#restartBuild");
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

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restoreBuild"></a>
# **restoreBuild**
> Object restoreBuild(owner, project, id)

Restore build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.restoreBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#restoreBuild");
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

<a name="stopBuild"></a>
# **stopBuild**
> Object stopBuild(owner, project, id, body)

Stop build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
V1OwnedEntityIdRequest body = new V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 
try {
    Object result = apiInstance.stopBuild(owner, project, id, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#stopBuild");
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

<a name="stopBuilds"></a>
# **stopBuilds**
> Object stopBuilds(owner, project, body)

Stop builds

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1ProjectBodyRequest body = new V1ProjectBodyRequest(); // V1ProjectBodyRequest | 
try {
    Object result = apiInstance.stopBuilds(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#stopBuilds");
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

<a name="unBookmarkBuild"></a>
# **unBookmarkBuild**
> Object unBookmarkBuild(owner, project, id)

UnBookmark build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String id = "id_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.unBookmarkBuild(owner, project, id);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#unBookmarkBuild");
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

<a name="updateBuild2"></a>
# **updateBuild2**
> V1Build updateBuild2(owner, project, buildId, body)

Update build

### Example
```java
// Import classes:
//import io.swagger.client.ApiException;
//import io.swagger.client.api.BuildServiceApi;


BuildServiceApi apiInstance = new BuildServiceApi();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String buildId = "buildId_example"; // String | Unique integer identifier
V1BuildBodyRequest body = new V1BuildBodyRequest(); // V1BuildBodyRequest | 
try {
    V1Build result = apiInstance.updateBuild2(owner, project, buildId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling BuildServiceApi#updateBuild2");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **buildId** | **String**| Unique integer identifier |
 **body** | [**V1BuildBodyRequest**](V1BuildBodyRequest.md)|  |

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

