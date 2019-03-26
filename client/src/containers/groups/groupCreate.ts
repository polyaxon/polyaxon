import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/groups';
import * as modalActions from '../../actions/modal';
import GroupCreate from '../../components/groups/groupCreate';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { GroupModel } from '../../models/group';

export function mapStateToProps(state: AppState, params: any) {
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading: isTrue(state.loadingIndicators.groups.global.create),
    errors: state.errors.groups.global.create,
  };
}

export interface DispatchProps {
  onCreate: (group: GroupModel) => actions.GroupAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.GroupAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(
      actions.createGroup(
        params.match.params.user,
        params.match.params.projectName,
        group,
        true)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupCreate));
