# BuildService.BuildServiceApi

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
[**greateBuildCodeRef**](BuildServiceApi.md#greateBuildCodeRef) | **POST** /v1/{entity.owner}/{entity.project}/builds/{entity.id}/coderef | Create build code ref
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.archiveBuild(owner, project, id, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.bookmarkBuild(owner, project, id, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new BuildService.V1BuildBodyRequest(); // V1BuildBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createBuild(owner, project, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new BuildService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createBuildStatus(owner, project, id, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.deleteBuild(owner, project, id, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new BuildService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteBuilds(owner, project, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.getBuild(owner, project, id, callback);
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
> V1CodeReference getBuildCodeRef(owner, project, id)

Get build code ref

### Example
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.getBuildCodeRef(owner, project, id, callback);
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

<a name="greateBuildCodeRef"></a>
# **greateBuildCodeRef**
> V1CodeReference greateBuildCodeRef(entity_owner, entity_project, entity_id, body)

Create build code ref

### Example
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_id = "entity_id_example"; // String | Unique integer identifier of the entity

var body = new BuildService.V1CodeReferenceBodyRequest(); // V1CodeReferenceBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.greateBuildCodeRef(entity_owner, entity_project, entity_id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project where the experiement will be assigned | 
 **entity_id** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1CodeReferenceBodyRequest**](V1CodeReferenceBodyRequest.md)|  | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArchivedBuilds(owner, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listBookmarkedBuilds(owner, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.listBuildStatuses(owner, project, id, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listBuilds(owner, project, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new BuildService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restartBuild(owner, project, id, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.restoreBuild(owner, project, id, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new BuildService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopBuild(owner, project, id, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new BuildService.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopBuilds(owner, project, body, callback);
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
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

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
apiInstance.unBookmarkBuild(owner, project, id, callback);
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
> V1Build updateBuild2(owner, project, build_id, body)

Update build

### Example
```javascript
var BuildService = require('build_service');

var apiInstance = new BuildService.BuildServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var build_id = "build_id_example"; // String | Unique integer identifier

var body = new BuildService.V1BuildBodyRequest(); // V1BuildBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateBuild2(owner, project, build_id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **build_id** | **String**| Unique integer identifier | 
 **body** | [**V1BuildBodyRequest**](V1BuildBodyRequest.md)|  | 

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

