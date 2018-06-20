import { connect, Dispatch } from 'react-redux';

import { getExperimentIndexName } from '../constants/utils';
import { AppState } from '../constants/types';
import ExperimentJobs from '../components/experimentJobs';
import { ExperimentJobModel } from '../models/experimentJob';

import * as actions from '../actions/experimentJob';
import { getPaginatedSlice } from '../constants/paginate';

export function mapStateToProps(state: AppState, params: any) {
  let experimentName = getExperimentIndexName(params.experiment.unique_name);
  let jobs: ExperimentJobModel[] = [];
  let experiment = state.experiments.byUniqueNames[experimentName];
  let jobNames = experiment.jobs;
  jobNames = getPaginatedSlice(jobNames, state.pagination.experimentJobCurrentPage);
  jobNames.forEach(
    function (job: string, idx: number) {
      jobs.push(state.experimentJobs.byUniqueNames[job]);
    });

  return {jobs: jobs, count: experiment.num_jobs};
}

export interface DispatchProps {
  onCreate?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onDelete?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onUpdate?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  fetchData?: (currentPage?: number) => actions.ExperimentJobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, params: any): DispatchProps {
  return {
    onCreate: (job: ExperimentJobModel) => dispatch(actions.createExperimentJobActionCreator(job)),
    onDelete: (job: ExperimentJobModel) => dispatch(actions.deleteExperimentJobActionCreator(job)),
    onUpdate: (job: ExperimentJobModel) => dispatch(actions.updateExperimentJobActionCreator(job)),
    fetchData: (currentPage?: number) => dispatch(
      actions.fetchExperimentJobs(params.experiment.project_name, params.experiment.id, currentPage))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ExperimentJobs);
