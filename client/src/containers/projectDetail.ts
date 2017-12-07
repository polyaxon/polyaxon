import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import ProjectDetail from "../components/projectDetail";
import * as actions from "../actions/project";


export function mapStateToProps(state: AppState, params: any)  {
  let projectUuid = params.match.params.projectUuid;
  if (_.includes(state.projects.uuids, projectUuid)) {
    return {project: state.projects.byUuids[projectUuid]};
  }
  return {project: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(actions.deleteProject(params.match.params.projectUuid)),
    fetchData: () => dispatch(actions.fetchProject(params.match.params.projectUuid))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
