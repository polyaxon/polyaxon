import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import Groups from '../components/groups';
import { GroupModel } from '../models/group';
import * as actions from '../actions/group';
import { getPaginatedSlice } from '../constants/paginate';
import { getOffset } from '../constants/paginate';

interface OwnProps {
  user: string;
  projectName: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let groups: GroupModel[] = [];
  let project = state.projects.byUniqueNames[ownProps.projectName];
  let groupNames = project.groups;
  groupNames = getPaginatedSlice(groupNames);
  groupNames.forEach(
    function (group: string, idx: number) {
      groups.push(state.groups.byUniqueNames[group]);
    });

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    groups: groups,
    count: project.num_experiment_groups};
}

export interface DispatchProps {
  onCreate?: (group: GroupModel) => any;
  onDelete?: (group: GroupModel) => any;
  onUpdate?: (group: GroupModel) => any;
  fetchData?: (currentPage?: number) => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroupActionCreator(group)),
    onDelete: (group: GroupModel) => dispatch(actions.deleteGroupActionCreator(group)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroupActionCreator(group)),
    fetchData: (currentPage?: number) => {
      let filters: {[key: string]: number|boolean|string} = {};
      let offset = getOffset(currentPage);
      if (offset != null) {
        filters.offset = offset;
      }
      return dispatch(actions.fetchGroups(ownProps.projectName, filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
