import { Action } from 'redux';
import { SearchModel } from '../../models/search';
import { actionTypes } from './actionTypes';

export interface GetSearchSuccessAction extends Action {
  type: actionTypes.GET_SEARCH_SUCCESS;
  search: SearchModel;
  searchId: number;
}

export function getSearchSuccessActionCreator(search: SearchModel): GetSearchSuccessAction {
  return {
    type: actionTypes.GET_SEARCH_SUCCESS,
    search,
    searchId: search.id
  };
}

export type GetSearchAction = GetSearchSuccessAction;
