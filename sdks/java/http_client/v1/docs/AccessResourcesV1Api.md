# AccessResourcesV1Api
Polyaxon&#39;s typescript client

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createAccessResource**](AccessResourcesV1Api.md#createAccessResource) | **POST** /api/v1/orgs/{owner}/access_resources | Create access resource
[**deleteAccessResource**](AccessResourcesV1Api.md#deleteAccessResource) | **DELETE** /api/v1/orgs/{owner}/access_resources/{uuid} | Delete access resource
[**getAccessResource**](AccessResourcesV1Api.md#getAccessResource) | **GET** /api/v1/orgs/{owner}/access_resources/{uuid} | Get access resource
[**listAccessResourceNames**](AccessResourcesV1Api.md#listAccessResourceNames) | **GET** /api/v1/orgs/{owner}/access_resources/names | List access resource names
[**listAccessResources**](AccessResourcesV1Api.md#listAccessResources) | **GET** /api/v1/orgs/{owner}/access_resources | List access resources
[**patchAccessResource**](AccessResourcesV1Api.md#patchAccessResource) | **PATCH** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Patch access resource
[**updateAccessResource**](AccessResourcesV1Api.md#updateAccessResource) | **PUT** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Update access resource


<a name="createAccessResource"></a>
# **createAccessResource**
> V1AccessResource createAccessResource(owner, body)

Create access resource

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
    try {
      V1AccessResource result = apiInstance.createAccessResource(owner, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#createAccessResource");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="deleteAccessResource"></a>
# **deleteAccessResource**
> Object deleteAccessResource(owner, uuid)

Delete access resource

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      Object result = apiInstance.deleteAccessResource(owner, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#deleteAccessResource");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getAccessResource"></a>
# **getAccessResource**
> V1AccessResource getAccessResource(owner, uuid)

Get access resource

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1AccessResource result = apiInstance.getAccessResource(owner, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#getAccessResource");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listAccessResourceNames"></a>
# **listAccessResourceNames**
> V1ListAccessResourcesResponse listAccessResourceNames(owner, offset, limit, sort, query)

List access resource names

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListAccessResourcesResponse result = apiInstance.listAccessResourceNames(owner, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#listAccessResourceNames");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listAccessResources"></a>
# **listAccessResources**
> V1ListAccessResourcesResponse listAccessResources(owner, offset, limit, sort, query)

List access resources

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListAccessResourcesResponse result = apiInstance.listAccessResources(owner, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#listAccessResources");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="patchAccessResource"></a>
# **patchAccessResource**
> V1AccessResource patchAccessResource(owner, accessResourceUuid, body)

Patch access resource

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String accessResourceUuid = "accessResourceUuid_example"; // String | UUID
    V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
    try {
      V1AccessResource result = apiInstance.patchAccessResource(owner, accessResourceUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#patchAccessResource");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **accessResourceUuid** | **String**| UUID |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="updateAccessResource"></a>
# **updateAccessResource**
> V1AccessResource updateAccessResource(owner, accessResourceUuid, body)

Update access resource

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.AccessResourcesV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    AccessResourcesV1Api apiInstance = new AccessResourcesV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String accessResourceUuid = "accessResourceUuid_example"; // String | UUID
    V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
    try {
      V1AccessResource result = apiInstance.updateAccessResource(owner, accessResourceUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AccessResourcesV1Api#updateAccessResource");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **accessResourceUuid** | **String**| UUID |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

