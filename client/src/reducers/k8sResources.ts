import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, K8SResourceAction } from '../actions/k8sResources';
import { ACTIONS } from '../constants/actions';
import { K8SResourceSchema } from '../constants/schemas';
import {
  AlertEmptyState,
  AlertSchema,
  initErrorById,
  initErrorGlobal,
  processErrorById,
  processErrorGlobal
} from '../models/alerts';
import { K8SResourceModel, K8SResourcesEmptyState, K8SResourceStateSchema } from '../models/k8sResource';
import {
  initLoadingIndicator, initLoadingIndicatorById,
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { LastFetchedNames } from '../models/utils';

export const K8SResourcesReducer: Reducer<K8SResourceStateSchema> =
  (state: K8SResourceStateSchema = K8SResourcesEmptyState, action: K8SResourceAction) => {
    let newState = {...state};

    const processK8SResource = (k8sResource: K8SResourceModel) => {
      const uniqueName = k8sResource.name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(k8sResource.deleted)) {
        k8sResource.deleted = false;
      }
      const normalizedK8SResources = normalize(k8sResource, K8SResourceSchema).entities.k8sResources;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedK8SResources[k8sResource.name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.name),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.name)
          },
        };
      case actionTypes.UPDATE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.k8sResource.name]: action.k8sResource}
        };
      case actionTypes.FETCH_K8S_RESOURCES_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_K8S_RESOURCES_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const k8sResource of action.k8sResources) {
          newState = processK8SResource(k8sResource);
        }
        return newState;
      case actionTypes.GET_K8S_RESOURCE_SUCCESS:
        return processK8SResource(action.k8sResource);
      default:
        return state;
    }
  };

export const LoadingIndicatorK8SResourceReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: K8SResourceAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processLoadingIndicatorById(state.k8sResources, action.name, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_K8S_RESOURCE_ERROR:
      case actionTypes.UPDATE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processLoadingIndicatorById(state.k8sResources, action.name, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.k8sResources, action.name, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_K8S_RESOURCE_ERROR:
      case actionTypes.GET_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processLoadingIndicatorById(state.k8sResources, action.name, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processLoadingIndicatorById(state.k8sResources, action.name, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_K8S_RESOURCE_ERROR:
      case actionTypes.DELETE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processLoadingIndicatorById(state.k8sResources, action.name, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_K8S_RESOURCES_REQUEST:
        return {
          ...state,
          k8sResources: processLoadingIndicatorGlobal(state.k8sResources, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_K8S_RESOURCES_ERROR:
      case actionTypes.FETCH_K8S_RESOURCES_SUCCESS:
        return {
          ...state,
          k8sResources: processLoadingIndicatorGlobal(state.k8sResources, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processLoadingIndicatorGlobal(state.k8sResources, true, ACTIONS.CREATE)
        };

      case actionTypes.CREATE_K8S_RESOURCE_ERROR:
      case actionTypes.CREATE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processLoadingIndicatorGlobal(state.k8sResources, false, ACTIONS.CREATE)
        };
      case actionTypes.INIT_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: action.name ?
            initLoadingIndicatorById(state.k8sResources, action.name) :
            initLoadingIndicator(state.k8sResources)
        };
      default:
        return state;
    }
  };

export const AlertK8SResourceReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: K8SResourceAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_K8S_RESOURCE_ERROR:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processErrorGlobal(
            processErrorById(state.k8sResources, action.name, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_K8S_RESOURCE_ERROR:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_K8S_RESOURCE_ERROR:
        return {
          ...state,
          k8sResources: processErrorById(state.k8sResources, action.name, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_K8S_RESOURCES_REQUEST:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_K8S_RESOURCES_SUCCESS:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_K8S_RESOURCES_ERROR:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, null, null, ACTIONS.CREATE)
        };
        case actionTypes.CREATE_K8S_RESOURCE_SUCCESS:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_K8S_RESOURCE_ERROR:
        return {
          ...state,
          k8sResources: processErrorGlobal(state.k8sResources, action.error, false, ACTIONS.CREATE)
        };

      case actionTypes.INIT_K8S_RESOURCE_REQUEST:
        return {
          ...state,
          k8sResources: action.name ?
            initErrorById(state.k8sResources, action.name) :
            initErrorGlobal(state.k8sResources)
        };
      default:
        return state;
    }
  };
