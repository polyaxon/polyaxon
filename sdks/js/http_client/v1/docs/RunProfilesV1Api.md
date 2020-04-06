# PolyaxonSdk.RunProfilesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**runProfilesV1CreateRunProfile**](RunProfilesV1Api.md#runProfilesV1CreateRunProfile) | **POST** /api/v1/orgs/{owner}/run_profiles | Create hub component
[**runProfilesV1DeleteRunProfile**](RunProfilesV1Api.md#runProfilesV1DeleteRunProfile) | **DELETE** /api/v1/orgs/{owner}/run_profiles/{uuid} | Delete hub component
[**runProfilesV1GetRunProfile**](RunProfilesV1Api.md#runProfilesV1GetRunProfile) | **GET** /api/v1/orgs/{owner}/run_profiles/{uuid} | Get hub component
[**runProfilesV1ListRunProfileNames**](RunProfilesV1Api.md#runProfilesV1ListRunProfileNames) | **GET** /api/v1/orgs/{owner}/run_profiles/names | List hub component names
[**runProfilesV1ListRunProfiles**](RunProfilesV1Api.md#runProfilesV1ListRunProfiles) | **GET** /api/v1/orgs/{owner}/run_profiles | List hub components
[**runProfilesV1PatchRunProfile**](RunProfilesV1Api.md#runProfilesV1PatchRunProfile) | **PATCH** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Patch hub component
[**runProfilesV1UpdateRunProfile**](RunProfilesV1Api.md#runProfilesV1UpdateRunProfile) | **PUT** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Update hub component


<a name="runProfilesV1CreateRunProfile"></a>
# **runProfilesV1CreateRunProfile**
> V1RunProfile runProfilesV1CreateRunProfile(owner, body)

Create hub component

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1RunProfile(); // V1RunProfile | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1CreateRunProfile(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1DeleteRunProfile"></a>
# **runProfilesV1DeleteRunProfile**
> runProfilesV1DeleteRunProfile(owner, uuid)

Delete hub component

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runProfilesV1DeleteRunProfile(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1GetRunProfile"></a>
# **runProfilesV1GetRunProfile**
> V1RunProfile runProfilesV1GetRunProfile(owner, uuid)

Get hub component

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1GetRunProfile(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1ListRunProfileNames"></a>
# **runProfilesV1ListRunProfileNames**
> V1ListRunProfilesResponse runProfilesV1ListRunProfileNames(owner, opts)

List hub component names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1ListRunProfileNames(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1ListRunProfiles"></a>
# **runProfilesV1ListRunProfiles**
> V1ListRunProfilesResponse runProfilesV1ListRunProfiles(owner, opts)

List hub components

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1ListRunProfiles(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1PatchRunProfile"></a>
# **runProfilesV1PatchRunProfile**
> V1RunProfile runProfilesV1PatchRunProfile(owner, run_profile_uuid, body)

Patch hub component

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var run_profile_uuid = "run_profile_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1RunProfile(); // V1RunProfile | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1PatchRunProfile(owner, run_profile_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **run_profile_uuid** | **String**| UUID | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1UpdateRunProfile"></a>
# **runProfilesV1UpdateRunProfile**
> V1RunProfile runProfilesV1UpdateRunProfile(owner, run_profile_uuid, body)

Update hub component

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunProfilesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var run_profile_uuid = "run_profile_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1RunProfile(); // V1RunProfile | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runProfilesV1UpdateRunProfile(owner, run_profile_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **run_profile_uuid** | **String**| UUID | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

