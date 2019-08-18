# PolyaxonSdk.ExperimentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveExperiment**](ExperimentServiceApi.md#archiveExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/archive | Restore build
[**bookmarkExperiment**](ExperimentServiceApi.md#bookmarkExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/bookmark | UnBookmark build
[**createExperiment**](ExperimentServiceApi.md#createExperiment) | **POST** /v1/{owner}/{project}/experiments | Create new build
[**createExperimentCodeRef**](ExperimentServiceApi.md#createExperimentCodeRef) | **POST** /v1/{entity.owner}/{entity.project}/experiments/{entity.id}/coderef | Get experiment code ref
[**createExperimentStatus**](ExperimentServiceApi.md#createExperimentStatus) | **POST** /v1/{owner}/{project}/experiments/{id}/statuses | Get job code ref
[**deleteExperiment**](ExperimentServiceApi.md#deleteExperiment) | **DELETE** /v1/{owner}/{project}/experiments/{id} | Delete build
[**deleteExperiments**](ExperimentServiceApi.md#deleteExperiments) | **DELETE** /v1/{owner}/{project}/experiments/delete | Delete builds
[**getExperiment**](ExperimentServiceApi.md#getExperiment) | **GET** /v1/{owner}/{project}/experiments/{id} | Get build
[**getExperimentCodeRef**](ExperimentServiceApi.md#getExperimentCodeRef) | **GET** /v1/{owner}/{project}/experiments/{id}/coderef | Get experiment code ref
[**listArchivedExperiments**](ExperimentServiceApi.md#listArchivedExperiments) | **GET** /v1/archives/{owner}/experiments | List archived builds
[**listBookmarkedExperiments**](ExperimentServiceApi.md#listBookmarkedExperiments) | **GET** /v1/bookmarks/{owner}/experiments | List bookmarked builds
[**listExperimentStatuses**](ExperimentServiceApi.md#listExperimentStatuses) | **GET** /v1/{owner}/{project}/experiments/{id}/statuses | Create build code ref
[**listExperiments**](ExperimentServiceApi.md#listExperiments) | **GET** /v1/{owner}/{project}/experiments | List builds
[**restartExperiment**](ExperimentServiceApi.md#restartExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restart | Restart build
[**restoreExperiment**](ExperimentServiceApi.md#restoreExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/restore | Bookmark build
[**resumeExperiment**](ExperimentServiceApi.md#resumeExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/resume | Archive build
[**startExperimentTensorboard**](ExperimentServiceApi.md#startExperimentTensorboard) | **POST** /v1/{owner}/{project}/experiments/{id}/tensorboard/start | List build statuses
[**stopExperiment**](ExperimentServiceApi.md#stopExperiment) | **POST** /v1/{owner}/{project}/experiments/{id}/stop | Stop build
[**stopExperimentTensorboard**](ExperimentServiceApi.md#stopExperimentTensorboard) | **DELETE** /v1/{owner}/{project}/experiments/{id}/tensorboard/stop | Create new build status
[**stopExperiments**](ExperimentServiceApi.md#stopExperiments) | **POST** /v1/{owner}/{project}/experiments/stop | Stop builds
[**unBookmarkExperiment**](ExperimentServiceApi.md#unBookmarkExperiment) | **DELETE** /v1/{owner}/{project}/experiments/{id}/unbookmark | Get build status
[**updateExperiment2**](ExperimentServiceApi.md#updateExperiment2) | **PUT** /v1/{owner}/{project}/experiments/{experiment.id} | Update build


<a name="archiveExperiment"></a>
# **archiveExperiment**
> Object archiveExperiment(owner, project, id)

Restore build

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.archiveExperiment(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.bookmarkExperiment(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new PolyaxonSdk.V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createExperiment(owner, project, body, callback);
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
> V1CodeReference createExperimentCodeRef(entity_owner, entity_project, entity_id, body)

Get experiment code ref

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_id = "entity_id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1CodeReferenceBodyRequest(); // V1CodeReferenceBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createExperimentCodeRef(entity_owner, entity_project, entity_id, body, callback);
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

<a name="createExperimentStatus"></a>
# **createExperimentStatus**
> V1ExperimentStatus createExperimentStatus(owner, project, id, body)

Get job code ref

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createExperimentStatus(owner, project, id, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.deleteExperiment(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteExperiments(owner, project, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.getExperiment(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.getExperimentCodeRef(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArchivedExperiments(owner, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listBookmarkedExperiments(owner, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.listExperimentStatuses(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listExperiments(owner, project, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restartExperiment(owner, project, id, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.restoreExperiment(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.resumeExperiment(owner, project, id, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.startExperimentTensorboard(owner, project, id, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopExperiment(owner, project, id, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.stopExperimentTensorboard(owner, project, id, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopExperiments(owner, project, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

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
apiInstance.unBookmarkExperiment(owner, project, id, callback);
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
> V1Experiment updateExperiment2(owner, project, experiment_id, body)

Update build

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');

var apiInstance = new PolyaxonSdk.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var experiment_id = "experiment_id_example"; // String | Unique integer identifier

var body = new PolyaxonSdk.V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateExperiment2(owner, project, experiment_id, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **experiment_id** | **String**| Unique integer identifier | 
 **body** | [**V1ExperimentBodyRequest**](V1ExperimentBodyRequest.md)|  | 

### Return type

[**V1Experiment**](V1Experiment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

