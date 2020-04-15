# PolyaxonSdk.ArtifactsStoresV1Api

Polyaxon&#39;s typescript client

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**uploadArtifact**](ArtifactsStoresV1Api.md#uploadArtifact) | **POST** /api/v1/catalogs/{owner}/artifacts/{uuid}/upload | Upload artifact to a store



## uploadArtifact

> uploadArtifact(owner, uuid, uploadfile, opts)

Upload artifact to a store

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let uuid = "uuid_example"; // String | Unique integer identifier of the entity
let uploadfile = "/path/to/file"; // File | The file to upload.
let opts = {
  'path': "path_example", // String | File path query params.
  'overwrite': true // Boolean | File path query params.
};
apiInstance.uploadArtifact(owner, uuid, uploadfile, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
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

