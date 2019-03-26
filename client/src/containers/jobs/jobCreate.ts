import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/jobs';
import * as modalActions from '../../actions/modal';
import JobCreate from '../../components/jobs/jobCreate';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { JobModel } from '../../models/job';

export function mapStateToProps(state: AppState, params: any) {
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading: isTrue(state.loadingIndicators.jobs.global.create),
    errors: state.errors.jobs.global.create,
  };
}

export interface DispatchProps {
  onCreate: (job: JobModel) => actions.JobAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.JobAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onCreate: (job: JobModel) => dispatch(
      actions.createJob(
        params.match.params.user,
        params.match.params.projectName,
        job,
        true)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobCreate));
