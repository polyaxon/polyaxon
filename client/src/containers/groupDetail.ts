import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import { GroupModel } from "../models/group";

import GroupDetail from "../components/groupDetail";
import * as actions from "../actions/group";


export function mapStateToProps(state: AppState, params: any)  {
  let groupSequence = parseInt(params.match.params.groupSequence);
  let results;
  
  state.groups.uuids.forEach(function (uuid: string, idx: number) {
    if (state.groups.byUuids[uuid].sequence === groupSequence) {
      results = {group: state.groups.byUuids[uuid]};
    }
  });

  if (!results) {
    results = {group: null};
  }
  return results;
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(() => {}),
    fetchData: () => dispatch(actions.fetchGroup(params.match.params.user, params.match.params.projectName, params.match.params.groupSequence))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupDetail));