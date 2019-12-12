# K8sSecretsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8sSecret**](K8sSecretsV1Api.md#createK8sSecret) | **POST** /api/v1/orgs/{owner}/k8s_secrets | List runs
[**deleteK8sSecret**](K8sSecretsV1Api.md#deleteK8sSecret) | **DELETE** /api/v1/orgs/{owner}/k8s_secrets/{uuid} | Patch run
[**getK8sSecret**](K8sSecretsV1Api.md#getK8sSecret) | **GET** /api/v1/orgs/{owner}/k8s_secrets/{uuid} | Create new run
[**listK8sSecretNames**](K8sSecretsV1Api.md#listK8sSecretNames) | **GET** /api/v1/orgs/{owner}/k8s_secrets/names | List bookmarked runs for user
[**listK8sSecrets**](K8sSecretsV1Api.md#listK8sSecrets) | **GET** /api/v1/orgs/{owner}/k8s_secrets | List archived runs for user
[**patchK8sSecret**](K8sSecretsV1Api.md#patchK8sSecret) | **PATCH** /api/v1/orgs/{owner}/k8s_secrets/{k8s_resource.uuid} | Update run
[**updateK8sSecret**](K8sSecretsV1Api.md#updateK8sSecret) | **PUT** /api/v1/orgs/{owner}/k8s_secrets/{k8s_resource.uuid} | Get run


<a name="createK8sSecret"></a>
# **createK8sSecret**
> V1K8sResource createK8sSecret(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.createK8sSecret(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#createK8sSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8sSecret"></a>
# **deleteK8sSecret**
> deleteK8sSecret(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteK8sSecret(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#deleteK8sSecret");
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

<a name="getK8sSecret"></a>
# **getK8sSecret**
> V1K8sResource getK8sSecret(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1K8sResource result = apiInstance.getK8sSecret(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#getK8sSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sSecretNames"></a>
# **listK8sSecretNames**
> V1ListK8sResourcesResponse listK8sSecretNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8sResourcesResponse result = apiInstance.listK8sSecretNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#listK8sSecretNames");
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sSecrets"></a>
# **listK8sSecrets**
> V1ListK8sResourcesResponse listK8sSecrets(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8sResourcesResponse result = apiInstance.listK8sSecrets(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#listK8sSecrets");
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8sSecret"></a>
# **patchK8sSecret**
> V1K8sResource patchK8sSecret(owner, k8sResourceUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.patchK8sSecret(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#patchK8sSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8sSecret"></a>
# **updateK8sSecret**
> V1K8sResource updateK8sSecret(owner, k8sResourceUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sSecretsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sSecretsV1Api apiInstance = new K8sSecretsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.updateK8sSecret(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sSecretsV1Api#updateK8sSecret");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

