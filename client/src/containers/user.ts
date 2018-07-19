import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import { withRouter } from 'react-router-dom';

import { AppState } from '../constants/types';
import User from '../components/user';
import { ProjectModel } from '../models/project';
import * as actions from '../actions/project';
import * as modalActions from '../actions/modal';
import { modalTypes, modalPropsByTypes } from '../models/modal';

export function mapStateToProps(state: AppState, params: any) {
  return {user: params.match.params.user};
}

export interface DispatchProps {
  showModal: () => any;
  hideModal: () => any;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    showModal: () => dispatch(modalActions.showModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {
          ...modalPropsByTypes[modalTypes.CREATE_PROJECT],
          show: true,
          submitCb: (project: ProjectModel) => dispatch(actions.createProject(params.match.params.user, project))
        }
      })),
    hideModal: () => dispatch(modalActions.hideModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {...modalPropsByTypes[modalTypes.CREATE_PROJECT], show: false}
      })),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(User));
