# HubComponentsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**hubComponentsV1CreateHubComponent**](HubComponentsV1Api.md#hubComponentsV1CreateHubComponent) | **POST** /api/v1/orgs/{owner}/components | Create hub model
[**hubComponentsV1DeleteHubComponent**](HubComponentsV1Api.md#hubComponentsV1DeleteHubComponent) | **DELETE** /api/v1/orgs/{owner}/components/{uuid} | Delete hub model
[**hubComponentsV1GetHubComponent**](HubComponentsV1Api.md#hubComponentsV1GetHubComponent) | **GET** /api/v1/orgs/{owner}/components/{uuid} | Get hub model
[**hubComponentsV1ListHubComponebtNames**](HubComponentsV1Api.md#hubComponentsV1ListHubComponebtNames) | **GET** /api/v1/orgs/{owner}/components/names | List hub model names
[**hubComponentsV1ListHubComponents**](HubComponentsV1Api.md#hubComponentsV1ListHubComponents) | **GET** /api/v1/orgs/{owner}/components | List hub models
[**hubComponentsV1PatchHubComponent**](HubComponentsV1Api.md#hubComponentsV1PatchHubComponent) | **PATCH** /api/v1/orgs/{owner}/components/{component.uuid} | Patch hub model
[**hubComponentsV1UpdateHubComponent**](HubComponentsV1Api.md#hubComponentsV1UpdateHubComponent) | **PUT** /api/v1/orgs/{owner}/components/{component.uuid} | Update hub model


<a name="hubComponentsV1CreateHubComponent"></a>
# **hubComponentsV1CreateHubComponent**
> V1HubComponent hubComponentsV1CreateHubComponent(owner, body)

Create hub model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1HubComponent body = new V1HubComponent(); // V1HubComponent | Component body
try {
    V1HubComponent result = apiInstance.hubComponentsV1CreateHubComponent(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1CreateHubComponent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body |

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1DeleteHubComponent"></a>
# **hubComponentsV1DeleteHubComponent**
> hubComponentsV1DeleteHubComponent(owner, uuid)

Delete hub model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.hubComponentsV1DeleteHubComponent(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1DeleteHubComponent");
    e.printStackTrace();
}
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

<a name="hubComponentsV1GetHubComponent"></a>
# **hubComponentsV1GetHubComponent**
> V1HubComponent hubComponentsV1GetHubComponent(owner, uuid)

Get hub model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1HubComponent result = apiInstance.hubComponentsV1GetHubComponent(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1GetHubComponent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1ListHubComponebtNames"></a>
# **hubComponentsV1ListHubComponebtNames**
> V1ListHubComponentsResponse hubComponentsV1ListHubComponebtNames(owner, offset, limit, sort, query)

List hub model names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHubComponentsResponse result = apiInstance.hubComponentsV1ListHubComponebtNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1ListHubComponebtNames");
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1ListHubComponents"></a>
# **hubComponentsV1ListHubComponents**
> V1ListHubComponentsResponse hubComponentsV1ListHubComponents(owner, offset, limit, sort, query)

List hub models

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHubComponentsResponse result = apiInstance.hubComponentsV1ListHubComponents(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1ListHubComponents");
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1PatchHubComponent"></a>
# **hubComponentsV1PatchHubComponent**
> V1HubComponent hubComponentsV1PatchHubComponent(owner, componentUuid, body)

Patch hub model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String componentUuid = "componentUuid_example"; // String | UUID
V1HubComponent body = new V1HubComponent(); // V1HubComponent | Component body
try {
    V1HubComponent result = apiInstance.hubComponentsV1PatchHubComponent(owner, componentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1PatchHubComponent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **componentUuid** | **String**| UUID |
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body |

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1UpdateHubComponent"></a>
# **hubComponentsV1UpdateHubComponent**
> V1HubComponent hubComponentsV1UpdateHubComponent(owner, componentUuid, body)

Update hub model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubComponentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubComponentsV1Api apiInstance = new HubComponentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String componentUuid = "componentUuid_example"; // String | UUID
V1HubComponent body = new V1HubComponent(); // V1HubComponent | Component body
try {
    V1HubComponent result = apiInstance.hubComponentsV1UpdateHubComponent(owner, componentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubComponentsV1Api#hubComponentsV1UpdateHubComponent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **componentUuid** | **String**| UUID |
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body |

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

