import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";

import { AppState } from "../constants/types";
import { ProjectModel } from "../models/project";
import ProjectDetail from "../components/projectDetail";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState, params: any)  {
  let projectName = params.match.params.projectName;
  let results;
  state.projects.uniqueNames.forEach(function (uniqueName: string, idx: number) {
    if (state.projects.ByUniqueNames[uniqueName].name === projectName) {
      results = {project: state.projects.ByUniqueNames[uniqueName]};
    }
  });
  if (!results) {
    results = {project: null};
  }
  return results;
}

export interface DispatchProps {
  onDelete?: (project: ProjectModel) => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    onDelete: (project: ProjectModel) => dispatch(actions.deleteProject(project)),
    fetchData: () => dispatch(actions.fetchProject(params.match.params.user, params.match.params.projectName))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
