# ArtifactsStoresV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**uploadArtifact**](ArtifactsStoresV1Api.md#uploadArtifact) | **POST** /api/v1/catalogs/{owner}/artifacts/{uuid}/upload | Upload artifact to a store


<a name="uploadArtifact"></a>
# **uploadArtifact**
> uploadArtifact(owner, uuid, uploadfile, path, overwrite)

Upload artifact to a store

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ArtifactsStoresV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ArtifactsStoresV1Api apiInstance = new ArtifactsStoresV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
File uploadfile = new File("/path/to/file.txt"); // File | The file to upload.
String path = "path_example"; // String | File path query params.
Boolean overwrite = true; // Boolean | File path query params.
try {
    apiInstance.uploadArtifact(owner, uuid, uploadfile, path, overwrite);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#uploadArtifact");
    e.printStackTrace();
}
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

