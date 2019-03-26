import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/jobs';
import * as modalActions from '../../actions/modal';
import JobCreate from '../../components/jobs/jobCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { JobModel } from '../../models/job';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.jobs.global.create);
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading,
    errors: getErrorsGlobal(state.errors.jobs.global, isLoading, ACTIONS.CREATE),
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
