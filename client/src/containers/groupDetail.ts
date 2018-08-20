import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/group';
import GroupDetail from '../components/groupDetail';
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
  onDelete?: () => any;
  fetchData?: () => any;
  bookmark: () => any;
  unbookmark: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchGroup(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId)),
    bookmark: () => dispatch(
      actions.bookmark(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId)),
    unbookmark: () => dispatch(
      actions.unbookmark(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupId))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupDetail));
