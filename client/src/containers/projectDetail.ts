import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import ProjectDetail from "../components/projectDetail";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState, params: any)  {
  let projectId = parseInt(params.match.params.projectId);
  if (_.includes(state.projects.ids, projectId)) {
    return {project: state.projects.byIds[projectId]};
  }
  return {project: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(actions.deleteProject(params.match.params.projectId)),
    fetchData: () => dispatch(actions.fetchProject(params.match.params.projectId))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
