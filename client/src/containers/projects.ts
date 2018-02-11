import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import Projects from '../components/projects';
import { ProjectModel } from '../models/project';
import * as actions from '../actions/project';
import * as modalActions from '../actions/modal';
import { modalTypes, modalPropsByTypes } from '../models/modal';
import { getPaginatedSlice } from '../constants/paginate';

export function mapStateToProps(state: AppState, params: any)  {
  let username = params.match.params.user;
  let projects: ProjectModel[] = [];
  let user = state.users.byUserNames[username];
  if (user == null) {
    return {user: username, projects: <ProjectModel[]> [], count: 0};
  }
  let projectNames = user.projects;
  projectNames = getPaginatedSlice(projectNames, state.pagination.projectCurrentPage);
  projectNames.forEach(
    function (project: string, idx: number) {
      projects.push(state.projects.byUniqueNames[project]);
    });

  return {user: username, projects: projects, count: user.num_projects};
}

export interface DispatchProps {
  onDelete?: (project: ProjectModel) => actions.ProjectAction;
  onUpdate?: (project: ProjectModel) => actions.ProjectAction;
  fetchData?: () => actions.ProjectAction;
  showModal: () => any;
  hideModal: () => any;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onDelete: (project: ProjectModel) => dispatch(actions.deleteProject(project)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectActionCreator(project)),
    fetchData: (currentPage?: number) => dispatch(
      actions.fetchProjects(params.match.params.user, currentPage)),
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
