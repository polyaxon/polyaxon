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
        byUuids: {...state.byUuids, [action.project.uuid] : action.project},
        uuids: [...state.uuids, action.project.uuid]
      };
    case actionTypes.DELETE_PROJECT:
      return {
        ...state,
        byUuids: {...state.byUuids, [action.projectUuid] : {...state.byUuids[action.projectUuid], deleted:true}},
        uuids: state.uuids.filter(uuid => uuid != action.projectUuid),
      };
    case actionTypes.UPDATE_PROJECT:
      return {
        ...state,
        byUuids: {...state.byUuids, [action.project.uuid]: action.project}
      };
    case actionTypes.RECEIVE_PROJECTS:
      var newState = {...state};
      for (let project of action.projects) {
        if (!_.includes(newState.uuids, project.uuid)) {
          newState.uuids.push(project.uuid);
        }
        newState.byUuids[project.uuid] = project;
      }
      return newState;
    case actionTypes.RECEIVE_PROJECT:
      var newState = {...state};
      if (!_.includes(newState.uuids, action.project.uuid)) {
        newState.uuids.push(action.project.uuid);
      }
      let normalized_projects = normalize(action.project, ProjectSchema).entities.projects;
      newState.byUuids[action.project.uuid] = normalized_projects[action.project.uuid];
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
      for (let xpUuid of Object.keys(projectExperiments)) {
        if (!_.includes(newState.uuids, xpUuid)) {
          newState.uuids.push(xpUuid);
          let xp = projectExperiments[xpUuid];
          newState.byUuids[xpUuid] = {
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
