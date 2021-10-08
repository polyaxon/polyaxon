# PolyaxonSdk.TagsV1Api

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



## createTag

> V1Tag createTag(owner, body)

Create tag

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Tag(); // V1Tag | Tag body
apiInstance.createTag(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## deleteTag

> deleteTag(owner, name)

Delete tag

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.deleteTag(owner, name, (error, data, response) => {
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
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getTag

> V1Tag getTag(owner, name)

Get tag

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getTag(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## listTags

> V1ListTagsResponse listTags(owner, opts)

List tags

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listTags(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListTagsResponse**](V1ListTagsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## loadTags

> V1LoadTagsResponse loadTags(owner, opts)

Load tags

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.loadTags(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1LoadTagsResponse**](V1LoadTagsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchTag

> V1Tag patchTag(owner, tag_name, body)

Patch tag

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let tag_name = "tag_name_example"; // String | Tag name
let body = new PolyaxonSdk.V1Tag(); // V1Tag | Tag body
apiInstance.patchTag(owner, tag_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **tag_name** | **String**| Tag name | 
 **body** | [**V1Tag**](V1Tag.md)| Tag body | 

### Return type

[**V1Tag**](V1Tag.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## syncTags

> syncTags(owner, body)

Sync tags

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1EntitiesTags(); // V1EntitiesTags | Data
apiInstance.syncTags(owner, body, (error, data, response) => {
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
 **body** | [**V1EntitiesTags**](V1EntitiesTags.md)| Data | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateTag

> V1Tag updateTag(owner, tag_name, body)

Update tag

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.TagsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let tag_name = "tag_name_example"; // String | Tag name
let body = new PolyaxonSdk.V1Tag(); // V1Tag | Tag body
apiInstance.updateTag(owner, tag_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **tag_name** | **String**| Tag name | 
 **body** | [**V1Tag**](V1Tag.md)| Tag body | 

### Return type

[**V1Tag**](V1Tag.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

