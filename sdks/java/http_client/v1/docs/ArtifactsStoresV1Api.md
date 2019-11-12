# ArtifactsStoresV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createArtifactsStore**](ArtifactsStoresV1Api.md#createArtifactsStore) | **POST** /api/v1/{owner}/artifacts_stores | List runs
[**deleteArtifactsStore**](ArtifactsStoresV1Api.md#deleteArtifactsStore) | **DELETE** /api/v1/{owner}/artifacts_stores/{uuid} | Patch run
[**getArtifactsStore**](ArtifactsStoresV1Api.md#getArtifactsStore) | **GET** /api/v1/{owner}/artifacts_stores/{uuid} | Create new run
[**listArtifactsStoreNames**](ArtifactsStoresV1Api.md#listArtifactsStoreNames) | **GET** /api/v1/{owner}/artifacts_stores/names | List bookmarked runs for user
[**listArtifactsStores**](ArtifactsStoresV1Api.md#listArtifactsStores) | **GET** /api/v1/{owner}/artifacts_stores | List archived runs for user
[**patchArtifactsStore**](ArtifactsStoresV1Api.md#patchArtifactsStore) | **PATCH** /api/v1/{owner}/artifacts_stores/{artifact_store.uuid} | Update run
[**updateArtifactsStore**](ArtifactsStoresV1Api.md#updateArtifactsStore) | **PUT** /api/v1/{owner}/artifacts_stores/{artifact_store.uuid} | Get run
[**uploadArtifact**](ArtifactsStoresV1Api.md#uploadArtifact) | **POST** /api/v1/catalogs/{owner}/artifacts_stores/{uuid}/upload | Upload artifact to a store


<a name="createArtifactsStore"></a>
# **createArtifactsStore**
> V1ArtifactsStore createArtifactsStore(owner, body)

List runs

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
V1ArtifactsStore body = new V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body
try {
    V1ArtifactsStore result = apiInstance.createArtifactsStore(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#createArtifactsStore");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body |

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteArtifactsStore"></a>
# **deleteArtifactsStore**
> deleteArtifactsStore(owner, uuid)

Patch run

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
try {
    apiInstance.deleteArtifactsStore(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#deleteArtifactsStore");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getArtifactsStore"></a>
# **getArtifactsStore**
> V1ArtifactsStore getArtifactsStore(owner, uuid)

Create new run

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
try {
    V1ArtifactsStore result = apiInstance.getArtifactsStore(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#getArtifactsStore");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArtifactsStoreNames"></a>
# **listArtifactsStoreNames**
> V1ListArtifactsStoresResponse listArtifactsStoreNames(owner, offset, limit, sort, query)

List bookmarked runs for user

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListArtifactsStoresResponse result = apiInstance.listArtifactsStoreNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#listArtifactsStoreNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListArtifactsStoresResponse**](V1ListArtifactsStoresResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArtifactsStores"></a>
# **listArtifactsStores**
> V1ListArtifactsStoresResponse listArtifactsStores(owner, offset, limit, sort, query)

List archived runs for user

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListArtifactsStoresResponse result = apiInstance.listArtifactsStores(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#listArtifactsStores");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListArtifactsStoresResponse**](V1ListArtifactsStoresResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchArtifactsStore"></a>
# **patchArtifactsStore**
> V1ArtifactsStore patchArtifactsStore(owner, artifactStoreUuid, body)

Update run

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
String artifactStoreUuid = "artifactStoreUuid_example"; // String | UUID
V1ArtifactsStore body = new V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body
try {
    V1ArtifactsStore result = apiInstance.patchArtifactsStore(owner, artifactStoreUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#patchArtifactsStore");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **artifactStoreUuid** | **String**| UUID |
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body |

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateArtifactsStore"></a>
# **updateArtifactsStore**
> V1ArtifactsStore updateArtifactsStore(owner, artifactStoreUuid, body)

Get run

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
String artifactStoreUuid = "artifactStoreUuid_example"; // String | UUID
V1ArtifactsStore body = new V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body
try {
    V1ArtifactsStore result = apiInstance.updateArtifactsStore(owner, artifactStoreUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ArtifactsStoresV1Api#updateArtifactsStore");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **artifactStoreUuid** | **String**| UUID |
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body |

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

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

