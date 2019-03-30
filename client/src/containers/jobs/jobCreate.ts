import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as jobsActions from '../../actions/jobs';
import * as projectsActions from '../../actions/projects';
import JobCreate from '../../components/jobs/jobCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { JobModel } from '../../models/job';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.jobs.global.create);
  const isProjectEntity = _.isNil(params.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: params.match.params.user || state.auth.user,
    projectName: params.match.params.projectName,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.jobs.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (job: JobModel) => jobsActions.JobAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<jobsActions.JobAction>, params: any): DispatchProps {
  return {
    onCreate: (job: JobModel, user?: string, projectName?: string) => dispatch(
      jobsActions.createJob(
        user || params.match.params.user,
        projectName || params.match.params.projectName,
        job,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobCreate));
