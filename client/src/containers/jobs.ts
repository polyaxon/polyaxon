import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import Jobs from '../components/jobs';
import { JobModel } from '../models/job';

import * as actions from '../actions/job';
import { getOffset, getPaginatedSlice } from '../constants/paginate';

export function mapStateToProps(state: AppState, params: any) {
  let jobs: JobModel[] = [];
  let project = state.projects.byUniqueNames[params.projectName];
  let jobNames = project.jobs;
  jobNames = getPaginatedSlice(jobNames);
  jobNames.forEach(
    function (job: string, idx: number) {
      jobs.push(state.jobs.byUniqueNames[job]);
    });

  return {
    isCurrentUser: state.auth.user === params.user,
    jobs: jobs,
    count: project.num_jobs
  };
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
    fetchData: (currentPage?: number) => {
      let filters: {[key: string]: number|boolean|string} = {};
      let offset = getOffset(currentPage);
      if (offset != null) {
        filters.offset = offset;
      }
      return dispatch(actions.fetchJobs(params.projectName, filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Jobs);
