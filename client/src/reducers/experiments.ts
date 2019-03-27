import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, ExperimentAction } from '../actions/experiments';
import { ACTIONS } from '../constants/actions';
import { ExperimentSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { getExperimentIndexName } from '../constants/utils';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import {
  ExperimentModel,
  ExperimentParamStateSchema,
  ExperimentsEmptyState,
  ExperimentsParamsEmptyState,
  ExperimentStateSchema
} from '../models/experiment';
import { GroupsEmptyState, GroupStateSchema } from '../models/group';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const experimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    const setExperimentRelated = (experiment: ExperimentModel) => {
      if (experiment.jobs == null) {
        experiment.jobs = [];
      }
      return experiment;
    };
    const processExperiment = (experiment: ExperimentModel) => {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(experiment.deleted)) {
        experiment.deleted = false;
      }
      const normalizedExperiments = normalize(experiment, ExperimentSchema).entities.experiments;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName],
        ...normalizedExperiments[experiment.unique_name]
      };
      setExperimentRelated(newState.byUniqueNames[uniqueName]);
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== getExperimentIndexName(action.experimentName)),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter(
              (name) => name !== getExperimentIndexName(action.experimentName))
          },
        };
      case actionTypes.DELETE_EXPERIMENTS_SUCCESS:
        const experimentNames = action.experimentIds.map(
          (id: number) => action.projectName + '.' + id);
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => experimentNames.indexOf(name) === -1),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter(
              (name) => experimentNames.indexOf(name) === -1)
          },
        };
      case actionTypes.ARCHIVE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], deleted: false
            }
          },
        };
      case actionTypes.STOP_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], last_status: STOPPED
            }
          },
        };
      case actionTypes.STOP_EXPERIMENTS_SUCCESS:
        const byUniqueNames = {...state.byUniqueNames};
        for (const exprimentId of action.experimentIds) {
          const experimentName = action.projectName + '.' + exprimentId;
          byUniqueNames[experimentName] = {...byUniqueNames[experimentName], last_status: STOPPED};
        }
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            ...byUniqueNames
          },
        };
      case actionTypes.BOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [
              getExperimentIndexName(action.experiment.unique_name)]: setExperimentRelated(action.experiment)
          }
        };
      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], has_tensorboard: false
            }
          }
        };
      case actionTypes.FETCH_EXPERIMENTS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      case actionTypes.FETCH_EXPERIMENTS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.GET_EXPERIMENT_SUCCESS:
        return processExperiment(action.experiment);
      default:
        return state;
    }
  };

export const ExperimentsParamsReducer: Reducer<ExperimentParamStateSchema> =
  (state: ExperimentParamStateSchema = ExperimentsParamsEmptyState, action: ExperimentAction) => {
    let newState = {
      ...state,
      ...{lastFetched: new LastFetchedNames()}
    };

    const processExperiment = (experiment: ExperimentModel) => {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      const normalizedExperiments = normalize(experiment, ExperimentSchema).entities.experiments;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName],
        ...normalizedExperiments[experiment.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_EXPERIMENTS_PARAMS_SUCCESS:
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };

export const ProjectExperimentsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    const processExperiment = (experiment: ExperimentModel) => {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      const projectName = experiment.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].experiments, uniqueName)) {
        newState.byUniqueNames[projectName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_EXPERIMENT_SUCCESS:
        return processExperiment(action.experiment);
      case actionTypes.FETCH_EXPERIMENTS_SUCCESS:
        for (const experiment of action.experiments) {
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

    const processExperiment = (experiment: ExperimentModel) => {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      const groupName = experiment.experiment_group;
      if (groupName != null &&
        _.includes(newState.uniqueNames, groupName) &&
        !_.includes(newState.byUniqueNames[groupName].experiments, uniqueName)) {
        newState.byUniqueNames[groupName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_EXPERIMENT_SUCCESS:
        return processExperiment(action.experiment);
      case actionTypes.FETCH_EXPERIMENTS_SUCCESS:
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorExperimentReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: ExperimentAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_EXPERIMENT_ERROR:
      case actionTypes.UPDATE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_EXPERIMENT_ERROR:
      case actionTypes.GET_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_EXPERIMENT_ERROR:
      case actionTypes.DELETE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_EXPERIMENT_ERROR:
      case actionTypes.ARCHIVE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_EXPERIMENT_ERROR:
      case actionTypes.RESTORE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENT_ERROR:
      case actionTypes.STOP_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_EXPERIMENT_ERROR:
      case actionTypes.BOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_EXPERIMENT_ERROR:
      case actionTypes.UNBOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments, action.experimentName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_EXPERIMENT_TENSORBOARD_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments,
                                                   action.experimentName,
                                                   true,
                                                   ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_EXPERIMENT_TENSORBOARD_ERROR:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments,
                                                   action.experimentName,
                                                   false,
                                                   ACTIONS.START_TENSORBOARD)
        };

      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorById(state.experiments,
                                                   action.experimentName,
                                                   true,
                                                   ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_ERROR:
      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorById(
            state.experiments,
            action.experimentName,
            false,
            ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.STOP_EXPERIMENTS_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENTS_ERROR:
      case actionTypes.STOP_EXPERIMENTS_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, false, ACTIONS.STOP)
        };

      case actionTypes.FETCH_EXPERIMENTS_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENTS_ERROR:
      case actionTypes.FETCH_EXPERIMENTS_PARAMS_SUCCESS:
      case actionTypes.FETCH_EXPERIMENTS_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_EXPERIMENT_ERROR:
      case actionTypes.CREATE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processLoadingIndicatorGlobal(state.experiments, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const AlertExperimentReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: ExperimentAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorGlobal(
            processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, action.error, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, null, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments, action.experimentName, null, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        action.error,
                                        false,
                                        ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_EXPERIMENT_TENSORBOARD_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        null,
                                        null,
                                        ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_EXPERIMENT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        null,
                                        true,
                                        ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_EXPERIMENT_TENSORBOARD_ERROR:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        action.error,
                                        false,
                                        ACTIONS.START_TENSORBOARD)
        };

      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_REQUEST:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        null,
                                        null,
                                        ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          experiments: processErrorById(state.experiments,
                                        action.experimentName,
                                        null,
                                        true,
                                        ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_EXPERIMENT_TENSORBOARD_ERROR:
        return {
          ...state,
          experiments: processErrorById(
            state.experiments,
            action.experimentName,
            action.error,
            false,
            ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.STOP_EXPERIMENTS_REQUEST:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENTS_SUCCESS:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_EXPERIMENTS_ERROR:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, action.error, false, ACTIONS.STOP)
        };

      case actionTypes.FETCH_EXPERIMENTS_REQUEST:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENTS_PARAMS_SUCCESS:
      case actionTypes.FETCH_EXPERIMENTS_SUCCESS:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENTS_ERROR:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_EXPERIMENT_REQUEST:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_EXPERIMENT_SUCCESS:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_EXPERIMENT_ERROR:
        return {
          ...state,
          experiments: processErrorGlobal(state.experiments, action.error, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
