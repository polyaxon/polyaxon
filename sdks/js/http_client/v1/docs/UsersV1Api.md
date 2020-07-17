# PolyaxonSdk.UsersV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createToken**](UsersV1Api.md#createToken) | **POST** /api/v1/users/tokens | Create token
[**deleteToken**](UsersV1Api.md#deleteToken) | **DELETE** /api/v1/users/tokens/{uuid} | Delete token
[**getToken**](UsersV1Api.md#getToken) | **GET** /api/v1/users/tokens/{uuid} | Get token
[**getUser**](UsersV1Api.md#getUser) | **GET** /api/v1/users | Get current user
[**listTokens**](UsersV1Api.md#listTokens) | **GET** /api/v1/users/tokens | List tokens
[**patchToken**](UsersV1Api.md#patchToken) | **PATCH** /api/v1/users/tokens/{token.uuid} | Patch token
[**patchUser**](UsersV1Api.md#patchUser) | **PATCH** /api/v1/users | Patch current user
[**updateToken**](UsersV1Api.md#updateToken) | **PUT** /api/v1/users/tokens/{token.uuid} | Update token
[**updateUser**](UsersV1Api.md#updateUser) | **PUT** /api/v1/users | Update current user



## createToken

> V1Token createToken(body)

Create token

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let body = new PolyaxonSdk.V1Token(); // V1Token | Token body
apiInstance.createToken(body, (error, data, response) => {
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
 **body** | [**V1Token**](V1Token.md)| Token body | 

### Return type

[**V1Token**](V1Token.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteToken

> deleteToken(uuid)

Delete token

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let uuid = "uuid_example"; // String | UUid of the namespace
apiInstance.deleteToken(uuid, (error, data, response) => {
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
 **uuid** | **String**| UUid of the namespace | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getToken

> V1Token getToken(uuid)

Get token

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let uuid = "uuid_example"; // String | UUid of the namespace
apiInstance.getToken(uuid, (error, data, response) => {
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
 **uuid** | **String**| UUid of the namespace | 

### Return type

[**V1Token**](V1Token.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getUser

> V1User getUser()

Get current user

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
apiInstance.getUser((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**V1User**](V1User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listTokens

> V1ListTokenResponse listTokens(opts)

List tokens

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listTokens(opts, (error, data, response) => {
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
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListTokenResponse**](V1ListTokenResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchToken

> V1Token patchToken(token_uuid, body)

Patch token

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let token_uuid = "token_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Token(); // V1Token | Token body
apiInstance.patchToken(token_uuid, body, (error, data, response) => {
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
 **token_uuid** | **String**| UUID | 
 **body** | [**V1Token**](V1Token.md)| Token body | 

### Return type

[**V1Token**](V1Token.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchUser

> V1User patchUser(body)

Patch current user

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let body = new PolyaxonSdk.V1User(); // V1User | 
apiInstance.patchUser(body, (error, data, response) => {
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
 **body** | [**V1User**](V1User.md)|  | 

### Return type

[**V1User**](V1User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateToken

> V1Token updateToken(token_uuid, body)

Update token

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let token_uuid = "token_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Token(); // V1Token | Token body
apiInstance.updateToken(token_uuid, body, (error, data, response) => {
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
 **token_uuid** | **String**| UUID | 
 **body** | [**V1Token**](V1Token.md)| Token body | 

### Return type

[**V1Token**](V1Token.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateUser

> V1User updateUser(body)

Update current user

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.UsersV1Api();
let body = new PolyaxonSdk.V1User(); // V1User | 
apiInstance.updateUser(body, (error, data, response) => {
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
 **body** | [**V1User**](V1User.md)|  | 

### Return type

[**V1User**](V1User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

