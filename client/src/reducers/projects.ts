import {Reducer} from "redux";

import {ProjectAction, actionTypes} from "../actions/project";
import {ProjectModel} from "../models/project";

export const projectsReducer: Reducer<{byIds: {[id: number]: ProjectModel}, ids: number[]}> =
	(state: {byIds: {[id: number]: ProjectModel}, ids: number[]} = {
    byIds: {10: {id: 10, name: 'name1'}, 20: {id: 20, name: 'name2'}},
    ids: [10, 20]
	}, action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.CREATE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.project.id] : project},
        ids: [...state.ids, action.project.id]
      };
    case actionTypes.DELETE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.projectId] : {...state.byIds[action.projectId], delete:true}},
        ids: state.ids.filter(id => id != action.projectId),
      };
    case actionTypes.UPDATE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.project.id]: action.project}
      };
  }
  return state;
};
