import { connect, Dispatch } from "react-redux";

import { AppState } from "../constants/types";
import Projects from "../components/projects";
import {ProjectModel} from "../models/project";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState)  {
  if (state.projects)
    return {projects: (<any>Object).values(state.projects.byIds)};
  return [];
}

export interface DispatchProps {
  onCreate?: (project: ProjectModel) => any;
  onDelete?: (projectId: number) => any;
  onUpdate?: (project: ProjectModel) => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>): DispatchProps {
  return {
    onCreate: (project: ProjectModel) => dispatch(actions.createProject(project)),
    onDelete: (projectId: number) => dispatch(actions.deleteProject(projectId)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProject(project)),
    fetchData: () => dispatch(actions.fetchProjects())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
