import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";

import { AppState } from "../types/index";
import ProjectDetail from "../components/ProjectDetail";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState, params: any)  {
  let projectId = parseInt(params.match.params.projectId);
  if (state.projects.ids.includes(projectId)) {
    return {project: state.projects.byIds[projectId]};
  }
  return null;
}

export interface DispatchProps {
  onDelete?: (projectId: number) => any;
  fetchData?: (projectId: number) => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>): DispatchProps {
  return {
    onDelete: (projectId: number) => dispatch(actions.deleteProject(projectId)),
    fetchData: (projectId: number) => dispatch(actions.fetchProject(projectId))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
