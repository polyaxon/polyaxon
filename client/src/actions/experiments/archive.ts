import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName, getProjectUrl } from '../../constants/utils';
import history from '../../history';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveExperimentRequestAction extends Action {
  type: actionTypes.ARCHIVE_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface ArchiveExperimentSuccessAction extends Action {
  type: actionTypes.ARCHIVE_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface ArchiveExperimentErrorAction extends Action {
  type: actionTypes.ARCHIVE_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function archiveExperimentRequestActionCreator(experimentName: string): ArchiveExperimentRequestAction {
  return {
    type: actionTypes.ARCHIVE_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function archiveExperimentSuccessActionCreator(experimentName: string): ArchiveExperimentSuccessAction {
  return {
    type: actionTypes.ARCHIVE_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function archiveExperimentErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    experimentName: string): ArchiveExperimentErrorAction {
  return {
    type: actionTypes.ARCHIVE_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type ArchiveExperimentAction =
  ArchiveExperimentRequestAction
  | ArchiveExperimentSuccessAction
  | ArchiveExperimentErrorAction;

export function archiveExperiment(experimentName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(archiveExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/archive`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to archive experiment',
        [experimentName]),
      )
      .then(() => {
        const dispatched = dispatch(archiveExperimentSuccessActionCreator(experimentName));
        if (redirect) {
          const values = experimentName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#experiments');
        }
        return dispatched;
      });
  };
}
