import { connect, Dispatch } from "react-redux";

import { AppState } from "../constants/types";
import Projects from "../components/projects";
import {ProjectModel} from "../models/project";
import * as actions from "../actions/project";
import * as modalActions from "../actions/modal"
import {modalTypes, modalPropsByTypes} from "../models/modal";


export function mapStateToProps(state: AppState)  {
  if (state.projects)
    return {projects: (<any>Object).values(state.projects.byUuids)};
  return {projects: []};
}

export interface DispatchProps {
  onDelete?: (projectUuid: string) => any;
  onUpdate?: (project: ProjectModel) => any;
  fetchData?: () => any;
  showModal: () => any;
  hideModal: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>): DispatchProps {
  return {
    onDelete: (projectUuid: string) => dispatch(actions.deleteProject(projectUuid)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectActionCreator(project)),
    fetchData: () => dispatch(actions.fetchProjects()),
    showModal: () => dispatch(modalActions.showModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {...modalPropsByTypes[modalTypes.CREATE_PROJECT], show: true, submitCb: (project: ProjectModel) => dispatch(actions.createProject(project))}
      })),
    hideModal: () => dispatch(modalActions.hideModal(
      {
        type: modalTypes.CREATE_PROJECT,
        props: {...modalPropsByTypes[modalTypes.CREATE_PROJECT], show: false}
      })),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
