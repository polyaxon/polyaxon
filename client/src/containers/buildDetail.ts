import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import { withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import { AppState } from '../constants/types';

import * as actions from '../actions/build';
import { getBuildUniqueName } from '../constants/utils';
import buildDetail from '../components/buildDetail';

export function mapStateToProps(state: AppState, params: any) {
  let buildUniqueName = getBuildUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.buildId);
  return _.includes(state.builds.uniqueNames, buildUniqueName) ?
    {build: state.builds.byUniqueNames[buildUniqueName]} :
    {build: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchBuild(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.buildId))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(buildDetail));
