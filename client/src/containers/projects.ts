import { connect, Dispatch } from "react-redux";

import { AppState } from "../types/index";
import Projects, {Props} from "../components/Projects";
import {ProjectModel} from "../models/project";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState)  {
  return {projects: state.projects}
}

export interface DispatchProps {
  onCreate?: (project: ProjectModel) => any;
  onDelete?: (projectId: number) => any;
  onUpdate?: (project: ProjectModel) => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>): DispatchProps {
  return {
    onCreate: (project: ProjectModel) => dispatch(actions.createProject(project)),
    onDelete: (projectId: number) => dispatch(actions.deleteProject(projectId)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProject(project)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
