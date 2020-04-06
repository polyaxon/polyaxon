# PolyaxonSdk.OrganizationsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**organizationsV1CreateOrganization**](OrganizationsV1Api.md#organizationsV1CreateOrganization) | **POST** /api/v1/orgs/create | 
[**organizationsV1CreateOrganizationMember**](OrganizationsV1Api.md#organizationsV1CreateOrganizationMember) | **POST** /api/v1/orgs/{owner}/members | 
[**organizationsV1DeleteOrganization**](OrganizationsV1Api.md#organizationsV1DeleteOrganization) | **DELETE** /api/v1/orgs/{owner} | 
[**organizationsV1DeleteOrganizationMember**](OrganizationsV1Api.md#organizationsV1DeleteOrganizationMember) | **DELETE** /api/v1/orgs/{owner}/members/{user} | 
[**organizationsV1GetOrganization**](OrganizationsV1Api.md#organizationsV1GetOrganization) | **GET** /api/v1/orgs/{owner} | 
[**organizationsV1GetOrganizationMember**](OrganizationsV1Api.md#organizationsV1GetOrganizationMember) | **GET** /api/v1/orgs/{owner}/members/{user} | 
[**organizationsV1ListOrganizationMembers**](OrganizationsV1Api.md#organizationsV1ListOrganizationMembers) | **GET** /api/v1/orgs/{owner}/members | 
[**organizationsV1ListOrganizationNames**](OrganizationsV1Api.md#organizationsV1ListOrganizationNames) | **GET** /api/v1/orgs/names | Get versions
[**organizationsV1ListOrganizations**](OrganizationsV1Api.md#organizationsV1ListOrganizations) | **GET** /api/v1/orgs/list | Get log handler
[**organizationsV1PatchOrganization**](OrganizationsV1Api.md#organizationsV1PatchOrganization) | **PATCH** /api/v1/orgs/{owner} | 
[**organizationsV1PatchOrganizationMember**](OrganizationsV1Api.md#organizationsV1PatchOrganizationMember) | **PATCH** /api/v1/orgs/{owner}/members/{member.user} | 
[**organizationsV1UpdateOrganization**](OrganizationsV1Api.md#organizationsV1UpdateOrganization) | **PUT** /api/v1/orgs/{owner} | 
[**organizationsV1UpdateOrganizationMember**](OrganizationsV1Api.md#organizationsV1UpdateOrganizationMember) | **PUT** /api/v1/orgs/{owner}/members/{member.user} | 


<a name="organizationsV1CreateOrganization"></a>
# **organizationsV1CreateOrganization**
> V1Organization organizationsV1CreateOrganization(body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var body = new PolyaxonSdk.V1Organization(); // V1Organization | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1CreateOrganization(body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**V1Organization**](V1Organization.md)|  | 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1CreateOrganizationMember"></a>
# **organizationsV1CreateOrganizationMember**
> V1OrganizationMember organizationsV1CreateOrganizationMember(owner, body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1CreateOrganizationMember(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1DeleteOrganization"></a>
# **organizationsV1DeleteOrganization**
> organizationsV1DeleteOrganization(owner)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.organizationsV1DeleteOrganization(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1DeleteOrganizationMember"></a>
# **organizationsV1DeleteOrganizationMember**
> organizationsV1DeleteOrganizationMember(owner, user)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var user = "user_example"; // String | Memeber under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.organizationsV1DeleteOrganizationMember(owner, user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **user** | **String**| Memeber under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1GetOrganization"></a>
# **organizationsV1GetOrganization**
> V1Organization organizationsV1GetOrganization(owner)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1GetOrganization(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1GetOrganizationMember"></a>
# **organizationsV1GetOrganizationMember**
> V1OrganizationMember organizationsV1GetOrganizationMember(owner, user)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var user = "user_example"; // String | Memeber under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1GetOrganizationMember(owner, user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **user** | **String**| Memeber under namesapce | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizationMembers"></a>
# **organizationsV1ListOrganizationMembers**
> V1ListOrganizationMembersResponse organizationsV1ListOrganizationMembers(owner, opts)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1ListOrganizationMembers(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizationNames"></a>
# **organizationsV1ListOrganizationNames**
> V1ListOrganizationsResponse organizationsV1ListOrganizationNames()

Get versions

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1ListOrganizationNames(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizations"></a>
# **organizationsV1ListOrganizations**
> V1ListOrganizationsResponse organizationsV1ListOrganizations()

Get log handler

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1ListOrganizations(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1PatchOrganization"></a>
# **organizationsV1PatchOrganization**
> V1Organization organizationsV1PatchOrganization(owner, body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1PatchOrganization(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1PatchOrganizationMember"></a>
# **organizationsV1PatchOrganizationMember**
> V1OrganizationMember organizationsV1PatchOrganizationMember(owner, member_user, body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var member_user = "member_user_example"; // String | User

var body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1PatchOrganizationMember(owner, member_user, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1UpdateOrganization"></a>
# **organizationsV1UpdateOrganization**
> V1Organization organizationsV1UpdateOrganization(owner, body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1UpdateOrganization(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1UpdateOrganizationMember"></a>
# **organizationsV1UpdateOrganizationMember**
> V1OrganizationMember organizationsV1UpdateOrganizationMember(owner, member_user, body)



### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.OrganizationsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var member_user = "member_user_example"; // String | User

var body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.organizationsV1UpdateOrganizationMember(owner, member_user, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

