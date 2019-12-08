# PolyaxonSdk.OrganizationsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createOrganization**](OrganizationsV1Api.md#createOrganization) | **POST** /api/v1/organizations/create | List runs
[**createOrganizationMember**](OrganizationsV1Api.md#createOrganizationMember) | **POST** /api/v1/organizations/{owner}/members | Delete runs
[**deleteOrganization**](OrganizationsV1Api.md#deleteOrganization) | **DELETE** /api/v1/organizations/{owner} | Patch run
[**deleteOrganizationMember**](OrganizationsV1Api.md#deleteOrganizationMember) | **DELETE** /api/v1/organizations/{owner}/members/{user} | Invalidate runs
[**getOrganization**](OrganizationsV1Api.md#getOrganization) | **GET** /api/v1/organizations/{owner} | Create new run
[**getOrganizationMember**](OrganizationsV1Api.md#getOrganizationMember) | **GET** /api/v1/organizations/{owner}/members/{user} | Stop run
[**listOrganizationMembers**](OrganizationsV1Api.md#listOrganizationMembers) | **GET** /api/v1/organizations/{owner}/members | Delete run
[**listOrganizationNames**](OrganizationsV1Api.md#listOrganizationNames) | **GET** /api/v1/organizations/names | List bookmarked runs for user
[**listOrganizations**](OrganizationsV1Api.md#listOrganizations) | **GET** /api/v1/organizations/list | List archived runs for user
[**patchOrganization**](OrganizationsV1Api.md#patchOrganization) | **PATCH** /api/v1/organizations/{owner} | Update run
[**patchOrganizationMember**](OrganizationsV1Api.md#patchOrganizationMember) | **PATCH** /api/v1/organizations/{owner}/members/{member.user} | Invalidate run
[**updateOrganization**](OrganizationsV1Api.md#updateOrganization) | **PUT** /api/v1/organizations/{owner} | Get run
[**updateOrganizationMember**](OrganizationsV1Api.md#updateOrganizationMember) | **PUT** /api/v1/organizations/{owner}/members/{member.user} | Stop runs


<a name="createOrganization"></a>
# **createOrganization**
> V1Organization createOrganization(body)

List runs

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
apiInstance.createOrganization(body, callback);
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

<a name="createOrganizationMember"></a>
# **createOrganizationMember**
> V1OrganizationMember createOrganizationMember(owner, body)

Delete runs

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
apiInstance.createOrganizationMember(owner, body, callback);
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

<a name="deleteOrganization"></a>
# **deleteOrganization**
> deleteOrganization(owner)

Patch run

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
apiInstance.deleteOrganization(owner, callback);
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

<a name="deleteOrganizationMember"></a>
# **deleteOrganizationMember**
> deleteOrganizationMember(owner, user)

Invalidate runs

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
apiInstance.deleteOrganizationMember(owner, user, callback);
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

<a name="getOrganization"></a>
# **getOrganization**
> V1Organization getOrganization(owner)

Create new run

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
apiInstance.getOrganization(owner, callback);
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

<a name="getOrganizationMember"></a>
# **getOrganizationMember**
> V1OrganizationMember getOrganizationMember(owner, user)

Stop run

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
apiInstance.getOrganizationMember(owner, user, callback);
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

<a name="listOrganizationMembers"></a>
# **listOrganizationMembers**
> V1ListOrganizationMembersResponse listOrganizationMembers(owner)

Delete run

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
apiInstance.listOrganizationMembers(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listOrganizationNames"></a>
# **listOrganizationNames**
> V1ListOrganizationsResponse listOrganizationNames()

List bookmarked runs for user

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
apiInstance.listOrganizationNames(callback);
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

<a name="listOrganizations"></a>
# **listOrganizations**
> V1ListOrganizationsResponse listOrganizations()

List archived runs for user

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
apiInstance.listOrganizations(callback);
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

<a name="patchOrganization"></a>
# **patchOrganization**
> V1Organization patchOrganization(owner, body)

Update run

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
apiInstance.patchOrganization(owner, body, callback);
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

<a name="patchOrganizationMember"></a>
# **patchOrganizationMember**
> V1OrganizationMember patchOrganizationMember(owner, member_user, body)

Invalidate run

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
apiInstance.patchOrganizationMember(owner, member_user, body, callback);
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

<a name="updateOrganization"></a>
# **updateOrganization**
> V1Organization updateOrganization(owner, body)

Get run

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
apiInstance.updateOrganization(owner, body, callback);
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

<a name="updateOrganizationMember"></a>
# **updateOrganizationMember**
> V1OrganizationMember updateOrganizationMember(owner, member_user, body)

Stop runs

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
apiInstance.updateOrganizationMember(owner, member_user, body, callback);
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

