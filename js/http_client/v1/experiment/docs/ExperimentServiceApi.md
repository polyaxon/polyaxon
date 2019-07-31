# ExperimentService.ExperimentServiceApi

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
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Bookmark experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Create new experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new ExperimentService.V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 


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

<a name="createExperimentStatus"></a>
# **createExperimentStatus**
> V1ExperimentStatus createExperimentStatus(owner, project, id, body)

Create new experiment status

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Delete experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Delete experiments

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Get experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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
> Object getExperimentCodeRef(owner, project, id)

Get experiment code ref

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.greateExperimentCodeRef(owner, project, id, body, callback);
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
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

List bookmarked experiments

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

List experiment statuses

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

List experiments

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Restart experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Restore experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Resume experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Start experiment tensorboard

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Stop experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var id = "id_example"; // String | Unique integer identifier of the entity

var body = new ExperimentService.V1OwnedEntityIdRequest(); // V1OwnedEntityIdRequest | 


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

Stop experiment tensorboard

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Stop experiments

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new ExperimentService.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


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

UnBookmark experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

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

Update experiment

### Example
```javascript
var ExperimentService = require('experiment_service');

var apiInstance = new ExperimentService.ExperimentServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var experiment_id = "experiment_id_example"; // String | Unique integer identifier

var body = new ExperimentService.V1ExperimentBodyRequest(); // V1ExperimentBodyRequest | 


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

