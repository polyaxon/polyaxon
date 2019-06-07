import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/experimentJobs';
import ExperimentJobDetail from '../../components/experimentJobs/experimentJobDetail';
import { getExperimentJobUniqueName } from '../../constants/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const jobUniqueName = getExperimentJobUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.experimentId,
    props.match.params.jobId);
  return _.includes(state.experimentJobs.uniqueNames, jobUniqueName) ?
    {job: state.experimentJobs.byUniqueNames[jobUniqueName]} :
    {job: null};
}

export interface DispatchProps {
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchExperimentJob(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.experimentId,
        props.match.params.jobId))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentJobDetail));
