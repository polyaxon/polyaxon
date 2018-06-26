import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';
import Groups from '../components/groups';
import { GroupModel } from '../models/group';
import * as actions from '../actions/group';
import { getPaginatedSlice } from '../constants/paginate';

interface OwnProps {
  user: string;
  projectName: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let useFilter = () => {
    let groups: GroupModel[] = [];
    let project = state.projects.byUniqueNames[ownProps.projectName];
    let groupNames = project.groups;
    groupNames = getPaginatedSlice(groupNames);
    groupNames.forEach(
      function (group: string, idx: number) {
        groups.push(state.groups.byUniqueNames[group]);
      });
    return {groups: groups, count: project.num_experiment_groups};
  };

  let useLastFetched = () => {
    let groupNames = state.groups.lastFetched.names;
    let count = state.groups.lastFetched.count;
    let groups: GroupModel[] = [];
    groupNames.forEach(
      function (group: string, idx: number) {
        groups.push(state.groups.byUniqueNames[group]);
      });
    return {groups: groups, count: count};
  };
  let results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    groups: results.groups,
    count: results.count
  };
}

export interface DispatchProps {
  onCreate?: (group: GroupModel) => actions.GroupAction;
  onDelete?: (group: GroupModel) => actions.GroupAction;
  onUpdate?: (group: GroupModel) => actions.GroupAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroupActionCreator(group)),
    onDelete: (group: GroupModel) => dispatch(actions.deleteGroupActionCreator(group)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroupActionCreator(group)),
    fetchData: (offset?: number, query?: string, sort?: string) => {
      let filters: {[key: string]: number|boolean|string} = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      return dispatch(actions.fetchGroups(ownProps.projectName, filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
