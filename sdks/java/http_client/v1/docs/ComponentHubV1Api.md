# ComponentHubV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveComponentHub**](ComponentHubV1Api.md#archiveComponentHub) | **POST** /api/v1/{owner}/hub/{name}/archive | Archive hub component
[**bookmarkComponentHub**](ComponentHubV1Api.md#bookmarkComponentHub) | **POST** /api/v1/{owner}/hub/{name}/bookmark | Bookmark component hub
[**createComponentHub**](ComponentHubV1Api.md#createComponentHub) | **POST** /api/v1/{owner}/hub/create | Create hub component
[**createComponentVersion**](ComponentHubV1Api.md#createComponentVersion) | **POST** /api/v1/{owner}/hub/{component}/versions | Create component version
[**createComponentVersionStage**](ComponentHubV1Api.md#createComponentVersionStage) | **POST** /api/v1/{owner}/hub/{entity}/versions/{name}/stages | Create new component version stage
[**deleteComponentHub**](ComponentHubV1Api.md#deleteComponentHub) | **DELETE** /api/v1/{owner}/hub/{name} | Delete hub component
[**deleteComponentVersion**](ComponentHubV1Api.md#deleteComponentVersion) | **DELETE** /api/v1/{owner}/hub/{entity}/versions/{name} | Delete component version
[**getComponentHub**](ComponentHubV1Api.md#getComponentHub) | **GET** /api/v1/{owner}/hub/{name} | Get hub component
[**getComponentHubActivities**](ComponentHubV1Api.md#getComponentHubActivities) | **GET** /api/v1/{owner}/hub/{name}/activities | Get hub activities
[**getComponentHubSettings**](ComponentHubV1Api.md#getComponentHubSettings) | **GET** /api/v1/{owner}/hub/{name}/settings | Get hub component settings
[**getComponentVersion**](ComponentHubV1Api.md#getComponentVersion) | **GET** /api/v1/{owner}/hub/{entity}/versions/{name} | Get component version
[**getComponentVersionStages**](ComponentHubV1Api.md#getComponentVersionStages) | **GET** /api/v1/{owner}/hub/{entity}/versions/{name}/stages | Get component version stages
[**listComponentHubNames**](ComponentHubV1Api.md#listComponentHubNames) | **GET** /api/v1/{owner}/hub/names | List hub component names
[**listComponentHubs**](ComponentHubV1Api.md#listComponentHubs) | **GET** /api/v1/{owner}/hub/list | List hub components
[**listComponentVersionNames**](ComponentHubV1Api.md#listComponentVersionNames) | **GET** /api/v1/{owner}/hub/{name}/versions/names | List component version names
[**listComponentVersions**](ComponentHubV1Api.md#listComponentVersions) | **GET** /api/v1/{owner}/hub/{name}/versions | List component versions
[**patchComponentHub**](ComponentHubV1Api.md#patchComponentHub) | **PATCH** /api/v1/{owner}/hub/{component.name} | Patch hub component
[**patchComponentHubSettings**](ComponentHubV1Api.md#patchComponentHubSettings) | **PATCH** /api/v1/{owner}/hub/{component}/settings | Patch hub component settings
[**patchComponentVersion**](ComponentHubV1Api.md#patchComponentVersion) | **PATCH** /api/v1/{owner}/hub/{component}/versions/{version.name} | Patch component version
[**restoreComponentHub**](ComponentHubV1Api.md#restoreComponentHub) | **POST** /api/v1/{owner}/hub/{name}/restore | Restore hub component
[**unbookmarkComponentHub**](ComponentHubV1Api.md#unbookmarkComponentHub) | **DELETE** /api/v1/{owner}/hub/{name}/unbookmark | Unbookmark component hub
[**updateComponentHub**](ComponentHubV1Api.md#updateComponentHub) | **PUT** /api/v1/{owner}/hub/{component.name} | Update hub component
[**updateComponentHubSettings**](ComponentHubV1Api.md#updateComponentHubSettings) | **PUT** /api/v1/{owner}/hub/{component}/settings | Update hub component settings
[**updateComponentVersion**](ComponentHubV1Api.md#updateComponentVersion) | **PUT** /api/v1/{owner}/hub/{component}/versions/{version.name} | Update component version


<a name="archiveComponentHub"></a>
# **archiveComponentHub**
> archiveComponentHub(owner, name)

Archive hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.archiveComponentHub(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#archiveComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="bookmarkComponentHub"></a>
# **bookmarkComponentHub**
> bookmarkComponentHub(owner, name)

Bookmark component hub

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.bookmarkComponentHub(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#bookmarkComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="createComponentHub"></a>
# **createComponentHub**
> V1ComponentHub createComponentHub(owner, body)

Create hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    V1ComponentHub body = new V1ComponentHub(); // V1ComponentHub | Component body
    try {
      V1ComponentHub result = apiInstance.createComponentHub(owner, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#createComponentHub");
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
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body |

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

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
**0** | An unexpected error response. |  -  |

<a name="createComponentVersion"></a>
# **createComponentVersion**
> V1ComponentVersion createComponentVersion(owner, component, body)

Create component version

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String component = "component_example"; // String | Component name
    V1ComponentVersion body = new V1ComponentVersion(); // V1ComponentVersion | Component version body
    try {
      V1ComponentVersion result = apiInstance.createComponentVersion(owner, component, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#createComponentVersion");
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
 **component** | **String**| Component name |
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body |

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

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
**0** | An unexpected error response. |  -  |

<a name="createComponentVersionStage"></a>
# **createComponentVersionStage**
> V1Stage createComponentVersionStage(owner, entity, name, body)

Create new component version stage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String entity = "entity_example"; // String | Entity namespace
    String name = "name_example"; // String | Name of the version to apply the stage to
    V1EntityStageBodyRequest body = new V1EntityStageBodyRequest(); // V1EntityStageBodyRequest | 
    try {
      V1Stage result = apiInstance.createComponentVersionStage(owner, entity, name, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#createComponentVersionStage");
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
 **entity** | **String**| Entity namespace |
 **name** | **String**| Name of the version to apply the stage to |
 **body** | [**V1EntityStageBodyRequest**](V1EntityStageBodyRequest.md)|  |

### Return type

[**V1Stage**](V1Stage.md)

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
**0** | An unexpected error response. |  -  |

<a name="deleteComponentHub"></a>
# **deleteComponentHub**
> deleteComponentHub(owner, name)

Delete hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.deleteComponentHub(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#deleteComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="deleteComponentVersion"></a>
# **deleteComponentVersion**
> deleteComponentVersion(owner, entity, name)

Delete component version

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
    String name = "name_example"; // String | Sub-entity name
    try {
      apiInstance.deleteComponentVersion(owner, entity, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#deleteComponentVersion");
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
 **entity** | **String**| Entity: project name, hub name, registry name, ... |
 **name** | **String**| Sub-entity name |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="getComponentHub"></a>
# **getComponentHub**
> V1ComponentHub getComponentHub(owner, name)

Get hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      V1ComponentHub result = apiInstance.getComponentHub(owner, name);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#getComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

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
**0** | An unexpected error response. |  -  |

<a name="getComponentHubActivities"></a>
# **getComponentHubActivities**
> V1ListActivitiesResponse getComponentHubActivities(owner, name, offset, limit, sort, query, mode)

Get hub activities

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Entity managing the resource
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    String mode = "mode_example"; // String | Mode the search.
    try {
      V1ListActivitiesResponse result = apiInstance.getComponentHubActivities(owner, name, offset, limit, sort, query, mode);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#getComponentHubActivities");
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
 **name** | **String**| Entity managing the resource |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search. | [optional]
 **mode** | **String**| Mode the search. | [optional]

### Return type

[**V1ListActivitiesResponse**](V1ListActivitiesResponse.md)

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
**0** | An unexpected error response. |  -  |

<a name="getComponentHubSettings"></a>
# **getComponentHubSettings**
> V1ComponentHubSettings getComponentHubSettings(owner, name)

Get hub component settings

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      V1ComponentHubSettings result = apiInstance.getComponentHubSettings(owner, name);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#getComponentHubSettings");
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
 **name** | **String**| Component under namesapce |

### Return type

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

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
**0** | An unexpected error response. |  -  |

<a name="getComponentVersion"></a>
# **getComponentVersion**
> V1ComponentVersion getComponentVersion(owner, entity, name)

Get component version

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
    String name = "name_example"; // String | Sub-entity name
    try {
      V1ComponentVersion result = apiInstance.getComponentVersion(owner, entity, name);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#getComponentVersion");
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
 **entity** | **String**| Entity: project name, hub name, registry name, ... |
 **name** | **String**| Sub-entity name |

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

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
**0** | An unexpected error response. |  -  |

<a name="getComponentVersionStages"></a>
# **getComponentVersionStages**
> V1Stage getComponentVersionStages(owner, entity, name)

Get component version stages

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
    String name = "name_example"; // String | Sub-entity name
    try {
      V1Stage result = apiInstance.getComponentVersionStages(owner, entity, name);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#getComponentVersionStages");
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
 **entity** | **String**| Entity: project name, hub name, registry name, ... |
 **name** | **String**| Sub-entity name |

### Return type

[**V1Stage**](V1Stage.md)

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
**0** | An unexpected error response. |  -  |

<a name="listComponentHubNames"></a>
# **listComponentHubNames**
> V1ListComponentHubsResponse listComponentHubNames(owner, offset, limit, sort, query)

List hub component names

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    try {
      V1ListComponentHubsResponse result = apiInstance.listComponentHubNames(owner, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#listComponentHubNames");
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
 **query** | **String**| Query filter the search. | [optional]

### Return type

[**V1ListComponentHubsResponse**](V1ListComponentHubsResponse.md)

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
**0** | An unexpected error response. |  -  |

<a name="listComponentHubs"></a>
# **listComponentHubs**
> V1ListComponentHubsResponse listComponentHubs(owner, offset, limit, sort, query)

List hub components

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    try {
      V1ListComponentHubsResponse result = apiInstance.listComponentHubs(owner, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#listComponentHubs");
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
 **query** | **String**| Query filter the search. | [optional]

### Return type

[**V1ListComponentHubsResponse**](V1ListComponentHubsResponse.md)

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
**0** | An unexpected error response. |  -  |

<a name="listComponentVersionNames"></a>
# **listComponentVersionNames**
> V1ListComponentVersionsResponse listComponentVersionNames(owner, name, offset, limit, sort, query, mode)

List component version names

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Entity managing the resource
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    String mode = "mode_example"; // String | Mode the search.
    try {
      V1ListComponentVersionsResponse result = apiInstance.listComponentVersionNames(owner, name, offset, limit, sort, query, mode);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#listComponentVersionNames");
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
 **name** | **String**| Entity managing the resource |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search. | [optional]
 **mode** | **String**| Mode the search. | [optional]

### Return type

[**V1ListComponentVersionsResponse**](V1ListComponentVersionsResponse.md)

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
**0** | An unexpected error response. |  -  |

<a name="listComponentVersions"></a>
# **listComponentVersions**
> V1ListComponentVersionsResponse listComponentVersions(owner, name, offset, limit, sort, query, mode)

List component versions

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Entity managing the resource
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    String mode = "mode_example"; // String | Mode the search.
    try {
      V1ListComponentVersionsResponse result = apiInstance.listComponentVersions(owner, name, offset, limit, sort, query, mode);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#listComponentVersions");
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
 **name** | **String**| Entity managing the resource |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search. | [optional]
 **mode** | **String**| Mode the search. | [optional]

### Return type

[**V1ListComponentVersionsResponse**](V1ListComponentVersionsResponse.md)

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
**0** | An unexpected error response. |  -  |

<a name="patchComponentHub"></a>
# **patchComponentHub**
> V1ComponentHub patchComponentHub(owner, componentName, body)

Patch hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String componentName = "componentName_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
    V1ComponentHub body = new V1ComponentHub(); // V1ComponentHub | Component body
    try {
      V1ComponentHub result = apiInstance.patchComponentHub(owner, componentName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#patchComponentHub");
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
 **componentName** | **String**| Optional component name, should be a valid fully qualified value: name[:version] |
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body |

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

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
**0** | An unexpected error response. |  -  |

<a name="patchComponentHubSettings"></a>
# **patchComponentHubSettings**
> V1ComponentHubSettings patchComponentHubSettings(owner, component, body)

Patch hub component settings

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String component = "component_example"; // String | Hub name
    V1ComponentHubSettings body = new V1ComponentHubSettings(); // V1ComponentHubSettings | Hub settings body
    try {
      V1ComponentHubSettings result = apiInstance.patchComponentHubSettings(owner, component, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#patchComponentHubSettings");
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
 **component** | **String**| Hub name |
 **body** | [**V1ComponentHubSettings**](V1ComponentHubSettings.md)| Hub settings body |

### Return type

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

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
**0** | An unexpected error response. |  -  |

<a name="patchComponentVersion"></a>
# **patchComponentVersion**
> V1ComponentVersion patchComponentVersion(owner, component, versionName, body)

Patch component version

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String component = "component_example"; // String | Component name
    String versionName = "versionName_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
    V1ComponentVersion body = new V1ComponentVersion(); // V1ComponentVersion | Component version body
    try {
      V1ComponentVersion result = apiInstance.patchComponentVersion(owner, component, versionName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#patchComponentVersion");
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
 **component** | **String**| Component name |
 **versionName** | **String**| Optional component name, should be a valid fully qualified value: name[:version] |
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body |

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

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
**0** | An unexpected error response. |  -  |

<a name="restoreComponentHub"></a>
# **restoreComponentHub**
> restoreComponentHub(owner, name)

Restore hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.restoreComponentHub(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#restoreComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="unbookmarkComponentHub"></a>
# **unbookmarkComponentHub**
> unbookmarkComponentHub(owner, name)

Unbookmark component hub

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.unbookmarkComponentHub(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#unbookmarkComponentHub");
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
 **name** | **String**| Component under namesapce |

### Return type

null (empty response body)

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
**0** | An unexpected error response. |  -  |

<a name="updateComponentHub"></a>
# **updateComponentHub**
> V1ComponentHub updateComponentHub(owner, componentName, body)

Update hub component

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String componentName = "componentName_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
    V1ComponentHub body = new V1ComponentHub(); // V1ComponentHub | Component body
    try {
      V1ComponentHub result = apiInstance.updateComponentHub(owner, componentName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#updateComponentHub");
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
 **componentName** | **String**| Optional component name, should be a valid fully qualified value: name[:version] |
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body |

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

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
**0** | An unexpected error response. |  -  |

<a name="updateComponentHubSettings"></a>
# **updateComponentHubSettings**
> V1ComponentHubSettings updateComponentHubSettings(owner, component, body)

Update hub component settings

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String component = "component_example"; // String | Hub name
    V1ComponentHubSettings body = new V1ComponentHubSettings(); // V1ComponentHubSettings | Hub settings body
    try {
      V1ComponentHubSettings result = apiInstance.updateComponentHubSettings(owner, component, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#updateComponentHubSettings");
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
 **component** | **String**| Hub name |
 **body** | [**V1ComponentHubSettings**](V1ComponentHubSettings.md)| Hub settings body |

### Return type

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

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
**0** | An unexpected error response. |  -  |

<a name="updateComponentVersion"></a>
# **updateComponentVersion**
> V1ComponentVersion updateComponentVersion(owner, component, versionName, body)

Update component version

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.ComponentHubV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    ComponentHubV1Api apiInstance = new ComponentHubV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String component = "component_example"; // String | Component name
    String versionName = "versionName_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
    V1ComponentVersion body = new V1ComponentVersion(); // V1ComponentVersion | Component version body
    try {
      V1ComponentVersion result = apiInstance.updateComponentVersion(owner, component, versionName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling ComponentHubV1Api#updateComponentVersion");
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
 **component** | **String**| Component name |
 **versionName** | **String**| Optional component name, should be a valid fully qualified value: name[:version] |
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body |

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

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
**0** | An unexpected error response. |  -  |

