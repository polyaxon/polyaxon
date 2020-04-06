# ConnectionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createConnection**](ConnectionsV1Api.md#createConnection) | **POST** /api/v1/orgs/{owner}/connections | Create connection
[**deleteConnection**](ConnectionsV1Api.md#deleteConnection) | **DELETE** /api/v1/orgs/{owner}/connections/{uuid} | Delete connection
[**getConnection**](ConnectionsV1Api.md#getConnection) | **GET** /api/v1/orgs/{owner}/connections/{uuid} | Get connection
[**listConnectionNames**](ConnectionsV1Api.md#listConnectionNames) | **GET** /api/v1/orgs/{owner}/connections/names | List connections names
[**listConnections**](ConnectionsV1Api.md#listConnections) | **GET** /api/v1/orgs/{owner}/connections | List connections
[**patchConnection**](ConnectionsV1Api.md#patchConnection) | **PATCH** /api/v1/orgs/{owner}/connections/{connection.uuid} | Patch connection
[**updateConnection**](ConnectionsV1Api.md#updateConnection) | **PUT** /api/v1/orgs/{owner}/connections/{connection.uuid} | Update connection


<a name="createConnection"></a>
# **createConnection**
> V1ConnectionResponse createConnection(owner, body)

Create connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.createConnection(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#createConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteConnection"></a>
# **deleteConnection**
> deleteConnection(owner, uuid)

Delete connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.deleteConnection(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#deleteConnection");
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

<a name="getConnection"></a>
# **getConnection**
> V1ConnectionResponse getConnection(owner, uuid)

Get connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1ConnectionResponse result = apiInstance.getConnection(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#getConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listConnectionNames"></a>
# **listConnectionNames**
> V1ListConnectionsResponse listConnectionNames(owner, offset, limit, sort, query)

List connections names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConnectionsResponse result = apiInstance.listConnectionNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#listConnectionNames");
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listConnections"></a>
# **listConnections**
> V1ListConnectionsResponse listConnections(owner, offset, limit, sort, query)

List connections

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConnectionsResponse result = apiInstance.listConnections(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#listConnections");
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchConnection"></a>
# **patchConnection**
> V1ConnectionResponse patchConnection(owner, connectionUuid, body)

Patch connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String connectionUuid = "connectionUuid_example"; // String | UUID
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.patchConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#patchConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateConnection"></a>
# **updateConnection**
> V1ConnectionResponse updateConnection(owner, connectionUuid, body)

Update connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String connectionUuid = "connectionUuid_example"; // String | UUID
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.updateConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#updateConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

