import { Action } from 'redux';

export enum actionTypes {
  PAGINATE_PROJECT = 'PAGINATE_PROJECT',
  PAGINATE_GROUP = 'PAGINATE_GROUP',
  PAGINATE_EXPERIMENT = 'PAGINATE_EXPERIMENT',
  PAGINATE_JOB = 'PAGINATE_JOB',
  PAGINATE_EXPERIMENT_JOB = 'PAGINATE_EXPERIMENT_JOB',
}

export interface PaginationAction extends Action {
  type: actionTypes.PAGINATE_PROJECT
    | actionTypes.PAGINATE_GROUP
    | actionTypes.PAGINATE_EXPERIMENT
    | actionTypes.PAGINATE_JOB
    | actionTypes.PAGINATE_EXPERIMENT_JOB;
  currentPage: number;
}

export function paginateProjectActionCreator(currentPage: number): PaginationAction {
  return {
    type: actionTypes.PAGINATE_PROJECT,
    currentPage
  };
}

export function paginateGroupActionCreator(currentPage: number): PaginationAction {
  return {
    type: actionTypes.PAGINATE_GROUP,
    currentPage
  };
}

export function paginateExperimentActionCreator(currentPage: number): PaginationAction {
  return {
    type: actionTypes.PAGINATE_EXPERIMENT,
    currentPage
  };
}

export function paginateJobActionCreator(currentPage: number): PaginationAction {
  return {
    type: actionTypes.PAGINATE_JOB,
    currentPage
  };
}

export function paginateExperimentJobActionCreator(currentPage: number): PaginationAction {
  return {
    type: actionTypes.PAGINATE_EXPERIMENT_JOB,
    currentPage
  };
}

export function paginateProject(dispatch: any, currentPage?: number) {
  return dispatch(paginateProjectActionCreator(currentPage || 1));
}

export function paginateGroup(dispatch: any, currentPage?: number) {
  return dispatch(paginateGroupActionCreator(currentPage || 1));
}

export function paginateExperiment(dispatch: any, currentPage?: number) {
  return dispatch(paginateExperimentActionCreator(currentPage || 1));
}

export function paginateJob(dispatch: any, currentPage?: number) {
  return dispatch(paginateJobActionCreator(currentPage || 1));
}

export function paginateExperimentJob(dispatch: any, currentPage?: number) {
  return dispatch(paginateExperimentJobActionCreator(currentPage || 1));
}
