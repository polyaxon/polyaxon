import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/group';
import GroupDetail from '../components/groups/groupDetail';
import { AppState } from '../constants/types';
import { getGroupUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const groupUniqueName = getGroupUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.groupId);
  return _.includes(state.groups.uniqueNames, groupUniqueName) ?
    {group: state.groups.byUniqueNames[groupUniqueName]} :
    {group: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.GroupAction;
  onDelete: () => actions.GroupAction;
  onStop: () => actions.GroupAction;
  onArchive: () => actions.GroupAction;
  onRestore: () => actions.GroupAction;
  fetchData?: () => actions.GroupAction;
  bookmark: () => actions.GroupAction;
  unbookmark: () => actions.GroupAction;
  startTensorboard: () => actions.GroupAction;
  stopTensorboard: () => actions.GroupAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchGroup(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateGroup(
        getGroupUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.groupId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteGroup(
      getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId),
      true
    )),
    onStop: () => dispatch(actions.stopGroup(
      getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId)
    )),
    onArchive: () => dispatch(actions.archiveGroup(
      getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId),
    true)),
    onRestore: () => dispatch(actions.restoreGroup(
      getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId)
    )),
    bookmark: () => dispatch(
      actions.bookmark(getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getGroupUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId))),
    startTensorboard: () => dispatch(
      actions.startTensorboard(
        getGroupUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.groupId))),
    stopTensorboard: () => dispatch(
      actions.stopTensorboard(
        getGroupUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.groupId)))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupDetail));
