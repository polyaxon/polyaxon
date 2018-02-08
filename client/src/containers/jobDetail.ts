import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import { AppState } from '../constants/types';

import JobDetail from '../components/jobDetail';
import * as actions from '../actions/job';
import { getJobUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any)  {
  let jobUniqueName = getJobUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentSequence,
    params.match.params.jobSequence,);
  return _.includes(state.jobs.uniqueNames, jobUniqueName) ?
      {job: state.jobs.byUniqueNames[jobUniqueName]} :
      {job: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, params: any): DispatchProps {
  // TODO: We are probably using the wrong user here
  return {
    onDelete: () => dispatch(() => undefined),
    fetchData: () => dispatch(
      actions.fetchJob(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentSequence,
        params.match.params.jobSequence))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobDetail));
