import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {urlifyProjectName, getStoredToken} from "../constants/utils"
import {GroupModel} from "../models/group";
import {BASE_URL} from "../constants/api";


export enum actionTypes {
  CREATE_GROUP='CREATE_GROUP',
  DELETE_GROUP='DELETE_GROUP',
  UPDATE_GROUP='UPDATE_GROUP',
  RECEIVE_GROUP='RECEIVE_GROUP',
  RECEIVE_GROUPS='RECEIVE_GROUPS',
  REQUEST_GROUP='REQUEST_GROUP',
  REQUEST_GROUPS='REQUEST_GROUPS',
}

export interface CreateUpdateReceiveGroupAction extends Action {
  type: actionTypes.CREATE_GROUP | actionTypes.UPDATE_GROUP | actionTypes.RECEIVE_GROUP;
  group: GroupModel
}

export interface DeleteGroupAction extends Action {
  type: actionTypes.DELETE_GROUP;
  group: GroupModel
}

export interface ReceiveGroupsAction extends Action {
  type: actionTypes.RECEIVE_GROUPS;
  groups: GroupModel[]
}

export interface RequestGroupsAction extends Action {
  type: actionTypes.REQUEST_GROUPS;
}

export type GroupAction = CreateUpdateReceiveGroupAction | DeleteGroupAction | ReceiveGroupsAction | RequestGroupsAction;

export function createGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
    return {
      type: actionTypes.CREATE_GROUP,
      group
    }
}

export function updateGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
    return {
      type: actionTypes.UPDATE_GROUP,
      group
    }
}

export function deleteGroupActionCreator(group: GroupModel): DeleteGroupAction {
    return {
      type: actionTypes.DELETE_GROUP,
      group
    }
}

export function requestGroupsActionCreator(): RequestGroupsAction {
  return {
    type: actionTypes.REQUEST_GROUPS,
  }
}

export function receiveGroupsActionCreator(groups: GroupModel[]): ReceiveGroupsAction {
  return {
    type: actionTypes.RECEIVE_GROUPS,
    groups
  }
}
  
export function receiveGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
  return {
    type: actionTypes.RECEIVE_GROUP,
    group
  }
}

export function fetchGroups(projectUniqueName: string): Dispatch<GroupModel[]> {
  return (dispatch: any)=> {
    dispatch(requestGroupsActionCreator());
    return fetch(BASE_URL + `/${urlifyProjectName(projectUniqueName)}` + '/groups/', {
        headers: {
            'Authorization': 'token ' + getStoredToken()
        }
      })
      .then(response => response.json())
      .then(json => json.results.map((xp: {[key: string]: any})=> {
          return {
            ...xp,
            createdAt: new Date(_.toString(xp.created_at)),
            updatedAt: new Date(_.toString(xp.updated_at))};
        })
      )
      .then(json => dispatch(receiveGroupsActionCreator(json)))
  }
}

export function fetchGroup(user: string, projectName: string, groupSequence: number): Dispatch<GroupModel> {
  return (dispatch: any) => {
    dispatch(requestGroupsActionCreator());
    return fetch(BASE_URL + `/${user}` + `/${projectName}` + `/groups/` + `${groupSequence}`, {
        headers: {
            'Authorization': 'token ' + getStoredToken()
        }
    })
      .then(response => response.json())
      .then(json => {
          return {
            ...json,
            createdAt: new Date(_.toString(json.created_at)),
            updatedAt: new Date(_.toString(json.updated_at))};
        }
      )
      .then(json => dispatch(receiveGroupActionCreator(json)))
  }
}

