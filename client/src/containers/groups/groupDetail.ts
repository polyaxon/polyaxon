import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/groups';
import GroupDetail from '../../components/groups/groupDetail';
import { AppState } from '../../constants/types';
import { getGroupUniqueName } from '../../constants/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const groupUniqueName = getGroupUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.groupId);
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
  stopTensorboard: () => actions.GroupAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchGroup(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateGroup(
        getGroupUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.groupId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteGroup(
      getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId),
      true
    )),
    onStop: () => dispatch(actions.stopGroup(
      getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId)
    )),
    onArchive: () => dispatch(actions.archiveGroup(
      getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId),
    true)),
    onRestore: () => dispatch(actions.restoreGroup(
      getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId)
    )),
    bookmark: () => dispatch(
      actions.bookmark(getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getGroupUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.groupId))),
    stopTensorboard: () => dispatch(
      actions.stopTensorboard(
        getGroupUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.groupId)))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupDetail));
