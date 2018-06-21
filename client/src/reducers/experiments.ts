import { Reducer } from 'redux';
import * as _ from 'lodash';
import { normalize } from 'normalizr';

import { ExperimentSchema } from '../constants/schemas';
import { ExperimentAction, actionTypes } from '../actions/experiment';
import { ExperimentStateSchema, ExperimentsEmptyState, ExperimentModel } from '../models/experiment';
import { getExperimentIndexName } from '../constants/utils';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { GroupsEmptyState, GroupStateSchema } from '../models/group';

export const experimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    let processExperiment = function (experiment: ExperimentModel) {
      let uniqueName = getExperimentIndexName(experiment.unique_name);
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedExperiments = normalize(experiment, ExperimentSchema).entities.experiments;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedExperiments[experiment.unique_name]
      };
      if (newState.byUniqueNames[uniqueName].jobs == null) {
        newState.byUniqueNames[uniqueName].jobs = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          },
          uniqueNames: [...state.uniqueNames, getExperimentIndexName(action.experiment.unique_name)]
        };
      case actionTypes.DELETE_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experiment.unique_name)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experiment.unique_name)], deleted: true
            }
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== getExperimentIndexName(action.experiment.unique_name)),
        };
      case actionTypes.UPDATE_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          }
        };
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (let experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      default:
        return state;
    }
  };

export const ProjectExperimentsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    let processExperiment = function (experiment: ExperimentModel) {
      let uniqueName = getExperimentIndexName(experiment.unique_name);
      let projectName = experiment.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].experiments, uniqueName)) {
        newState.byUniqueNames[projectName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (let experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };

export const GroupExperimentsReducer: Reducer<GroupStateSchema> =
  (state: GroupStateSchema = GroupsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    let processExperiment = function (experiment: ExperimentModel) {
      let uniqueName = getExperimentIndexName(experiment.unique_name);
      let groupName = experiment.experiment_group;
      if (groupName != null &&
        _.includes(newState.uniqueNames, groupName) &&
        !_.includes(newState.byUniqueNames[groupName].experiments, uniqueName)) {
        newState.byUniqueNames[groupName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (let experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };
