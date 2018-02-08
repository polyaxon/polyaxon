import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import Projects from '../components/projects';
import { ProjectModel } from '../models/project';
import { sortByUpdatedAt } from '../constants/utils';
import * as actions from '../actions/project';
import * as modalActions from '../actions/modal';
import { modalTypes, modalPropsByTypes } from '../models/modal';

export function mapStateToProps(state: AppState, params: any)  {
  let results = {projects: <ProjectModel[]> [], user: params.match.params.user};
  if (state.projects) {
    results.projects = Object.keys(state.projects.byUniqueNames).map(
      key => state.projects.byUniqueNames[key]).sort(sortByUpdatedAt);
  }
  return results;
}

export interface DispatchProps {
  onDelete?: (project: ProjectModel) => any;
  onUpdate?: (project: ProjectModel) => any;
  fetchData?: () => any;
  showModal: () => any;
  hideModal: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onDelete: (project: ProjectModel) => dispatch(actions.deleteProject(project)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectActionCreator(project)),
    fetchData: () => dispatch(actions.fetchProjects(params.match.params.user)),
    showModal: () => dispatch(modalActions.showModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {
          ...modalPropsByTypes[modalTypes.CREATE_PROJECT],
          show: true,
          submitCb: (project: ProjectModel) => dispatch(actions.createProject(params.match.params.user, project))}
      })),
    hideModal: () => dispatch(modalActions.hideModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {...modalPropsByTypes[modalTypes.CREATE_PROJECT], show: false}
      })),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
