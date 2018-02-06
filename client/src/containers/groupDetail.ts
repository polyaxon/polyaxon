import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import { AppState } from '../constants/types';
import GroupDetail from '../components/groupDetail';
import * as actions from '../actions/group';
import { getGroupUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  let groupUniqueName = getGroupUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.groupSequence);
  return _.includes(state.groups.uniqueNames, groupUniqueName) ?
      {group: state.groups.byUniqueNames[groupUniqueName]} :
      {group: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(() => undefined),
    fetchData: () => dispatch(
      actions.fetchGroup(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.groupSequence))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupDetail));
