import { connect, Dispatch } from "react-redux";

import {sortByUpdatedAt} from "../constants/utils"
import { AppState } from "../constants/types";
import Groups from "../components/groups";
import {GroupModel} from "../models/group";
import * as actions from "../actions/group";

interface OwnProps {
  user: string;
  projectName: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let groups : GroupModel[] = [];
  if (state.groups) {
    state.groups.uniqueNames.forEach(function (uniqueName: string, idx: number) {
      let group = state.groups.ByUniqueNames[uniqueName];
      if (group.project_name === ownProps.projectName) {
        groups.push(group);
      }
    });
  }

  return {groups: groups.sort(sortByUpdatedAt)}
}

export interface DispatchProps {
  onCreate?: (group: GroupModel) => any;
  onDelete?: (group: GroupModel) => any;
  onUpdate?: (group: GroupModel) => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroupActionCreator(group)),
    onDelete: (group: GroupModel) => dispatch(actions.deleteGroupActionCreator(group)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroupActionCreator(group)),
    fetchData: () => dispatch(actions.fetchGroups(ownProps.projectName))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
