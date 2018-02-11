import { connect, Dispatch } from 'react-redux';

import { getExperimentIndexName } from '../constants/utils';
import { AppState } from '../constants/types';
import Jobs from '../components/jobs';
import { JobModel } from '../models/job';

import * as actions from '../actions/job';
import { getPaginatedSlice } from '../constants/paginate';

export function mapStateToProps(state: AppState, params: any) {
  let experimentName = getExperimentIndexName(params.experiment.unique_name);
  let jobs: JobModel[] = [];
  let experiment = state.experiments.byUniqueNames[experimentName];
  let jobNames = experiment.jobs;
  jobNames = getPaginatedSlice(jobNames, state.pagination.jobCurrentPage);
  jobNames.forEach(
    function (job: string, idx: number) {
      jobs.push(state.jobs.byUniqueNames[job]);
    });

  return {jobs: jobs, count: experiment.num_jobs};
}

export interface DispatchProps {
  onCreate?: (job: JobModel) => actions.JobAction;
  onDelete?: (job: JobModel) => actions.JobAction;
  onUpdate?: (job: JobModel) => actions.JobAction;
  fetchData?: (currentPage?: number) => actions.JobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, params: any): DispatchProps {
  return {
    onCreate: (job: JobModel) => dispatch(actions.createJobActionCreator(job)),
    onDelete: (job: JobModel) => dispatch(actions.deleteJobActionCreator(job)),
    onUpdate: (job: JobModel) => dispatch(actions.updateJobActionCreator(job)),
    fetchData: (currentPage?: number) => dispatch(
      actions.fetchJobs(params.experiment.project_name, params.experiment.sequence, currentPage))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Jobs);
