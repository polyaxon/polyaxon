# TagsV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createTag**](TagsV1Api.md#createTag) | **POST** /api/v1/orgs/{owner}/tags | Create tag
[**deleteTag**](TagsV1Api.md#deleteTag) | **DELETE** /api/v1/orgs/{owner}/tags/{name} | Delete tag
[**getTag**](TagsV1Api.md#getTag) | **GET** /api/v1/orgs/{owner}/tags/{name} | Get tag
[**listTags**](TagsV1Api.md#listTags) | **GET** /api/v1/orgs/{owner}/tags | List tags
[**loadTags**](TagsV1Api.md#loadTags) | **GET** /api/v1/orgs/{owner}/tags/load | Load tags
[**patchTag**](TagsV1Api.md#patchTag) | **PATCH** /api/v1/orgs/{owner}/tags/{tag.name} | Patch tag
[**syncTags**](TagsV1Api.md#syncTags) | **POST** /api/v1/orgs/{owner}/tags/sync | Sync tags
[**updateTag**](TagsV1Api.md#updateTag) | **PUT** /api/v1/orgs/{owner}/tags/{tag.name} | Update tag


<a name="createTag"></a>
# **createTag**
> V1Tag createTag(owner, body)

Create tag

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    V1Tag body = new V1Tag(); // V1Tag | Tag body
    try {
      V1Tag result = apiInstance.createTag(owner, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#createTag");
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
 **body** | [**V1Tag**](V1Tag.md)| Tag body |

### Return type

[**V1Tag**](V1Tag.md)

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

<a name="deleteTag"></a>
# **deleteTag**
> deleteTag(owner, name)

Delete tag

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      apiInstance.deleteTag(owner, name);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#deleteTag");
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

<a name="getTag"></a>
# **getTag**
> V1Tag getTag(owner, name)

Get tag

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String name = "name_example"; // String | Component under namesapce
    try {
      V1Tag result = apiInstance.getTag(owner, name);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#getTag");
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

[**V1Tag**](V1Tag.md)

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

<a name="listTags"></a>
# **listTags**
> V1ListTagsResponse listTags(owner, offset, limit, sort, query, bookmarks, pins, mode, noPage)

List tags

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    Boolean bookmarks = true; // Boolean | Filter by bookmarks.
    String pins = "pins_example"; // String | Pinned entities.
    String mode = "mode_example"; // String | Mode of the search.
    Boolean noPage = true; // Boolean | No pagination.
    try {
      V1ListTagsResponse result = apiInstance.listTags(owner, offset, limit, sort, query, bookmarks, pins, mode, noPage);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#listTags");
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional]
 **pins** | **String**| Pinned entities. | [optional]
 **mode** | **String**| Mode of the search. | [optional]
 **noPage** | **Boolean**| No pagination. | [optional]

### Return type

[**V1ListTagsResponse**](V1ListTagsResponse.md)

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

<a name="loadTags"></a>
# **loadTags**
> V1LoadTagsResponse loadTags(owner, offset, limit, sort, query, bookmarks, pins, mode, noPage)

Load tags

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search.
    Boolean bookmarks = true; // Boolean | Filter by bookmarks.
    String pins = "pins_example"; // String | Pinned entities.
    String mode = "mode_example"; // String | Mode of the search.
    Boolean noPage = true; // Boolean | No pagination.
    try {
      V1LoadTagsResponse result = apiInstance.loadTags(owner, offset, limit, sort, query, bookmarks, pins, mode, noPage);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#loadTags");
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional]
 **pins** | **String**| Pinned entities. | [optional]
 **mode** | **String**| Mode of the search. | [optional]
 **noPage** | **Boolean**| No pagination. | [optional]

### Return type

[**V1LoadTagsResponse**](V1LoadTagsResponse.md)

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

<a name="patchTag"></a>
# **patchTag**
> V1Tag patchTag(owner, tagName, body)

Patch tag

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String tagName = "tagName_example"; // String | Tag name
    V1Tag body = new V1Tag(); // V1Tag | Tag body
    try {
      V1Tag result = apiInstance.patchTag(owner, tagName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#patchTag");
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
 **tagName** | **String**| Tag name |
 **body** | [**V1Tag**](V1Tag.md)| Tag body |

### Return type

[**V1Tag**](V1Tag.md)

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

<a name="syncTags"></a>
# **syncTags**
> syncTags(owner, body)

Sync tags

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    V1EntitiesTags body = new V1EntitiesTags(); // V1EntitiesTags | Data
    try {
      apiInstance.syncTags(owner, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#syncTags");
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
 **body** | [**V1EntitiesTags**](V1EntitiesTags.md)| Data |

### Return type

null (empty response body)

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

<a name="updateTag"></a>
# **updateTag**
> V1Tag updateTag(owner, tagName, body)

Update tag

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.TagsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    TagsV1Api apiInstance = new TagsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String tagName = "tagName_example"; // String | Tag name
    V1Tag body = new V1Tag(); // V1Tag | Tag body
    try {
      V1Tag result = apiInstance.updateTag(owner, tagName, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling TagsV1Api#updateTag");
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
 **tagName** | **String**| Tag name |
 **body** | [**V1Tag**](V1Tag.md)| Tag body |

### Return type

[**V1Tag**](V1Tag.md)

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

