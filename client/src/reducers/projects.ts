import {Reducer} from "redux";
import {normalize} from 'normalizr';
import * as _ from "lodash";

import {ProjectSchema} from "../constants/schemas"
import {ProjectAction, actionTypes} from "../actions/project";
import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

export const projectsReducer: Reducer<ProjectStateSchema> =
	(state: ProjectStateSchema = ProjectsEmptyState, action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.CREATE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.project.id] : action.project},
        ids: [...state.ids, action.project.id]
      };
    case actionTypes.DELETE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.projectId] : {...state.byIds[action.projectId], deleted:true}},
        ids: state.ids.filter(id => id != action.projectId),
      };
    case actionTypes.UPDATE_PROJECT:
      return {
        ...state,
        byIds: {...state.byIds, [action.project.id]: action.project}
      };
    case actionTypes.RECEIVE_PROJECTS:
      var newState = {...state};
      for (let project of action.projects) {
        if (!_.includes(newState.ids, project.id)) {
          newState.ids.push(project.id);
        }
        newState.byIds[project.id] = project;
      }
      return newState;
    case actionTypes.RECEIVE_PROJECT:
      var newState = {...state};
      if (!_.includes(newState.ids, action.project.id)) {
        newState.ids.push(action.project.id);
      }
      let normalized_projects = normalize(action.project, ProjectSchema).entities.projects;
      newState.byIds[action.project.id] = normalized_projects[action.project.id];
      return newState;
  }
  return state;
};

export const ProjectExperiments: Reducer<ExperimentStateSchema> =
	(state: ExperimentStateSchema = ExperimentsEmptyState, action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.RECEIVE_PROJECT:
      var newState = {...state};
      let normalized_project = normalize(action.project, ProjectSchema);
      let projectExperiments = normalized_project.entities.experiments;
      for (let _xpId of Object.keys(projectExperiments)) {
        let xpId = parseInt(_xpId);
        if (!_.includes(newState.ids, xpId)) {
          newState.ids.push(xpId);
          let xp = projectExperiments[xpId];
          newState.byIds[xpId] = {
            ...xp,
            createdAt: new Date(_.toString(xp.createdAt)),
            updatedAt: new Date(_.toString(xp.updatedAt))
          };
        }
      }
      return newState;
  }
  return state;
};
