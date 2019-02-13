import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';

import * as actions from '../actions/build';
import buildDetail from '../components/builds/buildDetail';
import { getBuildUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const buildUniqueName = getBuildUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.buildId);
  return _.includes(state.builds.uniqueNames, buildUniqueName) ?
    {build: state.builds.byUniqueNames[buildUniqueName]} :
    {build: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.BuildAction;
  onDelete: () => actions.BuildAction;
  onStop: () => actions.BuildAction;
  onArchive: () => actions.BuildAction;
  onRestore: () => actions.BuildAction;
  fetchData?: () => actions.BuildAction;
  bookmark: () => actions.BuildAction;
  unbookmark: () => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchBuild(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.buildId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateBuild(
        getBuildUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.buildId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteBuild(
      getBuildUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.buildId),
      true)),
    onStop: () => dispatch(actions.stopBuild(getBuildUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.buildId))),
    onArchive: () => dispatch(actions.archiveBuild(getBuildUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.buildId),
      true)),
    onRestore: () => dispatch(actions.restoreBuild(getBuildUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.buildId))),
    bookmark: () => dispatch(
      actions.bookmark(getBuildUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.buildId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getBuildUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.buildId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(buildDetail));
