import { Action } from 'redux';
import { SearchModel } from '../../models/search';
import { actionTypes } from './actionTypes';

export interface GetSearchSuccessAction extends Action {
  type: actionTypes.GET_SEARCH_SUCCESS_SUCCESS;
  search: SearchModel;
}

export function getSearchSuccessActionCreator(search: SearchModel): GetSearchSuccessAction {
  return {
    type: actionTypes.GET_SEARCH_SUCCESS_SUCCESS,
    search,
  };
}

export type GetSearchAction = GetSearchSuccessAction;
