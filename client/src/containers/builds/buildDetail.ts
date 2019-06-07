import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/builds';
import BuildDetail from '../../components/builds/buildDetail';
import { getBuildUniqueName } from '../../constants/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const buildUniqueName = getBuildUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.buildId);
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

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchBuild(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.buildId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateBuild(
        getBuildUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.buildId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteBuild(
      getBuildUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.buildId),
      true)),
    onStop: () => dispatch(actions.stopBuild(getBuildUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.buildId))),
    onArchive: () => dispatch(actions.archiveBuild(getBuildUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.buildId),
                                                   true)),
    onRestore: () => dispatch(actions.restoreBuild(getBuildUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.buildId))),
    bookmark: () => dispatch(
      actions.bookmark(getBuildUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.buildId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getBuildUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.buildId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildDetail));
