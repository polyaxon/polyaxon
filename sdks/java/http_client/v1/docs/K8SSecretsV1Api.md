# K8SSecretsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8SSecrets**](K8SSecretsV1Api.md#createK8SSecrets) | **POST** /api/v1/{owner}/k8s_secrets | List runs
[**deleteK8SSecret**](K8SSecretsV1Api.md#deleteK8SSecret) | **DELETE** /api/v1/{owner}/k8s_secrets/{uuid} | Patch run
[**getK8SSecret**](K8SSecretsV1Api.md#getK8SSecret) | **GET** /api/v1/{owner}/k8s_secrets/{uuid} | Create new run
[**listK8SSecretNames**](K8SSecretsV1Api.md#listK8SSecretNames) | **GET** /api/v1/{owner}/k8s_secrets/names | List bookmarked runs for user
[**listK8SSecrets**](K8SSecretsV1Api.md#listK8SSecrets) | **GET** /api/v1/{owner}/k8s_secrets | List archived runs for user
[**patchK8SSecret**](K8SSecretsV1Api.md#patchK8SSecret) | **PATCH** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Update run
[**updateK8SSecret**](K8SSecretsV1Api.md#updateK8SSecret) | **PUT** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Get run


<a name="createK8SSecrets"></a>
# **createK8SSecrets**
> V1K8SResource createK8SSecrets(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.createK8SSecrets(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#createK8SSecrets");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8SSecret"></a>
# **deleteK8SSecret**
> deleteK8SSecret(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteK8SSecret(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#deleteK8SSecret");
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

<a name="getK8SSecret"></a>
# **getK8SSecret**
> V1K8SResource getK8SSecret(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1K8SResource result = apiInstance.getK8SSecret(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#getK8SSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SSecretNames"></a>
# **listK8SSecretNames**
> V1ListK8SResourcesResponse listK8SSecretNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8SResourcesResponse result = apiInstance.listK8SSecretNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#listK8SSecretNames");
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SSecrets"></a>
# **listK8SSecrets**
> V1ListK8SResourcesResponse listK8SSecrets(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8SResourcesResponse result = apiInstance.listK8SSecrets(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#listK8SSecrets");
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8SSecret"></a>
# **patchK8SSecret**
> V1K8SResource patchK8SSecret(owner, k8sResourceUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.patchK8SSecret(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#patchK8SSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8SSecret"></a>
# **updateK8SSecret**
> V1K8SResource updateK8SSecret(owner, k8sResourceUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SSecretsV1Api apiInstance = new K8SSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.updateK8SSecret(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SSecretsV1Api#updateK8SSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

