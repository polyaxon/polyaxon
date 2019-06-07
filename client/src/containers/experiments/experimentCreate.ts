import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as experimentsActions from '../../actions/experiments';
import * as projectsActions from '../../actions/projects';
import ExperimentCreate from '../../components/experiments/experimentCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const isLoading = isTrue(state.loadingIndicators.experiments.global.create);
  const isProjectEntity = _.isNil(props.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: props.match.params.user || state.auth.user,
    projectName: props.match.params.projectName,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.experiments.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (experiment: ExperimentModel) => experimentsActions.ExperimentAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<experimentsActions.ExperimentAction>, params: any): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel, user?: string, projectName?: string) => dispatch(
      experimentsActions.createExperiment(
        user || params.match.params.user,
        projectName || params.match.params.projectName,
        experiment,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentCreate));
