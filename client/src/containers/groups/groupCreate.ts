import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/groups';
import * as modalActions from '../../actions/modal';
import GroupCreate from '../../components/groups/groupCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { GroupModel } from '../../models/group';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.groups.global.create);
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading,
    errors: getErrorsGlobal(state.errors.groups.global, isLoading, ACTIONS.CREATE),
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
