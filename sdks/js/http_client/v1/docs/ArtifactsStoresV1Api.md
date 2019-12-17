# PolyaxonSdk.ArtifactsStoresV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**uploadArtifact**](ArtifactsStoresV1Api.md#uploadArtifact) | **POST** /api/v1/catalogs/{owner}/artifacts_stores/{uuid}/upload | Upload artifact to a store


<a name="uploadArtifact"></a>
# **uploadArtifact**
> uploadArtifact(owner, uuid, uploadfile, opts)

Upload artifact to a store

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var uploadfile = "/path/to/file.txt"; // File | The file to upload.

var opts = { 
  'path': "path_example", // String | File path query params.
  'overwrite': true // Boolean | File path query params.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.uploadArtifact(owner, uuid, uploadfile, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **uploadfile** | **File**| The file to upload. | 
 **path** | **String**| File path query params. | [optional] 
 **overwrite** | **Boolean**| File path query params. | [optional] 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

